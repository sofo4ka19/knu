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
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    conn.autocommit = True
    return conn


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
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES customers(id),
            amount NUMERIC(10, 2) NOT NULL,
            status TEXT NOT NULL DEFAULT 'new',
            created_at TIMESTAMP DEFAULT now()
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
    row = cur.fetchone()
    if row is None:
        log.warning("No customers yet, skipping order")
        return
    amount = round(random.uniform(5, 500), 2)
    cur.execute(
        "INSERT INTO orders (customer_id, amount) VALUES (%s, %s) RETURNING id",
        (row[0], amount),
    )
    log.info("Created order #%s for customer #%s, amount %s",
             cur.fetchone()[0], row[0], amount)


def main():
    conn = get_connection()
    cur = conn.cursor()
    init_schema(cur)
    log.info("Generator started")
    while True:
        try:
            action = random.choice([create_customer, create_order, create_order])
            action(cur)
        except Exception as e:
            log.error("DB error: %s", e)
        time.sleep(random.uniform(0.2, 2))


if __name__ == "__main__":
    main()