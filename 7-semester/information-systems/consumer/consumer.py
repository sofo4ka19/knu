import json
import logging
import os
import random
import time

import pika
import psycopg2
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.propagate import extract
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import SpanKind
from prometheus_client import Counter, Histogram, start_http_server


class TraceIdFilter(logging.Filter):
    def filter(self, record):
        ctx = trace.get_current_span().get_span_context()
        record.trace_id = format(ctx.trace_id, "032x") if ctx.is_valid else "-"
        return True


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s trace_id=%(trace_id)s %(message)s",
)
for handler in logging.getLogger().handlers:
    handler.addFilter(TraceIdFilter())
logging.getLogger("pika").setLevel(logging.WARNING)
log = logging.getLogger("consumer")

QUEUE_NAME = "orders"
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))
OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "http://localhost:4318/v1/traces")

ACTIONS_TOTAL = Counter(
    "consumer_actions_total",
    "Events processed by the consumer",
    ["action", "status"],
)
ACTION_DURATION = Histogram(
    "consumer_action_duration_seconds",
    "Time to process one event (database work)",
    ["action"],
)


def setup_tracing():
    provider = TracerProvider(
        resource=Resource.create({"service.name": "shop-consumer"})
    )
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT))
    )
    trace.set_tracer_provider(provider)
    Psycopg2Instrumentor().instrument()


setup_tracing()
tracer = trace.get_tracer("consumer")


def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def connect_rabbit():
    while True:
        try:
            conn = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=os.getenv("RABBITMQ_HOST", "localhost"),
                    credentials=pika.PlainCredentials(
                        os.getenv("RABBITMQ_USER", "guest"),
                        os.getenv("RABBITMQ_PASSWORD", "guest"),
                    ),
                )
            )
            channel = conn.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            return channel
        except pika.exceptions.AMQPConnectionError:
            log.warning("RabbitMQ is not ready, retrying in 3s")
            time.sleep(3)


def create_customer(cur, payload):
    cur.execute(
        "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING id",
        (payload["name"], payload["email"]),
    )
    return f"customer #{cur.fetchone()[0]} created"


def create_order(cur, payload):
    cur.execute("SELECT id FROM customers ORDER BY random() LIMIT 1")
    customer = cur.fetchone()
    if customer is None:
        return "no customers yet, order skipped"

    cur.execute(
        "SELECT id, price FROM products ORDER BY random() LIMIT %s",
        (payload["items"],),
    )
    products = cur.fetchall()

    cur.execute(
        "INSERT INTO orders (customer_id) VALUES (%s) RETURNING id",
        (customer[0],),
    )
    order_id = cur.fetchone()[0]

    total = 0
    for product_id, price in products:
        quantity = random.randint(1, 3)
        cur.execute(
            """INSERT INTO order_items (order_id, product_id, quantity, price)
               VALUES (%s, %s, %s, %s)""",
            (order_id, product_id, quantity, price),
        )
        total += price * quantity

    cur.execute("UPDATE orders SET amount = %s WHERE id = %s", (total, order_id))
    return f"order #{order_id} created for customer #{customer[0]}, total {total}"


def update_order_status(cur, payload):
    cur.execute(
        """UPDATE orders SET status = %s
           WHERE id = (SELECT id FROM orders ORDER BY random() LIMIT 1)
           RETURNING id""",
        (payload["status"],),
    )
    row = cur.fetchone()
    return f"order #{row[0]} status changed to {payload['status']}" if row else "no orders yet"


def update_customer_email(cur, payload):
    cur.execute(
        """UPDATE customers SET email = %s
           WHERE id = (SELECT id FROM customers ORDER BY random() LIMIT 1)
           RETURNING id""",
        (payload["email"],),
    )
    row = cur.fetchone()
    return f"customer #{row[0]} changed email" if row else "no customers yet"


def delete_old_cancelled_orders(cur, payload):
    cur.execute(
        """DELETE FROM orders
           WHERE status = 'cancelled'
             AND created_at < now() - interval '2 minutes'"""
    )
    return f"deleted {cur.rowcount} old cancelled orders"


HANDLERS = {
    "create_customer": create_customer,
    "create_order": create_order,
    "update_order_status": update_order_status,
    "update_customer_email": update_customer_email,
    "delete_old_cancelled_orders": delete_old_cancelled_orders,
}


def main():
    start_http_server(METRICS_PORT)
    conn = connect_db()
    cur = conn.cursor()
    channel = connect_rabbit()
    channel.basic_qos(prefetch_count=10)

    def on_message(ch, method, properties, body):
        try:
            message = json.loads(body)
            name = message["type"]
            handler = HANDLERS[name]
        except (ValueError, KeyError, TypeError):
            ACTIONS_TOTAL.labels(action="unknown", status="error").inc()
            log.error("Unknown or malformed message: %r", body[:200])
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        context = extract(properties.headers or {})
        with tracer.start_as_current_span(name, context=context, kind=SpanKind.CONSUMER):
            try:
                with ACTION_DURATION.labels(action=name).time():
                    result = handler(cur, message.get("payload", {}))
                    conn.commit()
                ACTIONS_TOTAL.labels(action=name, status="success").inc()
                log.info("%s: %s", name, result)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                conn.rollback()
                ACTIONS_TOTAL.labels(action=name, status="error").inc()
                log.error("DB error in %s: %s", name, e)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
    log.info("Consumer started, waiting for messages")
    channel.start_consuming()


if __name__ == "__main__":
    main()