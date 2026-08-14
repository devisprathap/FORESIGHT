import pandas as pd
import matplotlib.pyplot as plt

# ======================================
# Load Cleaned Datasets
# ======================================

sales = pd.read_csv("data/processed/cleaned_sales_daily.csv")
sku = pd.read_csv("data/processed/cleaned_sku_master.csv")
calendar = pd.read_csv("data/processed/cleaned_calendar.csv")
inventory = pd.read_csv("data/processed/cleaned_inventory_snapshots.csv")

# ======================================
# Display First 5 Rows
# ======================================

print("\nSales Data")
print(sales.head())

print("\nSKU Master")
print(sku.head())

print("\nCalendar")
print(calendar.head())

print("\nInventory")
print(inventory.head())

# ======================================
# Dataset Shape
# ======================================

print("\nDataset Shapes")
print("Sales:", sales.shape)
print("SKU:", sku.shape)
print("Calendar:", calendar.shape)
print("Inventory:", inventory.shape)

# ======================================
# Dataset Information
# ======================================

print("\nSales Info")
sales.info()

print("\nSKU Info")
sku.info()

print("\nCalendar Info")
calendar.info()

print("\nInventory Info")
inventory.info()

# ======================================
# Summary Statistics
# ======================================

print("\nSales Summary")
print(sales.describe())

# ======================================
# Merge Datasets
# ======================================

merged = sales.merge(sku, on="sku_id")
merged = merged.merge(calendar, on="date")

merged["date"] = pd.to_datetime(merged["date"])
merged["month"] = merged["date"].dt.month

# ======================================
# Top 10 Selling SKUs
# ======================================

top_skus = merged.groupby("sku_id")["units_sold"].sum().sort_values(ascending=False)

print("\nTop 10 Selling SKUs")
print(top_skus.head(10))

# ======================================
# Bottom 10 Selling SKUs
# ======================================

bottom_skus = merged.groupby("sku_id")["units_sold"].sum().sort_values()

print("\nBottom 10 Selling SKUs")
print(bottom_skus.head(10))

# ======================================
# Category-wise Sales
# ======================================

category_sales = merged.groupby("category")["units_sold"].sum()

print("\nCategory-wise Sales")
print(category_sales)

# ======================================
# Monthly Sales
# ======================================

monthly_sales = merged.groupby("month")["units_sold"].sum()

print("\nMonthly Sales")
print(monthly_sales)

# ======================================
# Monthly Sales Chart
# ======================================

monthly_sales.plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Units Sold")
plt.grid(True)

plt.savefig("reports/monthly_sales.png")

plt.show()

# ======================================
# Top 10 SKU Chart
# ======================================

top_skus.head(10).plot(kind="bar")

plt.title("Top 10 Selling SKUs")
plt.xlabel("SKU")
plt.ylabel("Units Sold")

plt.savefig("reports/top10_skus.png")

plt.show()

# ======================================
# Category-wise Sales Chart
# ======================================

category_sales.plot(kind="bar")

plt.title("Category-wise Sales")
plt.xlabel("Category")
plt.ylabel("Units Sold")

plt.savefig("reports/category_sales.png")

plt.show()
# ======================================
# Promotion Effect
# ======================================

promo_sales = merged.groupby("promo_flag")["units_sold"].mean()

print("\nAverage Sales During Promotion")
print(promo_sales)

promo_sales.plot(kind="bar")

plt.title("Average Sales During Promotion")
plt.xlabel("Promotion Flag")
plt.ylabel("Average Units Sold")

plt.savefig("reports/promotion_effect.png")

plt.show()
# ======================================
# Inventory Distribution
# ======================================

inventory["on_hand_units"].plot(kind="hist", bins=20)

plt.title("Inventory Distribution")
plt.xlabel("On Hand Units")

plt.savefig("reports/inventory_distribution.png")

plt.show()
# ======================================
# Weekly Sales Trend
# ======================================

merged["week"] = merged["date"].dt.isocalendar().week

weekly_sales = merged.groupby("week")["units_sold"].sum()

weekly_sales.plot(kind="line", marker="o")

plt.title("Weekly Sales Trend")
plt.xlabel("Week")
plt.ylabel("Units Sold")

plt.savefig("reports/weekly_sales.png")

plt.show()