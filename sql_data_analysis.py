"""
SQL Data Analysis Project: Analyzing Customer Behavior in an Online Store
--------------------------------------------------------------------------
Project Overview:
• Data Source: Synthetic data created in a SQLite database.
• Tables: Customers, Products, Orders, OrderItems.
• Methods:
    - Create and populate the database with synthetic customers, products, orders, and order items.
    - Execute advanced SQL queries:
         1. Top 10 Customers by Total Spending.
         2. Monthly Sales Trend.
         3. Best-selling Products by Quantity.
         4. Customer Segmentation (using a window function to rank by average order value).
    - Use pandas to load query results and generate plots.
    - Save plots as downloadable PNG images in the "sql_analysis_images" folder.
• Tools: Python (sqlite3, Pandas, NumPy, Matplotlib, Seaborn)
• How to Run:
    1. Install required packages:
         pip install pandas numpy matplotlib seaborn
    2. Run the script:
         python sql_data_analysis.py
    3. Check the "sql_analysis_images" folder for generated images and the "online_store.db" file.
"""

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime

# ---------------------------
# Setup: Create output folder for images
# ---------------------------
OUTPUT_DIR = "sql_analysis_images"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created output directory: {OUTPUT_DIR}")

# ---------------------------
# Setup: Connect to SQLite database (or create it)
# ---------------------------
DB_FILE = "online_store.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Drop tables if they exist to start fresh
tables = ["OrderItems", "Orders", "Products", "Customers"]
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# ---------------------------
# Create Tables
# ---------------------------
cursor.execute("""
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    registration_date DATE
)
""")

cursor.execute("""
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE OrderItems (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
)
""")
conn.commit()

# ---------------------------
# Insert Synthetic Data
# ---------------------------

# Insert Customers
num_customers = 200
customers = []
for i in range(1, num_customers+1):
    name = f"Customer {i}"
    email = f"customer{i}@example.com"
    reg_date = (datetime.date(2021,1,1) + datetime.timedelta(days=np.random.randint(0, 730))).isoformat()
    customers.append((i, name, email, reg_date))
cursor.executemany("INSERT INTO Customers (customer_id, name, email, registration_date) VALUES (?, ?, ?, ?)", customers)

# Insert Products
products = [
    (1, "Smartphone", "Electronics", 699.99),
    (2, "Laptop", "Electronics", 1199.99),
    (3, "Tablet", "Electronics", 499.99),
    (4, "Headphones", "Electronics", 199.99),
    (5, "Jeans", "Fashion", 49.99),
    (6, "T-Shirt", "Fashion", 19.99),
    (7, "Sneakers", "Fashion", 89.99),
    (8, "Coffee Maker", "Home & Kitchen", 79.99),
    (9, "Blender", "Home & Kitchen", 59.99),
    (10, "Book", "Books", 14.99)
]
cursor.executemany("INSERT INTO Products (product_id, name, category, price) VALUES (?, ?, ?, ?)", products)

# Insert Orders and OrderItems
num_orders = 1000
orders = []
order_items = []
order_id = 1
for i in range(num_orders):
    customer_id = np.random.randint(1, num_customers+1)
    order_date = (datetime.date(2021,1,1) + datetime.timedelta(days=np.random.randint(0, 730))).isoformat()
    # Each order has between 1 and 5 items
    num_items = np.random.randint(1,6)
    total_amount = 0.0
    items = []
    for j in range(num_items):
        prod = products[np.random.randint(0, len(products))]
        product_id, prod_name, category, price = prod
        quantity = np.random.randint(1,4)
        total_amount += price * quantity
        items.append((order_id, product_id, quantity, price))
    orders.append((order_id, customer_id, order_date, round(total_amount,2)))
    order_items.extend(items)
    order_id += 1

cursor.executemany("INSERT INTO Orders (order_id, customer_id, order_date, total_amount) VALUES (?, ?, ?, ?)", orders)
cursor.executemany("INSERT INTO OrderItems (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)", order_items)
conn.commit()

# ---------------------------
# Advanced SQL Queries
# ---------------------------

# Query 1: Top 10 Customers by Total Spending
query_top_customers = """
WITH CustomerSpending AS (
    SELECT c.customer_id, c.name, SUM(o.total_amount) AS total_spent
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)
SELECT * FROM CustomerSpending
ORDER BY total_spent DESC
LIMIT 10;
"""
df_top_customers = pd.read_sql_query(query_top_customers, conn)
print("Top 10 Customers by Total Spending:")
print(df_top_customers)

# Query 2: Monthly Sales Trend
query_monthly_sales = """
SELECT strftime('%Y-%m', order_date) AS order_month, SUM(total_amount) AS monthly_sales
FROM Orders
GROUP BY order_month
ORDER BY order_month;
"""
df_monthly_sales = pd.read_sql_query(query_monthly_sales, conn)
print("Monthly Sales Trend:")
print(df_monthly_sales)

# Query 3: Best-selling Products by Quantity
query_best_products = """
SELECT p.name, p.category, SUM(oi.quantity) AS total_quantity
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY p.name, p.category
ORDER BY total_quantity DESC
LIMIT 10;
"""
df_best_products = pd.read_sql_query(query_best_products, conn)
print("Best-selling Products:")
print(df_best_products)

# Query 4: Customer Segmentation by Average Order Value (with ranking)
query_customer_segmentation = """
WITH CustomerOrders AS (
    SELECT c.customer_id, c.name, AVG(o.total_amount) AS avg_order_value
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)
SELECT customer_id, name, avg_order_value,
       RANK() OVER (ORDER BY avg_order_value DESC) AS spending_rank
FROM CustomerOrders
ORDER BY spending_rank
LIMIT 10;
"""
df_customer_segmentation = pd.read_sql_query(query_customer_segmentation, conn)
print("Top 10 Customers by Average Order Value:")
print(df_customer_segmentation)

# ---------------------------
# Visualization & Export Images
# ---------------------------

# Plot 1: Monthly Sales Trend (Line Plot)
plt.figure(figsize=(10,6))
plt.plot(df_monthly_sales['order_month'], df_monthly_sales['monthly_sales'], marker='o', color='teal')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=45)
plt.tight_layout()
monthly_sales_image = os.path.join(OUTPUT_DIR, "monthly_sales_trend.png")
plt.savefig(monthly_sales_image)
plt.close()
print(f"Saved plot: {monthly_sales_image}")

# Plot 2: Best-selling Products (Bar Plot)
plt.figure(figsize=(10,6))
sns.barplot(x='total_quantity', y='name', data=df_best_products, palette="viridis")
plt.title("Best-selling Products by Quantity")
plt.xlabel("Total Quantity Sold")
plt.ylabel("Product")
plt.tight_layout()
best_products_image = os.path.join(OUTPUT_DIR, "best_selling_products.png")
plt.savefig(best_products_image)
plt.close()
print(f"Saved plot: {best_products_image}")

# Plot 3: Top 10 Customers by Total Spending (Bar Plot)
plt.figure(figsize=(10,6))
sns.barplot(x='total_spent', y='name', data=df_top_customers, palette="rocket")
plt.title("Top 10 Customers by Total Spending")
plt.xlabel("Total Spent ($)")
plt.ylabel("Customer")
plt.tight_layout()
top_customers_image = os.path.join(OUTPUT_DIR, "top_customers_spending.png")
plt.savefig(top_customers_image)
plt.close()
print(f"Saved plot: {top_customers_image}")

# Plot 4: Customer Segmentation by Average Order Value (Bar Plot)
plt.figure(figsize=(10,6))
sns.barplot(x='avg_order_value', y='name', data=df_customer_segmentation, palette="mako")
plt.title("Top 10 Customers by Average Order Value")
plt.xlabel("Average Order Value ($)")
plt.ylabel("Customer")
plt.tight_layout()
customer_segmentation_image = os.path.join(OUTPUT_DIR, "customer_segmentation.png")
plt.savefig(customer_segmentation_image)
plt.close()
print(f"Saved plot: {customer_segmentation_image}")

# Close the SQLite connection
conn.close()

print("SQL Data Analysis Project completed.")
print(f"Database file: {DB_FILE}")
print(f"Check the '{OUTPUT_DIR}' folder for downloadable images.")
