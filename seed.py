import sqlite3
from pathlib import Path

from config import load_config

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

def seed(db_path: str) -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(schema)
        
        test_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        connection.execute(
            "INSERT OR IGNORE INTO products (url, name) VALUES (?, ?)",
            (test_url, "A Light in the Attic")
        )
        
        row = connection.execute(
            "SELECT id FROM products WHERE url = ?", (test_url,)
        ).fetchone()
        
        if row:
            product_id = row["id"] if isinstance(row, sqlite3.Row) else row[0]
            # Set a higher historical price to verify the drop-detection logic on first run.
            connection.execute(
                "INSERT INTO price_history (product_id, price) VALUES (?, ?)",
                (product_id, 55.00)
            )
        
        connection.commit()
        print(f"Database seeded at {db_path}")
    finally:
        connection.close()

if __name__ == "__main__":
    config = load_config()
    seed(config.db_path)