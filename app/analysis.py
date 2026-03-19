import sqlite3
import datetime
from typing import Dict, Any, List

DB_PATH = "data.db"


def _rows_to_list(cur) -> List[Dict[str, Any]]:
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def analyze_customer(customer_id: str, db_path: str = DB_PATH) -> Dict[str, Any]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    result = {"customer_id": customer_id, "out_of_stock": [], "zero_purchases_2w": False, "portfolio_suggestions": []}

    # Check out-of-stock items for this customer
    cur.execute("SELECT product_id, variant, quantity FROM inventory WHERE customer_id = ? AND quantity <= 0", (customer_id,))
    oos = _rows_to_list(cur)
    result["out_of_stock"] = oos

    # Check purchases in the last 14 days
    now = datetime.datetime.utcnow()
    threshold = (now - datetime.timedelta(days=14)).isoformat()
    cur.execute("SELECT COUNT(1) as cnt FROM purchases WHERE customer_id = ? AND ts >= ?", (customer_id, threshold))
    cnt = cur.fetchone()[0]
    result["zero_purchases_2w"] = cnt == 0

    # Portfolio mix heuristic: compare variants purchased vs available
    # Variants purchased by customer (any time)
    cur.execute("SELECT DISTINCT product_id FROM purchases WHERE customer_id = ?", (customer_id,))
    products = [r[0] for r in cur.fetchall()]

    suggestions = []
    for prod in products:
        cur.execute("SELECT DISTINCT variant FROM inventory WHERE product_id = ?", (prod,))
        available = set([r[0] for r in cur.fetchall()])
        cur.execute("SELECT DISTINCT variant FROM purchases WHERE customer_id = ? AND product_id = ?", (customer_id, prod))
        owned = set([r[0] for r in cur.fetchall()])
        missing = sorted(list(available - owned))
        if missing:
            suggestions.append({"product_id": prod, "missing_variants": missing})

    result["portfolio_suggestions"] = suggestions

    conn.close()
    return result


if __name__ == "__main__":
    print(analyze_customer("cust_1"))
