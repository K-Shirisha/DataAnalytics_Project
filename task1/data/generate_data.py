"""
Script to generate a realistic Superstore-like sales dataset.
Run once to create sales_data.csv in the same folder.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# ── Reference data ───────────────────────────────────────────────────────────
products = {
    "Technology": [
        ("Apple MacBook Pro", 1200, 250),
        ("Dell XPS 15", 950, 180),
        ("HP LaserJet Printer", 300, 50),
        ("Canon DSLR Camera", 650, 120),
        ("Samsung Galaxy Tab", 450, 80),
        ("Logitech Wireless Mouse", 35, 10),
        ("SanDisk SSD 1TB", 90, 20),
        ("Sony Headphones", 150, 35),
    ],
    "Furniture": [
        ("Herman Miller Chair", 800, 120),
        ("IKEA Standing Desk", 350, 40),
        ("Wooden Bookshelf", 220, 30),
        ("Leather Sofa", 1100, 200),
        ("Glass Coffee Table", 280, 45),
        ("Filing Cabinet", 180, 25),
    ],
    "Office Supplies": [
        ("Stapler Set", 15, 5),
        ("A4 Paper Ream", 8, 2),
        ("Whiteboard Markers", 12, 4),
        ("Sticky Notes Pack", 10, 3),
        ("Pen Set", 20, 6),
        ("Binder Clips Box", 7, 2),
        ("Highlighter Pack", 14, 4),
    ],
}

regions = ["East", "West", "South", "Central"]
region_multipliers = {"East": 1.2, "West": 1.1, "South": 0.9, "Central": 1.0}

# ── Generate rows ─────────────────────────────────────────────────────────────
rows = []
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)

for _ in range(2000):
    category = random.choice(list(products.keys()))
    product_name, base_price, base_profit = random.choice(products[category])
    region = random.choice(regions)
    multiplier = region_multipliers[region]

    quantity = random.randint(1, 10)
    noise = np.random.uniform(0.85, 1.15)
    sales = round(base_price * quantity * multiplier * noise, 2)
    profit = round(base_profit * quantity * multiplier * noise * np.random.uniform(0.6, 1.2), 2)

    # Occasionally make some rows loss-making (Office Supplies mostly)
    if category == "Office Supplies" and random.random() < 0.15:
        profit = round(-abs(profit) * 0.3, 2)

    order_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )

    rows.append(
        {
            "Order ID": f"ORD-{random.randint(10000, 99999)}",
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Product Name": product_name,
            "Category": category,
            "Region": region,
            "Sales": sales,
            "Profit": profit,
            "Quantity": quantity,
        }
    )

df = pd.DataFrame(rows)
df = df.sort_values("Order Date").reset_index(drop=True)

output_path = "sales_data.csv"
df.to_csv(output_path, index=False)
print(f"Dataset saved → {output_path}  ({len(df)} rows)")
