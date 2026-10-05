# Retail Sales Analytics Dashboard with Basic Demand Forecasting

A complete end-to-end data analytics, machine learning forecasting, and database project matching the tech stack listed on your resume.

---

## 🛠️ Tech Stack Included
- **Programming & Analysis**: Python 3.13, Pandas, NumPy, C++17 (High-Performance Module)
- **Data Visualization**: Matplotlib, Seaborn, Power BI
- **Database & SQL**: PostgreSQL, SQLite
- **Machine Learning**: Scikit-Learn (Random Forest Regressor, Time-Series Lag Features)
- **Reporting & Tools**: Excel (`openpyxl`), Jupyter Notebook, Power BI Desktop

---

## 📁 Repository Directory Structure

```text
retail_sales_analytics/
│
├── data/                                 # Datasets & Database Files
│   ├── retail_sales_raw.csv              # Synthetic raw transactions dataset (3,000 records)
│   ├── retail_sales_cleaned.csv          # Cleaned dataset with temporal features
│   ├── retail_database.db                # SQLite database populated with transaction table
│   └── Retail_Analytics_Summary.xlsx     # Multi-tab Excel summary workbook for Power BI
│
├── cpp_engine/                           # C++ High-Performance Data Engine
│   └── fast_retail_analyzer.cpp          # Fast C++ CSV parser & revenue metrics aggregator
│
├── sql/                                  # SQL Database Scripts
│   ├── 01_schema_and_tables.sql          # Table DDL & index creation script
│   └── 02_analytics_queries.sql          # PostgreSQL/SQLite aggregation, CTEs & window queries
│
├── notebooks/                            # Jupyter Notebooks
│   └── retail_sales_analytics.ipynb      # Step-by-step EDA, SQL execution, & ML forecasting
│
├── scripts/                              # Automated Python Pipelines
│   ├── generate_data.py                  # Generates retail transactions dataset & SQLite DB
│   └── run_pipeline.py                   # Executes data cleaning, EDA plots & ML forecasting model
│
├── visualizations/                       # Generated High-Res Visual Analytics
│   ├── 01_monthly_sales_trend.png        # Line plot of monthly revenue trends
│   ├── 02_category_revenue.png           # Bar chart of sales by product category
│   ├── 03_payment_distribution.png       # Pie chart of payment methods
│   └── 04_demand_forecasting_results.png # Actual vs Predicted daily sales graph
│
├── power_bi/                             # Power BI Setup & DAX Guide
│   └── PowerBI_Dashboard_Guide.md        # Step-by-step canvas layout & DAX measure formulas
│
├── interview_prep/                       # Interview Preparation Material
│   └── INTERVIEW_CHEAT_SHEET.md          # 30-sec pitch, QA breakdown, C++ explanation & SQL review
│
├── requirements.txt                      # Python dependencies list
└── README.md                             # Project Documentation
```

---

## 🚀 How to Run the Project

### 1. Run Python Automated Pipeline
Run the Python script to generate visualizations, cleaned CSV files, and Excel summaries:
```bash
.venv\Scripts\python scripts/run_pipeline.py
```

### 2. Run C++ High-Performance Data Analyzer
If you have `g++` installed, compile and run the native C++ engine:
```bash
g++ -O3 -std=c++17 cpp_engine/fast_retail_analyzer.cpp -o cpp_engine/retail_analyzer
./cpp_engine/retail_analyzer
```

### 3. Open Jupyter Notebook
To view or present the interactive notebook step-by-step:
```bash
.venv\Scripts\jupyter notebook notebooks/retail_sales_analytics.ipynb
```

---

## 🎯 Interview Quick Reference

For your interview in 2 days, open **`interview_prep/INTERVIEW_CHEAT_SHEET.md`**. It contains:
1. Your 30-Second Resume Elevator Pitch.
2. Detailed answers for every bullet point on your resume.
3. PostgreSQL queries (aggregations, `GROUP BY`, `HAVING`, window functions).
4. How to confidently explain using **C++** in your data analytics project.
5. DAX measures and Power BI setup steps.
