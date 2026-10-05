import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Retail Analytics & Demand Forecasting",
    page_icon="🏬",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        padding: 18px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stAppViewContainer {
        background-color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_sales_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df_raw = load_data()

# Title Header
st.title("🏬 Retail Sales Analytics & Demand Forecasting Dashboard")
st.markdown("Interactive Data Visualization, SQL Query Engine, and Machine Learning Demand Forecasting.")

# Sidebar Filters
st.sidebar.header("🔍 Dashboard Filters")
locations = st.sidebar.multiselect("Select Store Location:", options=df_raw["Store_Location"].unique(), default=df_raw["Store_Location"].unique())
categories = st.sidebar.multiselect("Select Product Category:", options=df_raw["Product_Category"].unique(), default=df_raw["Product_Category"].unique())

min_date = df_raw["Date"].min().to_pydatetime()
max_date = df_raw["Date"].max().to_pydatetime()
date_range = st.sidebar.date_input("Select Date Range:", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Filter Data
if len(date_range) == 2:
    start_d, end_d = date_range
    df = df_raw[
        (df_raw["Store_Location"].isin(locations)) &
        (df_raw["Product_Category"].isin(categories)) &
        (df_raw["Date"] >= pd.to_datetime(start_d)) &
        (df_raw["Date"] <= pd.to_datetime(end_d))
    ]
else:
    df = df_raw.copy()

# KPI Metric Row
total_revenue = df["Total_Amount"].sum()
total_orders = len(df)
aov = total_revenue / total_orders if total_orders > 0 else 0
units_sold = df["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💵 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("🛍️ Total Orders", f"{total_orders:,}")
col3.metric("💳 Avg Order Value (AOV)", f"${aov:,.2f}")
col4.metric("📦 Units Sold", f"{units_sold:,}")

st.divider()

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📈 Executive Insights & Trends", "🗃️ SQL Analytics Sandbox", "🔮 Live ML Demand Forecasting"])

with tab1:
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Monthly Revenue Trend")
        monthly_df = df.groupby(df["Date"].dt.to_period("M"))["Total_Amount"].sum().reset_index()
        monthly_df["Date"] = monthly_df["Date"].dt.to_timestamp()
        fig_trend = px.line(monthly_df, x="Date", y="Total_Amount", markers=True, title="Monthly Revenue Growth", line_shape="spline")
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        st.subheader("Revenue by Product Category")
        cat_df = df.groupby("Product_Category")["Total_Amount"].sum().reset_index().sort_values(by="Total_Amount", ascending=False)
        fig_cat = px.bar(cat_df, x="Product_Category", y="Total_Amount", color="Product_Category", title="Category Sales Breakdown")
        st.plotly_chart(fig_cat, use_container_width=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.subheader("Payment Method Share")
        pay_df = df["Payment_Method"].value_counts().reset_index()
        fig_pay = px.pie(pay_df, values="count", names="Payment_Method", title="Payment Method Distribution", hole=0.4)
        st.plotly_chart(fig_pay, use_container_width=True)

    with col_b2:
        st.subheader("Revenue by Location")
        loc_df = df.groupby("Store_Location")["Total_Amount"].sum().reset_index()
        fig_loc = px.bar(loc_df, x="Store_Location", y="Total_Amount", color="Store_Location", title="Store Regional Revenue")
        st.plotly_chart(fig_loc, use_container_width=True)

with tab2:
    st.subheader("Interactive SQL Analytics Engine")
    st.caption("Execute custom SQL queries against the underlying SQLite retail database.")
    
    sample_queries = {
        "1. Overall Metrics Summary": "SELECT COUNT(*) AS Orders, SUM(Total_Amount) AS Revenue, AVG(Total_Amount) AS AOV FROM retail_sales",
        "2. Category Revenue Breakdown": "SELECT Product_Category, SUM(Total_Amount) AS Category_Revenue FROM retail_sales GROUP BY Product_Category ORDER BY Category_Revenue DESC",
        "3. Top Spending Customers": "SELECT Customer_ID, COUNT(*) AS Visits, SUM(Total_Amount) AS Spend FROM retail_sales GROUP BY Customer_ID ORDER BY Spend DESC LIMIT 10"
    }

    selected_sample = st.selectbox("Select a Sample SQL Query:", list(sample_queries.keys()))
    user_query = st.text_area("SQL Query Editor:", value=sample_queries[selected_sample], height=100)

    if st.button("▶️ Execute SQL Query"):
        try:
            conn = sqlite3.connect("data/retail_database.db")
            sql_res = pd.read_sql_query(user_query, conn)
            conn.close()
            st.success("Query Executed Successfully!")
            st.dataframe(sql_res, use_container_width=True)
        except Exception as e:
            st.error(f"SQL Error: {e}")

with tab3:
    st.subheader("Predictive Demand Forecasting Model (Random Forest)")
    st.caption("Machine learning model using 7-day rolling averages and sales lag features.")

    daily = df.groupby("Date")["Total_Amount"].sum().reset_index()
    daily["DayOfYear"] = daily["Date"].dt.dayofyear
    daily["DayOfWeek"] = daily["Date"].dt.dayofweek
    daily["Month"] = daily["Date"].dt.month
    daily["Year"] = daily["Date"].dt.year
    daily["Sales_Lag_1"] = daily["Total_Amount"].shift(1)
    daily["Rolling_Avg_7"] = daily["Total_Amount"].shift(1).rolling(7).mean()

    model_df = daily.dropna()
    X = model_df[["DayOfYear", "DayOfWeek", "Month", "Year", "Sales_Lag_1", "Rolling_Avg_7"]]
    y = model_df["Total_Amount"]

    split = int(len(model_df) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    test_dates = model_df["Date"].iloc[split:]

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    preds = rf.predict(X_test)

    res_df = pd.DataFrame({"Date": test_dates, "Actual_Sales": y_test, "Predicted_Sales": preds})
    fig_pred = px.line(res_df, x="Date", y=["Actual_Sales", "Predicted_Sales"], title="Daily Demand Forecasting: Actual vs Predicted Revenue")
    st.plotly_chart(fig_pred, use_container_width=True)

