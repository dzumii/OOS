import sqlite3
import datetime

DB_PATH = "data.db"


def create_db(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            customer_id TEXT,
            product_id TEXT,
            variant TEXT,
            quantity INTEGER
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY,
            customer_id TEXT,
            product_id TEXT,
            variant TEXT,
            ts TEXT,
            quantity INTEGER
        )
        """
    )

    conn.commit()

    # Clear existing seed data (safe for prototype)
    cur.execute("DELETE FROM inventory")
    cur.execute("DELETE FROM purchases")

    # Seed sample inventory rows
    inv = [
        ("cust_1", "prod_a", "red", 0),
        ("cust_1", "prod_b", "small", 5),
        ("cust_2", "prod_a", "red", 10),
        ("cust_2", "prod_a", "blue", 3),
        ("cust_1", "prod_b", "large", 0),
    ]

    for cid, pid, var, q in inv:
        cur.execute(
            "INSERT INTO inventory (customer_id, product_id, variant, quantity) VALUES (?,?,?,?)",
            (cid, pid, var, q),
        )

    now = datetime.datetime.utcnow()
    older = (now - datetime.timedelta(days=30)).isoformat()
    recent = (now - datetime.timedelta(days=3)).isoformat()

    purchases = [
        ("cust_1", "prod_a", "red", older, 1),
        ("cust_2", "prod_a", "blue", recent, 2),
    ]

    for cid, pid, var, ts, q in purchases:
        cur.execute(
            "INSERT INTO purchases (customer_id, product_id, variant, ts, quantity) VALUES (?,?,?,?,?)",
            (cid, pid, var, ts, q),
        )

    conn.commit()
    conn.close()
    print(f"Initialized {db_path} with sample data")


if __name__ == "__main__":
    create_db()
