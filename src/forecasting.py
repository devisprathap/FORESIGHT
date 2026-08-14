import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
data = pd.read_csv("data/processed/feature_engineered_sales.csv")

print(data.head())
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

X = data[features]
y = data["units_sold"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)

print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)
joblib.dump(model, "models/forecast_model.pkl")

print("Forecast model saved successfully!")