-- =========================================================================
-- RETAIL SALES ANALYTICS DASHBOARD - ANALYTICAL SQL QUERIES
-- Includes Aggregations, Filtering, Grouping, Subqueries & Window Functions
-- =========================================================================

-- -------------------------------------------------------------------------
-- QUERY 1: Overall Business KPIs (Total Revenue, Total Orders, Average Order Value, Total Units)
-- -------------------------------------------------------------------------
SELECT 
    COUNT(Transaction_ID) AS Total_Orders,
    SUM(Quantity) AS Total_Units_Sold,
    SUM(Total_Amount) AS Total_Revenue,
    ROUND(AVG(Total_Amount), 2) AS Average_Order_Value,
    MIN(Total_Amount) AS Min_Transaction_Value,
    MAX(Total_Amount) AS Max_Transaction_Value
FROM retail_sales;


-- -------------------------------------------------------------------------
-- QUERY 2: Revenue and Quantity Breakdown by Product Category (Aggregation & Grouping)
-- -------------------------------------------------------------------------
SELECT 
    Product_Category,
    COUNT(Transaction_ID) AS Total_Transactions,
    SUM(Quantity) AS Units_Sold,
    SUM(Total_Amount) AS Total_Category_Revenue,
    ROUND(AVG(Total_Amount), 2) AS Avg_Transaction_Value,
    ROUND(SUM(Total_Amount) * 100.0 / (SELECT SUM(Total_Amount) FROM retail_sales), 2) AS Revenue_Percentage
FROM retail_sales
GROUP BY Product_Category
ORDER BY Total_Category_Revenue DESC;


-- -------------------------------------------------------------------------
-- QUERY 3: Regional Store Performance Analysis (Filter & Aggregation with HAVING)
-- -------------------------------------------------------------------------
SELECT 
    Store_Location,
    Product_Category,
    SUM(Total_Amount) AS Regional_Category_Revenue,
    COUNT(DISTINCT Customer_ID) AS Unique_Customers
FROM retail_sales
GROUP BY Store_Location, Product_Category
HAVING SUM(Total_Amount) > 10000
ORDER BY Store_Location ASC, Regional_Category_Revenue DESC;


-- -------------------------------------------------------------------------
-- QUERY 4: Monthly Sales Trends and Growth Analysis (Date Aggregation)
-- -------------------------------------------------------------------------
SELECT 
    SUBSTR(Date, 1, 7) AS Sales_Month, -- Works in SQLite & PostgreSQL (or DATE_TRUNC('month', Date))
    COUNT(Transaction_ID) AS Monthly_Orders,
    SUM(Total_Amount) AS Monthly_Revenue,
    ROUND(AVG(Total_Amount), 2) AS Avg_Order_Size
FROM retail_sales
GROUP BY SUBSTR(Date, 1, 7)
ORDER BY Sales_Month ASC;


-- -------------------------------------------------------------------------
-- QUERY 5: Customer Demographics Analysis (Age Groups & Gender Spending)
-- -------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN Age < 25 THEN '18-24 (Gen Z)'
        WHEN Age BETWEEN 25 AND 40 THEN '25-40 (Millennials)'
        WHEN Age BETWEEN 41 AND 55 THEN '41-55 (Gen X)'
        ELSE '56+ (Seniors)'
    END AS Age_Group,
    Gender,
    COUNT(Transaction_ID) AS Total_Purchases,
    SUM(Total_Amount) AS Total_Spend,
    ROUND(AVG(Total_Amount), 2) AS Avg_Spend_Per_Order
FROM retail_sales
GROUP BY 
    CASE 
        WHEN Age < 25 THEN '18-24 (Gen Z)'
        WHEN Age BETWEEN 25 AND 40 THEN '25-40 (Millennials)'
        WHEN Age BETWEEN 41 AND 55 THEN '41-55 (Gen X)'
        ELSE '56+ (Seniors)'
    END,
    Gender
ORDER BY Total_Spend DESC;


-- -------------------------------------------------------------------------
-- QUERY 6: Top 10 High-Value Customers (Subqueries & Customer Spend Ranking)
-- -------------------------------------------------------------------------
SELECT 
    Customer_ID,
    COUNT(Transaction_ID) AS Total_Visits,
    SUM(Quantity) AS Total_Items_Bought,
    SUM(Total_Amount) AS Lifetime_Value
FROM retail_sales
GROUP BY Customer_ID
HAVING SUM(Total_Amount) > (SELECT AVG(Total_Amount) * 3 FROM retail_sales)
ORDER BY Lifetime_Value DESC
LIMIT 10;


-- -------------------------------------------------------------------------
-- QUERY 7: Window Functions - Ranking Top Products per Category
-- -------------------------------------------------------------------------
WITH Product_Sales AS (
    SELECT 
        Product_Category,
        Product_Name,
        SUM(Quantity) AS Total_Units_Sold,
        SUM(Total_Amount) AS Product_Revenue,
        ROW_NUMBER() OVER (PARTITION BY Product_Category ORDER BY SUM(Total_Amount) DESC) AS Rank_In_Category
    FROM retail_sales
    GROUP BY Product_Category, Product_Name
)
SELECT 
    Product_Category,
    Product_Name,
    Total_Units_Sold,
    Product_Revenue,
    Rank_In_Category
FROM Product_Sales
WHERE Rank_In_Category <= 3
ORDER BY Product_Category, Rank_In_Category;


-- -------------------------------------------------------------------------
-- QUERY 8: Payment Method Preferences & Revenue Contribution
-- -------------------------------------------------------------------------
SELECT 
    Payment_Method,
    COUNT(Transaction_ID) AS Usage_Count,
    SUM(Total_Amount) AS Total_Volume,
    ROUND(AVG(Total_Amount), 2) AS Avg_Order_Value
FROM retail_sales
GROUP BY Payment_Method
ORDER BY Total_Volume DESC;
