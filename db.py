import sqlite3

def connect(db_path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def get_or_create_product(conn: sqlite3.Connection, url: str, name: str) -> int:
    cursor = conn.execute("SELECT id FROM products WHERE url = ?", (url,))
    row = cursor.fetchone()
    if row:
        return row["id"]
    
    cursor = conn.execute("INSERT INTO products (url, name) VALUES (?, ?)", (url, name))
    conn.commit()
    return cursor.lastrowid

def save_and_compare_price(conn: sqlite3.Connection, product_id: int, new_price: float) -> float | None:
    # Fetch previous price before inserting the new record to compare them later.
    cursor = conn.execute(
        "SELECT price FROM price_history WHERE product_id = ? ORDER BY scraped_at DESC LIMIT 1",
        (product_id,)
    )
    row = cursor.fetchone()
    previous_price = row["price"] if row else None

    conn.execute(
        "INSERT INTO price_history (product_id, price) VALUES (?, ?)",
        (product_id, new_price)
    )
    conn.commit()
    return previous_price