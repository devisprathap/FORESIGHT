import pandas as pd
import joblib
model = joblib.load("models/forecast_model.pkl")
sales = pd.read_csv("data/processed/feature_engineered_sales.csv")
inventory = pd.read_csv("data/processed/cleaned_inventory_snapshots.csv")
features = [
    "month",
    "week",
    "day",
    "day_of_week",
    "quarter",
    "lag_1",
    "rolling_7",
    "promo_flag",
    "is_holiday"
]

X = sales[features]
sales["predicted_demand"] = model.predict(X)
risk = sales.merge(inventory, on=["sku_id", "date"])
def check_risk(row):

    if row["on_hand_units"] < row["predicted_demand"]:
        return "Stockout Risk"

    elif row["on_hand_units"] > row["predicted_demand"] * 2:
        return "Overstock"

    else:
        return "Normal"

risk["risk_status"] = risk.apply(check_risk, axis=1)
def recommendation(status):

    if status == "Stockout Risk":
        return "Reorder Immediately"

    elif status == "Overstock":
        return "Reduce Purchase"

    else:
        return "No Action"

risk["recommendation"] = risk["risk_status"].apply(recommendation)

risk.to_csv(
    "data/processed/risk_report.csv",
    index=False
)

print("Risk report generated successfully!")