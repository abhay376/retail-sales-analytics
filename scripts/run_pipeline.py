import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set plot style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
os.makedirs("visualizations", exist_ok=True)

def run_analytics_and_forecasting():
    print("--- STEP 1: LOADING DATA ---")
    data_path = os.path.join("data", "retail_sales_raw.csv")
    df = pd.read_csv(data_path)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns.")

    print("\n--- STEP 2: DATA CLEANING & TRANSFORMATIONS ---")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['YearMonth'] = df['Date'].dt.to_period('M')
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['IsWeekend'] = df['Date'].dt.dayofweek.isin([5, 6]).astype(int)

    # Export cleaned dataset
    cleaned_path = os.path.join("data", "retail_sales_cleaned.csv")
    df.to_csv(cleaned_path, index=False)
    print(f"Cleaned data saved to: {cleaned_path}")

    print("\n--- STEP 3: EXPLORATORY DATA ANALYSIS (EDA) & PLOTS ---")
    # Plot 1: Monthly Sales Revenue Trend
    monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Total_Amount'].sum().reset_index()
    monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()

    plt.figure(figsize=(12, 5))
    plt.plot(monthly_sales['Date'], monthly_sales['Total_Amount'], marker='o', color='#1f77b4', linewidth=2.5)
    plt.title("Monthly Sales Revenue Trend (2024 - 2025)", fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=11)
    plt.ylabel("Total Sales Revenue ($)", fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("visualizations/01_monthly_sales_trend.png", dpi=300)
    plt.close()

    # Plot 2: Category Revenue Breakdown
    cat_sales = df.groupby('Product_Category')['Total_Amount'].sum().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(10, 5))
    sns.barplot(data=cat_sales, x='Product_Category', y='Total_Amount', palette='viridis')
    plt.title("Total Revenue by Product Category", fontsize=14, fontweight='bold')
    plt.xlabel("Product Category", fontsize=11)
    plt.ylabel("Revenue ($)", fontsize=11)
    plt.tight_layout()
    plt.savefig("visualizations/02_category_revenue.png", dpi=300)
    plt.close()

    # Plot 3: Payment Method Distribution
    plt.figure(figsize=(7, 7))
    payment_counts = df['Payment_Method'].value_counts()
    plt.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', colors=sns.color_palette('Set2'), startangle=140)
    plt.title("Payment Method Share", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig("visualizations/03_payment_distribution.png", dpi=300)
    plt.close()

    print("Visualizations created in 'visualizations/' folder.")

    print("\n--- STEP 4: BASIC DEMAND FORECASTING (SCIKIT-LEARN) ---")
    # Aggregate daily sales revenue for time-series modeling
    daily_sales = df.groupby('Date').agg({
        'Total_Amount': 'sum',
        'Quantity': 'sum'
    }).reset_index()

    # Feature Engineering for Forecasting
    daily_sales['DayOfYear'] = daily_sales['Date'].dt.dayofyear
    daily_sales['DayOfWeek_Num'] = daily_sales['Date'].dt.dayofweek
    daily_sales['Month'] = daily_sales['Date'].dt.month
    daily_sales['Year'] = daily_sales['Date'].dt.year
    
    # Lag Features (Past sales demand)
    daily_sales['Sales_Lag_1'] = daily_sales['Total_Amount'].shift(1)
    daily_sales['Sales_Lag_7'] = daily_sales['Total_Amount'].shift(7)
    daily_sales['Rolling_Avg_7'] = daily_sales['Total_Amount'].shift(1).rolling(window=7).mean()

    # Drop NaNs created by lag features
    model_df = daily_sales.dropna().reset_index(drop=True)

    X = model_df[['DayOfYear', 'DayOfWeek_Num', 'Month', 'Year', 'Sales_Lag_1', 'Sales_Lag_7', 'Rolling_Avg_7']]
    y = model_df['Total_Amount']

    # Chronological Train-Test Split (80% train, 20% test)
    split_idx = int(len(model_df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    test_dates = model_df['Date'].iloc[split_idx:]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print(f"Model Evaluation Metrics:")
    print(f"  - Mean Absolute Error (MAE) : ${mae:.2f}")
    print(f"  - Root Mean Squared Error   : ${rmse:.2f}")
    print(f"  - R² Score                  : {r2:.4f}")

    # Plot Actual vs Forecasted Sales
    plt.figure(figsize=(12, 5))
    plt.plot(test_dates, y_test, label="Actual Daily Sales", color='black', alpha=0.7)
    plt.plot(test_dates, predictions, label="Forecasted Sales (RandomForest)", color='crimson', linestyle='--')
    plt.title("Demand Forecasting: Actual vs Predicted Daily Sales", fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=11)
    plt.ylabel("Daily Sales Revenue ($)", fontsize=11)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("visualizations/04_demand_forecasting_results.png", dpi=300)
    plt.close()

    # Save Excel Summary for Power BI & Excel portfolio
    excel_path = os.path.join("data", "Retail_Analytics_Summary.xlsx")
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Cleaned_Transactions', index=False)
        cat_sales.to_excel(writer, sheet_name='Category_Summary', index=False)
        pd.DataFrame({
            'Date': test_dates,
            'Actual_Sales': y_test,
            'Predicted_Sales': predictions
        }).to_excel(writer, sheet_name='Sales_Forecast', index=False)
    
    print(f"Exported Excel workbook: {excel_path}")
    print("\n--- PIPELINE EXECUTED SUCCESSFULLY! ---")

if __name__ == "__main__":
    run_analytics_and_forecasting()
