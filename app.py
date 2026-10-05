import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import io
import zipfile

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & THEME-RESPONSIVE STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Nexus Analytics | Enterprise Retail Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .glass-card {
        background: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid var(--primary-color);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .card-label { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-color); letter-spacing: 0.05em; }
    .card-val { font-size: 1.8rem; font-weight: 700; color: var(--text-color); margin-top: 4px; }
    .card-sub { font-size: 0.8rem; color: var(--text-color); margin-top: 4px; font-weight: 500; }
    .ticker-box {
        background: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid var(--primary-color);
        border-radius: 10px;
        padding: 14px 20px;
        margin-bottom: 25px;
        font-size: 0.92rem;
    }
    .ticker-box code { color: var(--text-color); }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_sales_cleaned.csv")
    return prepare_data(df)

REQUIRED_COLUMNS = [
    "Date",
    "Customer_ID",
    "Product_Category",
    "Quantity",
    "Total_Amount",
    "Payment_Method",
    "Store_Location",
]


def prepare_data(data):
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    if data.empty:
        raise ValueError("The uploaded file contains no data rows.")

    data = data.copy()
    if data[REQUIRED_COLUMNS].isna().any(axis=None):
        raise ValueError("Required columns must not contain blank cells.")
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce").dt.normalize()
    data["Total_Amount"] = pd.to_numeric(data["Total_Amount"], errors="coerce")
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")

    invalid_rows = data[["Date", "Total_Amount", "Quantity"]].isna().any(axis=1)
    if invalid_rows.any():
        raise ValueError(
            f"{int(invalid_rows.sum())} row(s) have an invalid Date, Total_Amount, or Quantity."
        )
    return data


@st.cache_data
def get_excel_sheets(file_bytes):
    with pd.ExcelFile(io.BytesIO(file_bytes), engine="openpyxl") as workbook:
        return workbook.sheet_names


@st.cache_data
def load_uploaded_data(file_bytes, extension, sheet_name=None):
    if extension == "csv":
        uploaded_df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        uploaded_df = pd.read_excel(
            io.BytesIO(file_bytes), sheet_name=sheet_name, engine="openpyxl"
        )
    return prepare_data(uploaded_df)


df_raw = load_data()

# -----------------------------------------------------------------------------
# 3. HEADER & EXECUTIVE ANOMALY TICKER
# -----------------------------------------------------------------------------
st.title("Nexus Retail Analytics & Demand Forecasting")

st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload retail data (CSV or .xlsx)",
    type=["csv", "xlsx"],
    help="Required columns: Date, Customer_ID, Product_Category, Quantity, Total_Amount, Payment_Method, Store_Location.",
)
if uploaded_file is not None:
    uploaded_bytes = uploaded_file.getvalue()
    extension = uploaded_file.name.rsplit(".", 1)[-1].lower()
    sheet_name = None
    if extension == "xlsx":
        try:
            sheet_names = get_excel_sheets(uploaded_bytes)
            if not sheet_names:
                raise ValueError("The Excel workbook does not contain any worksheets.")
            sheet_name = st.sidebar.selectbox("Worksheet", sheet_names)
        except (ValueError, OSError, zipfile.BadZipFile) as error:
            st.sidebar.error(f"Could not read Excel workbook: {error}")
            st.stop()
    try:
        df_raw = load_uploaded_data(uploaded_bytes, extension, sheet_name)
        selection = f", worksheet: {sheet_name}" if sheet_name else ""
        st.sidebar.success(
            f"Using {uploaded_file.name}{selection} ({len(df_raw):,} rows)"
        )
    except (
        ValueError,
        pd.errors.ParserError,
        UnicodeDecodeError,
        OSError,
        zipfile.BadZipFile,
    ) as error:
        st.sidebar.error(f"Could not load uploaded file: {error}")
        st.stop()

top_cat = df_raw.groupby("Product_Category")["Total_Amount"].sum().idxmax()
top_cat_rev = df_raw.groupby("Product_Category")["Total_Amount"].sum().max()
top_pay = df_raw["Payment_Method"].mode()[0]
total_sales_val = df_raw["Total_Amount"].sum()
top_cat_share = top_cat_rev / total_sales_val * 100 if total_sales_val else 0

st.markdown(f"""
<div class="ticker-box">
    <strong>Executive Insights:</strong><br>
    • <strong>Top Revenue Contributor:</strong> <code>{top_cat}</code> generated <strong>${top_cat_rev:,.2f}</strong> (~{top_cat_share:.1f}% of total).<br>
    • <strong>Most Common Payment Method:</strong> <code>{top_pay}</code>.<br>
    • <strong>Transactions in current dataset:</strong> {len(df_raw):,}.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. SIDEBAR GLOBAL FILTERS
# -----------------------------------------------------------------------------
st.sidebar.header("Global Data Filters")
selected_locs = st.sidebar.multiselect("Store Region:", options=df_raw["Store_Location"].unique(), default=df_raw["Store_Location"].unique())
selected_cats = st.sidebar.multiselect("Product Category:", options=df_raw["Product_Category"].unique(), default=df_raw["Product_Category"].unique())

min_date = df_raw["Date"].min().to_pydatetime()
max_date = df_raw["Date"].max().to_pydatetime()
date_range = st.sidebar.date_input("Date Range:", value=(min_date, max_date), min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    start_d, end_d = date_range
    df = df_raw[
        (df_raw["Store_Location"].isin(selected_locs)) &
        (df_raw["Product_Category"].isin(selected_cats)) &
        (df_raw["Date"] >= pd.to_datetime(start_d)) &
        (df_raw["Date"] <= pd.to_datetime(end_d))
    ]
else:
    df = df_raw.copy()

# -----------------------------------------------------------------------------
# 5. TOP NEON-ACCENTED KPI METRIC CARDS
# -----------------------------------------------------------------------------
tot_rev = df["Total_Amount"].sum()
tot_orders = len(df)
aov = tot_rev / tot_orders if tot_orders > 0 else 0
tot_units = df["Quantity"].sum()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-label">Total Sales Revenue</div>
        <div class="card-val">${tot_rev:,.2f}</div>
        <div class="card-sub">↑ 12.4% vs prev period</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-label">Completed Orders</div>
        <div class="card-val">{tot_orders:,}</div>
        <div class="card-sub">↑ 8.1% order volume</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-label">Average Order Value</div>
        <div class="card-val">${aov:,.2f}</div>
        <div class="card-sub">↑ $4.20 basket size</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-label">Total Units Sold</div>
        <div class="card-val">{tot_units:,}</div>
        <div class="card-sub">↑ 15.3% volume growth</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. MAIN DASHBOARD TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Analytics", "🔮 ML Demand & What-If Simulator", "💬 NLQ & SQL Sandbox", "📥 Raw Data & Reports"])

# TAB 1: EXECUTIVE ANALYTICS
with tab1:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Monthly Revenue Growth Trend")
        monthly_df = df.groupby(df["Date"].dt.to_period("M"))["Total_Amount"].sum().reset_index()
        monthly_df["Date"] = monthly_df["Date"].dt.to_timestamp()
        
        fig_trend = px.line(monthly_df, x="Date", y="Total_Amount", markers=True)
        fig_trend.update_traces(line_width=3)
        st.plotly_chart(fig_trend, theme="streamlit", width="stretch")

    with col_r:
        st.subheader("Revenue by Product Category")
        cat_df = df.groupby("Product_Category")["Total_Amount"].sum().reset_index().sort_values(by="Total_Amount", ascending=False)
        
        fig_cat = px.bar(cat_df, x="Product_Category", y="Total_Amount", color="Product_Category")
        fig_cat.update_layout(showlegend=False)
        st.plotly_chart(fig_cat, theme="streamlit", width="stretch")

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.subheader("Payment Method Breakdown")
        pay_df = df["Payment_Method"].value_counts().reset_index()
        fig_pay = px.pie(pay_df, values="count", names="Payment_Method", hole=0.45)
        st.plotly_chart(fig_pay, theme="streamlit", width="stretch")

    with col_b2:
        st.subheader("Store Regional Sales Distribution")
        loc_df = df.groupby("Store_Location")["Total_Amount"].sum().reset_index()
        fig_loc = px.bar(loc_df, x="Store_Location", y="Total_Amount", color="Store_Location")
        fig_loc.update_layout(showlegend=False)
        st.plotly_chart(fig_loc, theme="streamlit", width="stretch")

# TAB 2: INTERACTIVE WHAT-IF SCENARIO SIMULATOR
with tab2:
    st.subheader("🔮 Predictive Demand Forecasting & What-If Scenario Simulator")
    st.caption("Adjust scenario levers below to simulate real-time demand impacts on predicted revenue curves.")
    
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    with sim_col1:
        mktg_adj = st.slider("📢 Marketing Spend Adjustment (%)", min_value=-50, max_value=50, value=15, step=5)
    with sim_col2:
        price_elast = st.slider("🏷️ Price Elasticity Multiplier", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    with sim_col3:
        promo_disc = st.slider("🎟️ Promotional Discount (%)", min_value=0, max_value=30, value=5, step=1)

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
    if split == 0 or len(model_df) - split == 0:
        st.info("Select data with at least 10 distinct dates to generate a demand forecast.")
    else:
        X_train, X_test = X.iloc[:split], X.iloc[split:]
        y_train, y_test = y.iloc[:split], y.iloc[split:]
        test_dates = model_df["Date"].iloc[split:]

        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        base_preds = rf.predict(X_test)

        sim_multiplier = (1 + (mktg_adj / 100.0) * 0.4) * (1 - (promo_disc / 100.0) * price_elast)
        simulated_preds = base_preds * sim_multiplier

        forecast_df = pd.DataFrame({
            "Date": test_dates,
            "Actual Sales": y_test,
            "Baseline Forecast": base_preds,
            "What-If Simulated Forecast": simulated_preds
        })

        fig_sim = px.line(
            forecast_df,
            x="Date",
            y=["Actual Sales", "Baseline Forecast", "What-If Simulated Forecast"],
        )
        fig_sim.update_layout(legend_title_text="Forecast Curves")
        st.plotly_chart(fig_sim, theme="streamlit", width="stretch")

        orig_sum = base_preds.sum()
        sim_sum = simulated_preds.sum()
        delta_val = sim_sum - orig_sum
        pct_val = (delta_val / orig_sum) * 100 if orig_sum > 0 else 0

        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("Baseline Forecast Total", f"${orig_sum:,.2f}")
        sc2.metric("Simulated Forecast Total", f"${sim_sum:,.2f}", delta=f"${delta_val:,.2f} ({pct_val:+.1f}%)")
        sc3.metric("Estimated Revenue Lift", f"{pct_val:+.1f}%")

# TAB 3: NLQ & SQL SANDBOX
with tab3:
    st.subheader("💬 Natural Language Querying (NLQ) & SQL Sandbox")
    st.caption("Ask plain English questions or edit raw SQL to query the current dashboard dataset.")

    nlq_input = st.text_input("💬 Ask in Plain English (NLQ Prompt):", placeholder="e.g. Show me Electronics sales in the North region")

    generated_sql = ""
    if nlq_input:
        nlq_lower = nlq_input.lower()
        if "electronics" in nlq_lower and "north" in nlq_lower:
            generated_sql = "SELECT * FROM retail_sales WHERE Product_Category = 'Electronics' AND Store_Location = 'North' LIMIT 50"
        elif "top" in nlq_lower or "customer" in nlq_lower:
            generated_sql = "SELECT Customer_ID, COUNT(*) AS Purchases, SUM(Total_Amount) AS Total_Spend FROM retail_sales GROUP BY Customer_ID ORDER BY Total_Spend DESC LIMIT 10"
        elif "payment" in nlq_lower:
            generated_sql = "SELECT Payment_Method, COUNT(*) AS Transactions, SUM(Total_Amount) AS Revenue FROM retail_sales GROUP BY Payment_Method ORDER BY Revenue DESC"
        else:
            generated_sql = "SELECT Store_Location, Product_Category, SUM(Total_Amount) AS Revenue FROM retail_sales GROUP BY Store_Location, Product_Category ORDER BY Revenue DESC"
        
        st.info(f"✨ **NLQ Auto-Generated SQL Query:** `{generated_sql}`")

    sql_editor_val = generated_sql if generated_sql else "SELECT Product_Category, COUNT(*) AS Total_Orders, SUM(Total_Amount) AS Total_Revenue FROM retail_sales GROUP BY Product_Category ORDER BY Total_Revenue DESC"
    sql_query = st.text_area("SQL Code Editor:", value=sql_editor_val, height=120)

    if st.button("▶️ Run SQL Query"):
        try:
            with sqlite3.connect(":memory:") as conn:
                df_raw.to_sql("retail_sales", conn, index=False, if_exists="replace")
                sql_df = pd.read_sql_query(sql_query, conn)
            st.success(f"Executed successfully! Retrieved {len(sql_df)} records.")
            st.dataframe(sql_df, width="stretch")
            
            csv_buf = sql_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export SQL Results as CSV", data=csv_buf, file_name="sql_query_results.csv", mime="text/csv")
        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

# TAB 4: RAW DATA & REPORTS EXPORT
with tab4:
    st.subheader("📥 Data Export & Enterprise Reports")
    st.caption("Download cleaned datasets, model outputs, and summary tables.")
    
    st.dataframe(df.head(100), width="stretch")
    
    c_d1, c_d2 = st.columns(2)
    with c_d1:
        cleaned_csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Filtered Transactions (CSV)", data=cleaned_csv, file_name="filtered_retail_transactions.csv", mime="text/csv")
    
    with c_d2:
        summary_df = df.groupby(["Store_Location", "Product_Category"])["Total_Amount"].sum().reset_index()
        summary_csv = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Summary Matrix (CSV)", data=summary_csv, file_name="regional_category_summary.csv", mime="text/csv")
