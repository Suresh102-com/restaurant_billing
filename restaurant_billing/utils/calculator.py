import pandas as pd

def calc_order_total(order: dict) -> float:
    return sum(v["price"] * v["qty"] for v in order.values())

def order_to_df(order: dict) -> pd.DataFrame:
    rows = []
    for name, data in order.items():
        subtotal = data["price"] * data["qty"]
        rows.append({
            "Item": name,
            "Qty": data["qty"],
            "Price": data["price"],
            "Subtotal": subtotal
        })
    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["Item", "Qty", "Price", "Subtotal"])