create DATABASE business_intelligence_db;
use business_intelligence_db;

CREATE TABLE sales_reps (
    rep_id INT AUTO_INCREMENT PRIMARY KEY,
    rep_name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    signup_date DATE
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    rep_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

SELECT COUNT(*) AS customers FROM customers;
SELECT COUNT(*) AS products FROM products;
SELECT COUNT(*) AS orders FROM orders;
SELECT COUNT(*) AS order_items FROM order_items;

-- Total Revenue
SELECT 
    SUM(quantity * price) AS total_revenue
FROM order_items;

-- Revenue by Month
SELECT 
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(oi.quantity * oi.price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

-- 5 Products by Revenue
SELECT 
    p.product_name,
    SUM(oi.quantity * oi.price) AS revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 5;

-- Best sales Reps
SELECT 
    s.rep_name,
    SUM(oi.quantity * oi.price) AS revenue
FROM sales_reps s
JOIN orders o ON s.rep_id = o.rep_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY s.rep_name
ORDER BY revenue DESC;

-- Create Views
CREATE VIEW sales_summary AS
SELECT 
    o.order_id,
    o.order_date,
    c.customer_name,
    s.rep_name,
    p.product_name,
    p.category,
    oi.quantity,
    oi.price,
    (oi.quantity * oi.price) AS revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN sales_reps s ON o.rep_id = s.rep_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
