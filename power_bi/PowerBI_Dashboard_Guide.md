# Power BI Dashboard Setup & DAX Guide

This guide details how to build the **Interactive Retail Sales Analytics Dashboard** in Power BI Desktop using the dataset exported from Python (`data/retail_sales_cleaned.csv` or `data/Retail_Analytics_Summary.xlsx`).

---

## 1. Data Connection & Power Query Cleaning
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV** and select `data/retail_sales_cleaned.csv`.
3. Click **Transform Data** to enter Power Query Editor:
   - Ensure `Date` column type is set to **Date**.
   - Ensure `Quantity`, `Age` are set to **Whole Number**.
   - Ensure `Price_Per_Unit` and `Total_Amount` are set to **Fixed Decimal Number / Currency**.
4. Click **Close & Apply**.

---

## 2. Key DAX Measures Created

Create a new table called `_Measures` and add the following DAX calculations:

### 1. Total Revenue
```dax
Total Revenue = SUM(retail_sales_cleaned[Total_Amount])
```

### 2. Total Transactions / Orders
```dax
Total Orders = COUNT(retail_sales_cleaned[Transaction_ID])
```

### 3. Average Order Value (AOV)
```dax
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

### 4. Total Units Sold
```dax
Total Units Sold = SUM(retail_sales_cleaned[Quantity])
```

### 5. Year-to-Date (YTD) Revenue
```dax
YTD Revenue = TOTALYTD([Total Revenue], retail_sales_cleaned[Date])
```

### 6. Month-over-Month (MoM) Sales Growth %
```dax
MoM Sales Growth % = 
VAR PreviousMonthRevenue = CALCULATE([Total Revenue], DATEADD(retail_sales_cleaned[Date], -1, MONTH))
RETURN DIVIDE([Total Revenue] - PreviousMonthRevenue, PreviousMonthRevenue, 0)
```

---

## 3. Visual Layout & Canvas Design

### Header & KPI Cards (Top Banner)
- **Card 1**: Total Revenue (`$Total Revenue`)
- **Card 2**: Total Orders (`Total Orders`)
- **Card 3**: Average Order Value (`$AOV`)
- **Card 4**: Total Units Sold (`Total Units Sold`)

### Central Visual Insights
- **Monthly Revenue Trend**: Line Chart with `Date` (Year/Month hierarchy) on X-axis and `[Total Revenue]` on Y-axis.
- **Category Sales Breakdown**: Clustered Bar Chart with `Product_Category` on Y-axis and `[Total Revenue]` on X-axis.
- **Regional Sales Distribution**: Donut Chart or Treemap with `Store_Location` as Legend and `[Total Revenue]` as Values.
- **Payment Method Preferences**: Pie Chart with `Payment_Method` as Legend and `[Total Orders]` as Values.

### Interactive Slicers (Left Sidebar / Top Filters)
- **Date Range Slicer**: Relative / Between date range picker.
- **Store Location Slicer**: Buttons for North, South, East, West, Central.
- **Product Category Slicer**: Multi-select dropdown.

---

## 4. Key Interview Highlights for Power BI
- **Question**: *"How did you connect Power BI with Python?"*
  - **Answer**: *"I used Python (Pandas) for data cleaning, transformation, and ML demand forecasting, and exported clean structured datasets (`retail_sales_cleaned.csv`) into Power BI. I created custom DAX measures for YTD Sales, MoM growth %, and Average Order Value to power dynamic KPI cards and interactive visual slicers."*
