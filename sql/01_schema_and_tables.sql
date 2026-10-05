-- =========================================================================
-- RETAIL SALES ANALYTICS DASHBOARD - DATABASE SCHEMA
-- Compatible with PostgreSQL, MySQL, and SQLite
-- =========================================================================

-- Drop table if already exists for fresh deployment
DROP TABLE IF EXISTS retail_sales;

CREATE TABLE retail_sales (
    Transaction_ID VARCHAR(20) PRIMARY KEY,
    Date DATE NOT NULL,
    Customer_ID VARCHAR(20) NOT NULL,
    Gender VARCHAR(10),
    Age INT,
    Product_Category VARCHAR(50) NOT NULL,
    Product_Name VARCHAR(100) NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    Price_Per_Unit DECIMAL(10, 2) NOT NULL,
    Total_Amount DECIMAL(10, 2) NOT NULL,
    Payment_Method VARCHAR(30),
    Store_Location VARCHAR(50)
);

-- Index creation for optimizing query execution times
CREATE INDEX idx_retail_date ON retail_sales(Date);
CREATE INDEX idx_retail_category ON retail_sales(Product_Category);
CREATE INDEX idx_retail_location ON retail_sales(Store_Location);
