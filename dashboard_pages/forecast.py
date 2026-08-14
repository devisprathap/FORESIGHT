import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

def show():

    st.title("🤖 Demand Forecast")

    st.write("""
    This dashboard predicts future product demand using the trained
    machine learning forecasting model.
    """)

    # ===============================
    # Load Data
    # ===============================

    sales = pd.read_csv("data/processed/feature_engineered_sales.csv")

    # ===============================
    # Load Model
    # ===============================

    model = joblib.load("models/forecast_model.pkl")

    # ===============================
    # Prepare Features
    # ===============================

    X = sales[["month", "day_of_week", "promo_flag"]]

    # ===============================
    # Forecast
    # ===============================

    sales["Predicted Demand"] = model.predict(X)

    # ===============================
    # KPI Cards
    # ===============================

    col1, col2 = st.columns(2)

    col1.metric(
        "Average Actual Demand",
        round(sales["units_sold"].mean(), 2)
    )

    col2.metric(
        "Average Forecast Demand",
        round(sales["Predicted Demand"].mean(), 2)
    )

    # ===============================
    # Actual vs Forecast
    # ===============================

    st.subheader("📈 Actual vs Forecast Demand")

    monthly = sales.groupby("month")[["units_sold","Predicted Demand"]].mean()

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(
        monthly.index,
        monthly["units_sold"],
        marker="o",
        label="Actual"
    )

    ax.plot(
        monthly.index,
        monthly["Predicted Demand"],
        marker="s",
        label="Forecast"
    )

    ax.set_xlabel("Month")

    ax.set_ylabel("Demand")

    ax.legend()

    st.pyplot(fig)

    # ===============================
    # Forecast Table
    # ===============================

    st.subheader("Forecast Results")

    st.dataframe(
        sales[
            [
                "date",
                "sku_id",
                "units_sold",
                "Predicted Demand"
            ]
        ].head(100)
    )

    # ===============================
    # Download Button
    # ===============================

    csv = sales.to_csv(index=False)

    st.download_button(
        label="Download Forecast",
        data=csv,
        file_name="forecast_results.csv",
        mime="text/csv"
    )

    # ===============================
    # Business Insights
    # ===============================

    st.subheader("💡 Forecast Insights")

    if sales["Predicted Demand"].mean() > sales["units_sold"].mean():

        st.success(
            "Demand is expected to increase. Increase inventory levels."
        )

    else:

        st.warning(
            "Demand is expected to decrease. Avoid overstocking."
        )