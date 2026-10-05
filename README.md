# Retail Sales Analytics & Demand Forecasting System

A comprehensive end-to-end data engineering, visual analytics, and machine learning forecasting pipeline designed for retail enterprise sales transactions.

---

## 🛠️ Technology Stack
- **Data Engineering & Analytics**: Python 3.13, Pandas, NumPy, C++17
- **Database & Querying**: PostgreSQL, SQLite
- **Machine Learning & Forecasting**: Scikit-Learn (Random Forest Regressor, Time-Series Lag Engineering)
- **Data Visualization & Business Intelligence**: Matplotlib, Seaborn, Power BI Desktop, Excel

---

## 📁 Repository Directory Structure

```text
retail_sales_analytics/
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

## 🚀 Pipeline Execution Instructions

### 1. Execute Data Cleaning & ML Pipeline
Run the automated ETL script to transform transaction data, build lag features, train the forecasting model, and export visual charts:
```bash
python scripts/run_pipeline.py
```

### 2. High-Performance C++ Analytics Module
Compile and execute the native C++ stream processor for ultra-fast metric aggregations:
```bash
g++ -O3 -std=c++17 cpp_engine/fast_retail_analyzer.cpp -o cpp_engine/retail_analyzer
./cpp_engine/retail_analyzer
```

### 3. Launch Jupyter Analytics Notebook
To inspect the interactive data exploration and machine learning workflow:
```bash
jupyter notebook notebooks/retail_sales_analytics.ipynb
```

---

## 📊 Key Findings & System Capabilities
- **Revenue Analytics**: Automated category breakdown, regional store performance, and payment distribution metrics.
- **Advanced SQL Queries**: Relational schema supporting aggregations (`GROUP BY`, `HAVING`), customer segmentation CTEs, and product ranking window functions (`RANK() OVER(...)`).
- **Predictive Demand Forecasting**: Time-series lag feature engineering (`Sales_Lag_1`, `Sales_Lag_7`, `Rolling_Avg_7`) coupled with Random Forest Regression to predict future sales revenue trends.
