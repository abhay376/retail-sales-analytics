import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sqlite3

def generate_retail_dataset():
    np.random.seed(42)
    num_records = 3000

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 9, 30)
    date_range = (end_date - start_date).days

    random_days = np.random.randint(0, date_range, num_records)
    dates = [start_date + timedelta(days=int(d)) for d in random_days]
    dates.sort()

    customers = [f"CUST-{np.random.randint(100, 600)}" for _ in range(num_records)]
    genders = np.random.choice(["Female", "Male", "Other"], size=num_records, p=[0.52, 0.44, 0.04])
    ages = np.random.randint(18, 68, num_records)

    categories_products = {
        "Electronics": [
            ("Wireless Headphones", 89.99),
            ("Smart Watch", 199.99),
            ("Bluetooth Speaker", 49.99),
            ("Tablet 10-inch", 299.99),
            ("USB-C Hub", 29.99)
        ],
        "Clothing": [
            ("Denim Jacket", 65.00),
            ("Cotton T-Shirt", 22.50),
            ("Running Shoes", 110.00),
            ("Formal Trousers", 55.00),
            ("Winter Coat", 140.00)
        ],
        "Beauty": [
            ("Hydrating Skincare Set", 45.00),
            ("Matte Lipstick Set", 28.00),
            ("Sunscreen SPF 50", 18.50),
            ("Perfume Spray 100ml", 75.00),
            ("Hair Dryer Pro", 85.00)
        ],
        "Home & Kitchen": [
            ("Smoothie Blender", 59.99),
            ("Drip Coffee Maker", 79.99),
            ("Stainless Steel Cookware Set", 129.99),
            ("Air Purifier", 149.99),
            ("Robot Vacuum", 249.99)
        ],
        "Books": [
            ("Data Analytics Handbook", 35.00),
            ("Sci-Fi Bestseller Novel", 15.99),
            ("Personal Finance Blueprint", 22.00),
            ("Cookbook 101 Recipes", 27.50),
            ("Mindfulness & Productivity", 18.00)
        ]
    }

    category_list = list(categories_products.keys())
    selected_categories = np.random.choice(category_list, size=num_records, p=[0.25, 0.25, 0.20, 0.18, 0.12])

    product_names = []
    prices = []

    for cat in selected_categories:
        prod_tuple = categories_products[cat][np.random.randint(0, len(categories_products[cat]))]
        product_names.append(prod_tuple[0])
        # add slight price variation/discount
        variation = round(np.random.uniform(0.9, 1.1), 2)
        prices.append(round(prod_tuple[1] * variation, 2))

    quantities = np.random.choice([1, 2, 3, 4, 5], size=num_records, p=[0.55, 0.25, 0.12, 0.05, 0.03])
    total_amounts = [round(q * p, 2) for q, p in zip(quantities, prices)]

    payment_methods = np.random.choice(["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"], size=num_records, p=[0.40, 0.30, 0.15, 0.10, 0.05])
    locations = np.random.choice(["North", "South", "East", "West", "Central"], size=num_records, p=[0.25, 0.25, 0.20, 0.15, 0.15])

    df = pd.DataFrame({
        "Transaction_ID": [f"TXN{10001 + i}" for i in range(num_records)],
        "Date": [d.strftime("%Y-%m-%d") for d in dates],
        "Customer_ID": customers,
        "Gender": genders,
        "Age": ages,
        "Product_Category": selected_categories,
        "Product_Name": product_names,
        "Quantity": quantities,
        "Price_Per_Unit": prices,
        "Total_Amount": total_amounts,
        "Payment_Method": payment_methods,
        "Store_Location": locations
    })

    # Ensure target directory exists
    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("data", "retail_sales_raw.csv")
    df.to_csv(csv_path, index=False)
    print(f"Data successfully generated: {csv_path} with {len(df)} records.")

    # Populate SQLite database
    db_path = os.path.join("data", "retail_database.db")
    conn = sqlite3.connect(db_path)
    df.to_sql("retail_sales", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Database created and populated: {db_path}")

if __name__ == "__main__":
    generate_retail_dataset()
