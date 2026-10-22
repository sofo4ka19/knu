import os
import random
import time
import logging

import psycopg2
from dotenv import load_dotenv
from faker import Faker

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("generator")
fake = Faker()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


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


def create_customer(cur):
    cur.execute(
        "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING id",
        (fake.name(), fake.unique.email()),
    )
    customer_id = cur.fetchone()[0]
    log.info("Created customer #%s", customer_id)


def create_order(cur):
    cur.execute("SELECT id FROM customers ORDER BY random() LIMIT 1")
    customer = cur.fetchone()
    if customer is None:
        log.warning("No customers yet, skipping order")
        return

    cur.execute(
        "SELECT id, price FROM products ORDER BY random() LIMIT %s",
        (random.randint(1, 4),),
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
    log.info("Created order #%s for customer #%s: %s items, total %s",
             order_id, customer[0], len(products), total)

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


def update_order_status(cur):
    new_status = random.choice(STATUSES)
    cur.execute(
        """UPDATE orders SET status = %s
           WHERE id = (SELECT id FROM orders ORDER BY random() LIMIT 1)
           RETURNING id""",
        (new_status,),
    )
    row = cur.fetchone()
    if row:
        log.info("Order #%s status changed to %s", row[0], new_status)


def update_customer_email(cur):
    cur.execute(
        """UPDATE customers SET email = %s
           WHERE id = (SELECT id FROM customers ORDER BY random() LIMIT 1)
           RETURNING id""",
        (fake.unique.email(),),
    )
    row = cur.fetchone()
    if row:
        log.info("Customer #%s changed email", row[0])


def delete_old_cancelled_orders(cur):
    cur.execute(
        """DELETE FROM orders
           WHERE status = 'cancelled'
             AND created_at < now() - interval '2 minutes'"""
    )
    if cur.rowcount:
        log.info("Deleted %s old cancelled orders", cur.rowcount)


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
    log.info("Generator started")
    actions = [
        (create_customer, 3),
        (create_order, 7),
        (update_order_status, 6),
        (update_customer_email, 1),
        (delete_old_cancelled_orders, 2),
        (report_top_products, 1),
        (read_stats, 1),
    ]
    functions = [f for f, _ in actions]
    weights = [w for _, w in actions]
    while True:
        try:
            action = random.choices(functions, weights=weights)[0]
            action(cur)
            conn.commit()
        except Exception as e:
            conn.rollback()
            log.error("DB error: %s", e)
        time.sleep(random.uniform(0.2, 2))


if __name__ == "__main__":
    main()