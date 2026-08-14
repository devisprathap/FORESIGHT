import pandas as pd
sales = pd.read_csv("data/processed/cleaned_sales_daily.csv")
calendar = pd.read_csv("data/processed/cleaned_calendar.csv")
sales["date"] = pd.to_datetime(sales["date"])
calendar["date"] = pd.to_datetime(calendar["date"])
sales = sales.merge(calendar, on="date", how="left")
sales["year"] = sales["date"].dt.year
sales["month"] = sales["date"].dt.month
sales["week"] = sales["date"].dt.isocalendar().week
sales["day"] = sales["date"].dt.day
sales["day_of_week"] = sales["date"].dt.dayofweek
sales["quarter"] = sales["date"].dt.quarter
sales = sales.sort_values(["sku_id", "date"])

sales["lag_1"] = sales.groupby("sku_id")["units_sold"].shift(1)
sales["rolling_7"] = (
    sales.groupby("sku_id")["units_sold"]
    .transform(lambda x: x.rolling(7).mean())
)
sales.fillna(0, inplace=True)
sales.to_csv(
    "data/processed/feature_engineered_sales.csv",
    index=False
)

print("Feature Engineering Completed Successfully!")