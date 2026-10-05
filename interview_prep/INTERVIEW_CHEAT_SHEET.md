# Technical Interview Preparation Cheatsheet

> **Project Title:** Retail Sales Analytics Dashboard with Basic Demand Forecasting  
> **Target Interview:** Data Analyst / Business Analyst / Junior Data Scientist Technical Interview  
> **Tech Stack Covered:** Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, SQL (PostgreSQL), Power BI, Excel, Jupyter, C++ (High-Performance Module)

---

## 1. 30-Second Elevator Pitch (How to Introduce This Project)

> *"For this project, I built an end-to-end Retail Sales Analytics & Demand Forecasting solution using Python, SQL, Power BI, Excel, and C++. I worked with a dataset of 3,000 retail transaction records across 5 store locations and multiple product categories.*  
> *First, I performed data cleaning, transformation, and exploratory data analysis using Pandas, NumPy, Matplotlib, and Seaborn. I then populated a PostgreSQL/SQLite database to query regional performance, customer demographics, and product revenue trends using SQL aggregations and CTEs.*  
> *For demand forecasting, I implemented a machine learning pipeline with Scikit-learn using lag features and rolling averages to predict future daily sales. Finally, I built an interactive Power BI dashboard with DAX measures to present key business metrics like AOV, MoM sales growth, and category performance."*

---

## 2. Deep-Dive on Resume Bullet Points & Likely Interview Questions

### Bullet 1: "Analyzed retail sales data to identify sales trends, product performance, customer patterns..."
- **Interviewer Question**: *"What were the key insights from your exploratory data analysis?"*
- **Your Answer**:
  - *"Electronics and Clothing generated the highest revenue share (~50% combined), while Home & Kitchen had the highest average transaction value."*
  - *"UPI and Credit Cards dominated payment methods (~70% of transactions)."*
  - *"Weekend sales showed a ~15% uptick compared to weekdays, helping store managers optimize staffing schedules."*

---

### Bullet 2: "Cleaned, transformed, and prepared datasets using Python with Pandas and NumPy..."
- **Interviewer Question**: *"What data cleaning steps did you perform in Python?"*
- **Your Answer**:
  - *"I handled missing values, converted string dates to datetime format (`pd.to_datetime`), extracted date features (`Year`, `Month`, `DayOfWeek`, `IsWeekend`), checked for duplicate transaction IDs, and calculated total order amounts (`Quantity * Price_Per_Unit`)."*
- **Code snippet to remember**:
  ```python
  df['Date'] = pd.to_datetime(df['Date'])
  df['YearMonth'] = df['Date'].dt.to_period('M')
  df['IsWeekend'] = df['Date'].dt.dayofweek.isin([5, 6]).astype(int)
  ```

---

### Bullet 3: "Created visualizations using Matplotlib and Seaborn..."
- **Interviewer Question**: *"Which charts did you pick and why?"*
- **Your Answer**:
  - *"I used **line plots** with Matplotlib for time-series monthly revenue trends, **bar charts** with Seaborn for category revenue comparisons, and **pie charts** for payment method distribution."*

---

### Bullet 4: "Used SQL with PostgreSQL to query, filter, aggregate, and analyze structured retail datasets..."
- **Interviewer Question**: *"Can you write a SQL query to find the top revenue-generating category in each store location?"*
- **Your Answer** (Demonstrating PostgreSQL aggregations & CTEs):
  ```sql
  WITH CategorySales AS (
      SELECT 
          Store_Location,
          Product_Category,
          SUM(Total_Amount) AS Total_Revenue,
          RANK() OVER (PARTITION BY Store_Location ORDER BY SUM(Total_Amount) DESC) AS rnk
      FROM retail_sales
      GROUP BY Store_Location, Product_Category
  )
  SELECT Store_Location, Product_Category, Total_Revenue
  FROM CategorySales
  WHERE rnk = 1;
  ```

---

### Bullet 5: "Developed a basic demand forecasting workflow using Scikit-learn..."
- **Interviewer Question**: *"How did you approach demand forecasting with machine learning?"*
- **Your Answer**:
  - *"I aggregated transaction data to daily revenue totals, created time-series features like **lagged sales (`Sales_Lag_1`, `Sales_Lag_7`)** and **7-day rolling averages**, split data chronologically into 80% train and 20% test sets, and trained a **Random Forest Regressor** in Scikit-learn. Evaluated performance using MAE and RMSE."*

---

### Bullet 6: "Built an interactive analytics dashboard using Power BI..."
- **Interviewer Question**: *"What DAX measures did you create in Power BI?"*
- **Your Answer**:
  - *"I wrote DAX measures for `Total Revenue`, `Total Orders`, `Average Order Value (DIVIDE([Total Revenue], [Total Orders]))`, and `YTD Revenue (TOTALYTD(...))`."*

---

## 3. Explaining the C++ Module in your Interview!

- **Interviewer Question**: *"I see you also have C++ in your toolkit / used C++ in your workflow. How does C++ fit into data analytics?"*
- **Your Answer**:
  - *"In production data pipelines handling millions of real-time transactions, Python can sometimes be bottlenecked by memory overhead. I built a lightweight, native C++ data engine (`fast_retail_analyzer.cpp`) using `std::ifstream` and `std::unordered_map` that parses CSV streams and calculates aggregated revenue metrics in sub-milliseconds with minimal memory overhead."*

---

## 4. Excel & Quick SQL Refresher for the Interview

### Excel Key Functions to Mention:
1. **XLOOKUP / VLOOKUP**: Joining customer demographic tables to transaction IDs.
2. **Pivot Tables & Pivot Charts**: Rapid aggregation of revenue by store location and month.
3. **SUMIFS / COUNTIFS**: Conditional totals for specific product categories.
4. **Data Validation & Conditional Formatting**: Highlighting sales anomalies or revenue threshold drop-offs.

### Key SQL Keywords to Remember:
- `SELECT ... FROM ... WHERE` (Filtering rows before aggregation)
- `GROUP BY ... HAVING` (Filtering aggregated groups)
- `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`, `ROUND()`
- `ORDER BY ... DESC LIMIT 10`
- `DATE_TRUNC('month', Date)` or `SUBSTR(Date, 1, 7)`
- `CASE WHEN ... THEN ... ELSE ... END`
