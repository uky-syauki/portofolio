"""SQLite helpers for the Aurora app.

Provides:
- get_db(): request-scoped connection (Row access enabled, foreign keys on)
- close_db(): teardown hook registered on the app
- init_db(): create schema and seed sample products (idempotent)

Usage from code:
    from db import get_db, init_db
"""
import sqlite3
from pathlib import Path

from flask import current_app, g

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "products.db"

PRODUCTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT    NOT NULL,
    category TEXT    NOT NULL,
    price    REAL    NOT NULL,
    rating   REAL    NOT NULL,
    emoji    TEXT    NOT NULL DEFAULT ''
)
"""

SEED_PRODUCTS = [
    ("Aurora Desk Lamp", "Lighting", 49.0, 4.8, "💡"),
    ("Nimbus Wireless Mouse", "Accessories", 29.5, 4.6, "🖱️"),
    ("Zen Minimal Headset", "Audio", 89.9, 4.9, "🎧"),
    ("Terra Indoor Plant", "Home", 24.0, 4.3, "🪴"),
    ("Pulse Smart Water Bottle", "Gadgets", 35.0, 4.5, "🍶"),
    ("Drift Mechanical Keyboard", "Accessories", 119.0, 4.7, "⌨️"),
    ("Halo Ring Light", "Lighting", 42.0, 4.4, "⭕"),
    ("Cove Bluetooth Speaker", "Audio", 65.0, 4.6, "🔊"),
]


def get_db():
    """Return the request-scoped SQLite connection."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None):
    """Close the request-scoped connection, if any."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app=None):
    """Create the schema and seed sample data (idempotent)."""
    target = app or current_app
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(PRODUCTS_SCHEMA)
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO products (name, category, price, rating, emoji)"
                " VALUES (?, ?, ?, ?, ?)",
                SEED_PRODUCTS,
            )
            conn.commit()
    finally:
        conn.close()
    if app is not None:
        app.teardown_appcontext(close_db)


def query_products(category=None):
    """Fetch products, optionally filtered by category (case-insensitive)."""
    db = get_db()
    if category:
        rows = db.execute(
            "SELECT * FROM products WHERE category = ? COLLATE NOCASE ORDER BY id",
            (category,),
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM products ORDER BY id").fetchall()
    return [dict(row) for row in rows]
