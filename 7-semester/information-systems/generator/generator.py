import json
import logging
import os
import random
import time

import pika
import psycopg2
from dotenv import load_dotenv
from faker import Faker
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.propagate import inject
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter, Histogram, start_http_server

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


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
log = logging.getLogger("generator")
fake = Faker()

DELAY_MIN = float(os.getenv("GENERATOR_DELAY_MIN", "0.2"))
DELAY_MAX = float(os.getenv("GENERATOR_DELAY_MAX", "2"))
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))
OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "http://localhost:4318/v1/traces")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
QUEUE_NAME = "orders"

ACTIONS_TOTAL = Counter(
    "generator_actions_total",
    "Number of generator actions executed",
    ["action", "status"],
)
ACTION_DURATION = Histogram(
    "generator_action_duration_seconds",
    "Duration of generator actions",
    ["action"],
)


def setup_tracing():
    provider = TracerProvider(
        resource=Resource.create({"service.name": "shop-generator"})
    )
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT))
    )
    trace.set_tracer_provider(provider)
    Psycopg2Instrumentor().instrument()


setup_tracing()
tracer = trace.get_tracer("generator")


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


_rabbit = {"conn": None, "channel": None}


def get_channel():
    conn, channel = _rabbit["conn"], _rabbit["channel"]
    if conn is None or conn.is_closed or channel is None or channel.is_closed:
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
                heartbeat=0,
            )
        )
        channel = conn.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        _rabbit["conn"], _rabbit["channel"] = conn, channel
    return channel


def publish(event_type, payload):
    headers = {}
    inject(headers)  # передаємо контекст трейса разом з повідомленням
    get_channel().basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps({"type": event_type, "payload": payload}),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json",
            headers=headers,
        ),
    )
    log.info("Published %s", event_type)


def init_schema(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT now()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            price NUMERIC(10, 2) NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            customer_id INT NOT NULL REFERENCES customers(id),
            amount NUMERIC(10, 2) NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'new',
            created_at TIMESTAMP DEFAULT now()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
            product_id INT NOT NULL REFERENCES products(id),
            quantity INT NOT NULL,
            price NUMERIC(10, 2) NOT NULL
        )
    """)


def seed_products(cur, count=30):
    cur.execute("SELECT count(*) FROM products")
    if cur.fetchone()[0] > 0:
        return
    for _ in range(count):
        cur.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s)",
            (fake.word().capitalize(), round(random.uniform(3, 300), 2)),
        )
    log.info("Seeded %s products", count)


STATUSES = ["paid", "shipped", "delivered", "cancelled"]


# --- записи: лише публікуємо подію, у базу пише consumer ---

def create_customer(cur):
    publish("create_customer", {"name": fake.name(), "email": fake.unique.email()})


def create_order(cur):
    publish("create_order", {"items": random.randint(1, 4)})


def update_order_status(cur):
    publish("update_order_status", {"status": random.choice(STATUSES)})


def update_customer_email(cur):
    publish("update_customer_email", {"email": fake.unique.email()})


def delete_old_cancelled_orders(cur):
    publish("delete_old_cancelled_orders", {})


# --- читання: потрібна відповідь одразу, тому напряму в базу ---

def report_top_products(cur):
    cur.execute(
        """SELECT p.name, sum(oi.quantity) AS sold, sum(oi.quantity * oi.price) AS revenue
           FROM order_items oi
           JOIN products p ON p.id = oi.product_id
           GROUP BY p.name
           ORDER BY revenue DESC
           LIMIT 5"""
    )
    log.info("Top products: %s", cur.fetchall())


def read_stats(cur):
    cur.execute("SELECT status, count(*), sum(amount) FROM orders GROUP BY status")
    log.info("Orders by status: %s", cur.fetchall())


def main():
    conn = get_connection()
    cur = conn.cursor()
    init_schema(cur)
    seed_products(cur)
    conn.commit()

    start_http_server(METRICS_PORT)
    log.info("Generator started, metrics on port %s", METRICS_PORT)

    actions = [
        (create_customer, 2),
        (create_order, 5),
        (update_order_status, 3),
        (update_customer_email, 1),
        (delete_old_cancelled_orders, 1),
        (report_top_products, 1),
        (read_stats, 1),
    ]
    functions = [f for f, _ in actions]
    weights = [w for _, w in actions]

    while True:
        action = random.choices(functions, weights=weights)[0]
        name = action.__name__
        with tracer.start_as_current_span(name):
            try:
                with ACTION_DURATION.labels(action=name).time():
                    action(cur)
                    conn.commit()
                ACTIONS_TOTAL.labels(action=name, status="success").inc()
            except Exception as e:
                conn.rollback()
                ACTIONS_TOTAL.labels(action=name, status="error").inc()
                log.error("Error in %s: %s", name, e)
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))


if __name__ == "__main__":
    main()