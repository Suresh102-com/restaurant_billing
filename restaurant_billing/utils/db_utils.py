import sqlite3
import pandas as pd
import os
import json

DB_FILE = "db/restaurant.db"
SAMPLE_JSON = "data/sample_bills.json"
SALES_REPORT = "data/sales_report.csv"

def init_db():
    os.makedirs("db", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mode TEXT,
        customer_name TEXT,
        table_no TEXT,
        items TEXT,
        total REAL,
        payment_method TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_order(mode, customer_name, table_no, items, total, payment_method):
    # --- Save to SQLite ---
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO orders (mode, customer_name, table_no, items, total, payment_method)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (mode, customer_name, table_no, items, total, payment_method))
    conn.commit()
    conn.close()

    # --- Save to JSON (append mode, safe) ---
    order = {
        "mode": mode,
        "customer_name": customer_name,
        "table_no": table_no,
        "items": items,
        "total": total,
        "payment_method": payment_method
    }

    data = []
    if os.path.exists(SAMPLE_JSON):
        try:
            with open(SAMPLE_JSON, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:  # only parse if not empty
                    data = json.loads(content)
        except json.JSONDecodeError:
            # if file is corrupted, reset it
            data = []

    data.append(order)

    with open(SAMPLE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # --- Save to CSV (sales report) ---
    row = pd.DataFrame([order])
    if os.path.exists(SALES_REPORT):
        row.to_csv(SALES_REPORT, mode="a", header=False, index=False)
    else:
        row.to_csv(SALES_REPORT, mode="w", header=True, index=False)