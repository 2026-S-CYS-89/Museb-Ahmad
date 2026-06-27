"""
retail_db.py
============
Single-file SQLite database for Retail Management System.
DB file: retail_store.db (created automatically on first run)

Tables:
  - products  : product catalog + stock
  - customers : customer records
  - sales     : each sale transaction
  - sale_items: individual items inside a sale
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "retail_store.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db():
    """Create all tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            category    TEXT    NOT NULL,
            price       REAL    NOT NULL,
            stock       INTEGER NOT NULL DEFAULT 0,
            created_at  TEXT    NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            phone       TEXT,
            email       TEXT,
            created_at  TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id  INTEGER REFERENCES customers(id),
            customer_name TEXT,
            total_amount REAL    NOT NULL,
            sale_date    TEXT    NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id     INTEGER NOT NULL REFERENCES sales(id),
            product_id  INTEGER NOT NULL REFERENCES products(id),
            product_name TEXT   NOT NULL,
            quantity    INTEGER NOT NULL,
            unit_price  REAL    NOT NULL,
            subtotal    REAL    NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ── PRODUCTS ──────────────────────────────────────────────────

def add_product(name, category, price, stock):
    conn = get_connection()
    conn.execute(
        "INSERT INTO products (name, category, price, stock, created_at) VALUES (?,?,?,?,?)",
        (name.strip(), category.strip(), float(price), int(stock), now())
    )
    conn.commit()
    conn.close()


def get_all_products():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM products ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_product(product_id, name, category, price, stock):
    conn = get_connection()
    conn.execute(
        "UPDATE products SET name=?, category=?, price=?, stock=? WHERE id=?",
        (name.strip(), category.strip(), float(price), int(stock), product_id)
    )
    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


def update_stock(product_id, quantity_sold):
    conn = get_connection()
    conn.execute(
        "UPDATE products SET stock = stock - ? WHERE id=?",
        (quantity_sold, product_id)
    )
    conn.commit()
    conn.close()


def get_low_stock_products(threshold=5):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM products WHERE stock <= ? ORDER BY stock", (threshold,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── CUSTOMERS ─────────────────────────────────────────────────

def add_customer(name, phone, email):
    conn = get_connection()
    conn.execute(
        "INSERT INTO customers (name, phone, email, created_at) VALUES (?,?,?,?)",
        (name.strip(), phone.strip(), email.strip(), now())
    )
    conn.commit()
    conn.close()


def get_all_customers():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM customers ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_customer(customer_id):
    conn = get_connection()
    conn.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()
    conn.close()


# ── SALES ─────────────────────────────────────────────────────

def create_sale(customer_name, items):
    """
    items = list of dicts:
      { product_id, product_name, quantity, unit_price, subtotal }
    Returns the new sale id.
    """
    total = sum(i["subtotal"] for i in items)
    conn  = get_connection()
    cur   = conn.cursor()
    cur.execute(
        "INSERT INTO sales (customer_name, total_amount, sale_date) VALUES (?,?,?)",
        (customer_name.strip(), total, now())
    )
    sale_id = cur.lastrowid
    for item in items:
        cur.execute(
            """INSERT INTO sale_items
               (sale_id, product_id, product_name, quantity, unit_price, subtotal)
               VALUES (?,?,?,?,?,?)""",
            (sale_id, item["product_id"], item["product_name"],
             item["quantity"], item["unit_price"], item["subtotal"])
        )
        # Deduct stock
        cur.execute(
            "UPDATE products SET stock = stock - ? WHERE id=?",
            (item["quantity"], item["product_id"])
        )
    conn.commit()
    conn.close()
    return sale_id


def get_all_sales():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM sales ORDER BY sale_date DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_sale_items(sale_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM sale_items WHERE sale_id=?", (sale_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_total_revenue():
    conn = get_connection()
    row = conn.execute("SELECT SUM(total_amount) as total FROM sales").fetchone()
    conn.close()
    return row["total"] or 0.0


def get_db_path():
    return DB_PATH
