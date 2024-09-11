-- SQL Code to build the database architecture for this project.

CREATE SCHEMA staging
CREATE SCHEMA analytics

USE STORE;

-- Staging table for raw data
IF OBJECT_ID('staging.transactions', 'U') IS NOT NULL
    DROP TABLE staging.transactions;

CREATE TABLE staging.transactions (
    transaction_id NVARCHAR(50) NOT NULL,
    transaction_date INT NOT NULL,
    store_id INT NOT NULL,
    product_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    customer_id INT NOT NULL,
    customer_name NVARCHAR(50),
    customer_email NVARCHAR(50),
    customer_address NVARCHAR(100),
    customer_phone NVARCHAR(50),
    customer_card_number BIGINT,
    CONSTRAINT PK_transactions PRIMARY KEY (transaction_id, product_id)
);

-- Dimension table for customers 
CREATE TABLE analytics.customers_dim 
customer_id INT PRIMARY KEY,
first_name NVARCHAR(40), last_name NVARCHAR(40),
email NVARCHAR(255),
address NVARCHAR(255), phone
NVARCHAR(25),
extension NVARCHAR(10), 
ard_number NVARCHAR(50) ;

-- Dimension table for products 
CREATE TABLE analytics.products_dim 
product_id NVARCHAR(50) PRIMARY KEY, 
product_name NVARCHAR(MAX),
product_brand NVARCHAR(100),
gender NVARCHAR(20),
price DECIMAL(10, 2),
manufacturing_cost DECIMAL(10, 2),
primary_colour NVARCHAR(50) );

-- Date table
CREATE TABLE analytics.date_dim (
    date_id BIGINT PRIMARY KEY NOT NULL,
    calendar_date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    monthname NVARCHAR(16) NOT NULL,
    day INT NOT NULL,
    dayname NVARCHAR(16) NOT NULL,
    day_of_week INT NOT NULL,
    week_of_year INT NOT NULL,
    is_weekday BIT NOT NULL,
    is_weekend BIT NOT NULL,
    is_holiday BIT DEFAULT 0
);

-- Populate date tables
DECLARE @StartDate DATE = '2023-01-01';
DECLARE @EndDate DATE = '2024-12-31';

WITH DateRange AS (
    SELECT @StartDate AS calendar_date
    UNION ALL
    SELECT DATEADD(DAY, 1, calendar_date)
    FROM DateRange
    WHERE calendar_date < @EndDate
)
INSERT INTO analytics.date_dim (date_id, calendar_date, year, month, monthname, day, dayname, day_of_week, week_of_year, is_weekday, is_weekend)
SELECT
    CAST(FORMAT(calendar_date, 'yyyyMMdd') AS BIGINT) AS date_id,
    calendar_date,
    YEAR(calendar_date) AS year,
    MONTH(calendar_date) AS month,
    DATENAME(MONTH, calendar_date) AS monthname,
    DAY(calendar_date) AS day,
    DATENAME(WEEKDAY, calendar_date) AS dayname,
    DATEPART(WEEKDAY, calendar_date) AS day_of_week,
    DATEPART(WEEK, calendar_date) AS week_of_year,
    CASE WHEN DATEPART(WEEKDAY, calendar_date) IN (1, 7) THEN 0 ELSE 1 END AS is_weekday,
    CASE WHEN DATEPART(WEEKDAY, calendar_date) IN (1, 7) THEN 1 ELSE 0 END AS is_weekend
FROM DateRange
OPTION (MAXRECURSION 0);

-- Fact table for transactions
CREATE TABLE analytics.transactions_fact (
transaction_item_id INT IDENTITY(1,1) PRIMARY KEY, 
transaction_id NVARCHAR(50),
customer_id INT, store_id INT,
transaction_date BIGINT NOT NULL,
Product_id INT,
item_price DECIMAL(10, 2) ;

ALTER TABLE analytics.transactions_fact
ADD CONSTRAINT FK_transactions_fact_date
FOREIGN KEY (transaction_date) REFERENCES analytics.date_dim(date_id);

ALTER TABLE analytics.transactions_fact
ADD CONSTRAINT FK_transactions_fact_customer
FOREIGN KEY (customer_id) REFERENCES analytics.customers_dim(customer_id);

ALTER TABLE analytics.transactions_fact
ADD CONSTRAINT FK_transactions_fact_product_id
FOREIGN KEY (product_id) REFERENCES analytics.products_dim(product_id);
