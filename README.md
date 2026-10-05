# Retail Sales Analytics & Demand Forecasting System

A comprehensive end-to-end data engineering, visual analytics, and machine learning forecasting web application designed for retail enterprise sales transactions.

---

## ⚡ Direct Quick Launch Links

- 🌐 **[Launch Interactive GitHub Codespaces Workspace](https://github.com/codespaces/new?repo=abhay376/retail-sales-analytics)**
- 🖥️ **Local 1-Click Browser Launch**: Double-click `Click_To_Launch_Dashboard.bat` in your project folder or run:
  ```bash
  streamlit run app.py
  ```

---

## 🛠️ Technology Stack
- **Web Application & UI**: Streamlit, Plotly Express
- **Data Engineering & Analytics**: Python 3.13, Pandas, NumPy, C++17
- **Database & Querying**: PostgreSQL, SQLite
- **Machine Learning & Forecasting**: Scikit-Learn (Random Forest Regressor, Time-Series Lag Engineering)
- **Data Visualization & Business Intelligence**: Matplotlib, Seaborn, Power BI Desktop, Excel

---

## 📁 Repository Directory Structure

```text
retail_sales_analytics/
│
├── app.py                                # Interactive Streamlit Web Dashboard Application
├── Click_To_Launch_Dashboard.bat         # 1-Click Windows Browser Dashboard Launcher
│
├── data/                                 # Datasets & Database Engine
│   ├── retail_sales_raw.csv              # Primary raw transactions dataset (3,000 records)
│   ├── retail_sales_cleaned.csv          # Processed dataset with engineered temporal features
│   ├── retail_database.db                # SQLite database storing transactional relational tables
│   └── Retail_Analytics_Summary.xlsx     # Multi-tab aggregated summary workbook for BI integration
│
├── cpp_engine/                           # High-Performance C++ Ingestion Module
│   └── fast_retail_analyzer.cpp          # Fast C++ file stream parser & revenue aggregator
│
├── sql/                                  # Database Schemas & Analytical SQL Scripts
│   ├── 01_schema_and_tables.sql          # DDL table creation and index definitions
│   └── 02_analytics_queries.sql          # Structured SQL queries (Aggregations, CTEs, Window Functions)
│
├── notebooks/                            # Exploratory Notebooks
│   └── retail_sales_analytics.ipynb      # End-to-end data cleaning, EDA, & ML demand forecasting
│
├── scripts/                              # Automated Pipeline Execution
│   ├── generate_data.py                  # Data generation & SQLite database population
│   └── run_pipeline.py                   # Automated ETL, visualization plotting, & ML model execution
│
├── visualizations/                       # Generated Analytical Artifacts
│   ├── 01_monthly_sales_trend.png        # Monthly sales revenue trend line chart
│   ├── 02_category_revenue.png           # Category performance revenue bar chart
│   ├── 03_payment_distribution.png       # Payment method market share pie chart
│   └── 04_demand_forecasting_results.png # Time-series actual vs predicted sales plot
│
├── power_bi/                             # Business Intelligence Dashboard Documentation
│   └── PowerBI_Dashboard_Guide.md        # Data model architecture & DAX measure definitions
│
├── requirements.txt                      # Environment dependencies specification
└── README.md                             # Repository Overview
```

---

## 🚀 Execution & Usage Instructions

### GitHub Codespaces Environment Setup
The dev container installs project dependencies automatically after it is created. To launch the dashboard in Codespaces, run:
```bash
streamlit run app.py --server.address 0.0.0.0
```
Codespaces forwards port `8501` so you can open the dashboard in your browser.

### 1. Launch Interactive Web Dashboard
Run the web application to view live revenue trends, run interactive SQL queries, and execute demand forecasts in your browser:
```bash
streamlit run app.py
```

### 2. Execute Data Pipeline Script
Run the automated ETL script to transform transaction data and generate visualization plots:
```bash
python scripts/run_pipeline.py
```

### 3. High-Performance C++ Analytics Module
Compile and execute the native C++ stream processor for ultra-fast metric aggregations:
```bash
g++ -O3 -std=c++17 cpp_engine/fast_retail_analyzer.cpp -o cpp_engine/retail_analyzer
./cpp_engine/retail_analyzer
```

---

## 📊 Key Features & Web Dashboard Capabilities
- **Interactive Visual BI**: Real-time KPI metric filtering by date range, store location, and product category using Plotly.
- **Theme-Aware Interface**: Dashboard cards, controls, and charts follow Streamlit's active Light or Dark theme.
- **Custom Data Uploads**: Upload CSV or `.xlsx` retail data to use it across dashboard filters, charts, forecasts, SQL queries, and exports. Required columns: `Date`, `Customer_ID`, `Product_Category`, `Quantity`, `Total_Amount`, `Payment_Method`, and `Store_Location`.
- **SQL Analytics Sandbox**: Execute custom SQL queries (`GROUP BY`, `HAVING`, CTEs, Window Functions) directly from the web browser.
- **Machine Learning Demand Forecasting**: Interactive time-series sales prediction powered by Scikit-learn Random Forest Regressor.
