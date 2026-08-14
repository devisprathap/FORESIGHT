import pandas as pd

# Sales Data
# ----------------------------

# Load the dataset
sales = pd.read_csv("data/raw/sales_daily.csv")

# View first 5 rows
print(sales.head())

# Check information
print(sales.info())

# Check missing values
print(sales.isnull().sum())

# Remove duplicate rows
sales = sales.drop_duplicates()

# Convert date column
sales["date"] = pd.to_datetime(sales["date"])

# Save cleaned data
sales.to_csv("data/processed/cleaned_sales_daily.csv", index=False)

print("Data cleaned successfully!")
import pandas as pd



# ----------------------------
# SKU Master
# ----------------------------
sku = pd.read_csv("data/raw/sku_master.csv")

sku.drop_duplicates(inplace=True)
sku.fillna("Unknown", inplace=True)

sku.to_csv("data/processed/cleaned_sku_master.csv", index=False)

# ----------------------------
# Calendar
# ----------------------------
calendar = pd.read_csv("data/raw/calendar.csv")

calendar.drop_duplicates(inplace=True)
calendar["date"] = pd.to_datetime(calendar["date"])

calendar.to_csv("data/processed/cleaned_calendar.csv", index=False)

# ----------------------------
# Inventory
# ----------------------------
inventory = pd.read_csv("data/raw/inventory_snapshots.csv")

inventory.drop_duplicates(inplace=True)
inventory["date"] = pd.to_datetime(inventory["date"])

inventory.to_csv("data/processed/cleaned_inventory_snapshots.csv", index=False)

print("All datasets cleaned successfully!")