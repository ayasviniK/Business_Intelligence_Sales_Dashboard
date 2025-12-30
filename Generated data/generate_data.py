import random
from faker import Faker
import mysql.connector
from datetime import datetime, timedelta

# -----------------------------
# CONFIGURATION
# -----------------------------
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 100
NUM_REPS = 15
NUM_ORDERS = 20000
MAX_ITEMS_PER_ORDER = 4

fake = Faker()

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Ayazzvini1028",
    database="business_intelligence_db"
)
cursor = conn.cursor()

# -----------------------------
# STEP 1: SALES REPS
# -----------------------------
sales_reps = []
for _ in range(NUM_REPS):
    sales_reps.append((fake.name(), fake.email()))

cursor.executemany(
    "INSERT INTO sales_reps (rep_name, email) VALUES (%s, %s)",
    sales_reps
)
conn.commit()

cursor.execute("SELECT rep_id FROM sales_reps")
rep_ids = [r[0] for r in cursor.fetchall()]

print("Sales reps inserted")

# -----------------------------
# STEP 2: CUSTOMERS
# -----------------------------
customers = []
for _ in range(NUM_CUSTOMERS):
    customers.append((
        fake.name(),
        fake.city(),
        fake.country(),
        fake.date_between(start_date='-3y', end_date='today')
    ))

cursor.executemany(
    """INSERT INTO customers (customer_name, city, country, signup_date)
       VALUES (%s, %s, %s, %s)""",
    customers
)
conn.commit()

cursor.execute("SELECT customer_id FROM customers")
customer_ids = [c[0] for c in cursor.fetchall()]

print("Customers inserted")

# -----------------------------
# STEP 3: PRODUCTS
# -----------------------------
products = []
categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]

for _ in range(NUM_PRODUCTS):
    products.append((
        fake.word().capitalize(),
        random.choice(categories),
        round(random.uniform(10, 500), 2)
    ))

cursor.executemany(
    """INSERT INTO products (product_name, category, price)
       VALUES (%s, %s, %s)""",
    products
)
conn.commit()

cursor.execute("SELECT product_id, price FROM products")
product_data = cursor.fetchall()
product_price_map = {p[0]: p[1] for p in product_data}

print("Products inserted")

# -----------------------------
# STEP 4: ORDERS
# -----------------------------
orders = []
start_date = datetime.now() - timedelta(days=730)

for _ in range(NUM_ORDERS):
    orders.append((
        random.choice(customer_ids),
        random.choice(rep_ids),
        start_date + timedelta(days=random.randint(0, 730))
    ))

cursor.executemany(
    """INSERT INTO orders (customer_id, rep_id, order_date)
       VALUES (%s, %s, %s)""",
    orders
)
conn.commit()

cursor.execute("SELECT order_id FROM orders")
order_ids = [o[0] for o in cursor.fetchall()]

print("Orders inserted")

# -----------------------------
# STEP 5: ORDER ITEMS
# -----------------------------
order_items = []

for order_id in order_ids:
    for _ in range(random.randint(1, MAX_ITEMS_PER_ORDER)):
        product_id = random.choice(list(product_price_map.keys()))
        quantity = random.randint(1, 5)
        price = product_price_map[product_id]

        order_items.append((
            order_id,
            product_id,
            quantity,
            price
        ))

cursor.executemany(
    """INSERT INTO order_items (order_id, product_id, quantity, price)
       VALUES (%s, %s, %s, %s)""",
    order_items
)
conn.commit()

print("Order items inserted")

# -----------------------------
# CLEAN UP
# -----------------------------
cursor.close()
conn.close()

print("DATA GENERATION COMPLETE")
