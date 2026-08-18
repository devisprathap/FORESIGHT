import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show():

    st.title(" Demand Forecast")

    # Load sales data
    try:
        sales = pd.read_csv(
            "data/processed/feature_engineered_sales.csv"
        )
    except Exception as e:
        st.error("Unable to load sales data.")
        st.exception(e)
        return

    st.success("Forecast page loaded successfully.")

    st.subheader(" Historical Demand")

    # Find date column
    date_col = None

    for col in ["date", "Date", "ds"]:
        if col in sales.columns:
            date_col = col
            break

    # Find demand/sales column
    value_col = None

    for col in [
        "units_sold",
        "quantity",
        "sales",
        "demand",
        "total_sales"
    ]:
        if col in sales.columns:
            value_col = col
            break

    if date_col is None:
        st.warning("Date column was not found in the sales dataset.")
        st.write("Available columns:")
        st.write(sales.columns.tolist())
        return

    if value_col is None:
        st.warning("Sales/demand column was not found.")
        st.write("Available columns:")
        st.write(sales.columns.tolist())
        return

    # Convert date
    sales[date_col] = pd.to_datetime(
        sales[date_col],
        errors="coerce"
    )

    sales[value_col] = pd.to_numeric(
        sales[value_col],
        errors="coerce"
    )

    sales = sales.dropna(
        subset=[date_col, value_col]
    )

    # Monthly demand
    monthly = (
        sales
        .set_index(date_col)[value_col]
        .resample("M")
        .sum()
    )

    if monthly.empty:
        st.warning("No valid sales data available.")
        return

    # Chart
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        monthly.index,
        monthly.values,
        marker="o"
    )

    ax.set_title("Monthly Demand Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Demand / Sales")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

    # Simple forecast
    st.subheader("🔮 Simple Demand Forecast")

    forecast_months = 3

    if len(monthly) >= 3:

        average_demand = monthly.tail(3).mean()

        future_dates = pd.date_range(
            start=monthly.index[-1] + pd.offsets.MonthEnd(1),
            periods=forecast_months,
            freq="M"
        )

        forecast = pd.Series(
            average_demand,
            index=future_dates
        )

        forecast_df = pd.DataFrame({
            "Month": future_dates,
            "Forecast Demand": forecast.values
        })

        st.dataframe(
            forecast_df,
            use_container_width=True
        )

        # Forecast chart
        fig2, ax2 = plt.subplots(figsize=(12, 5))

        ax2.plot(
            monthly.index,
            monthly.values,
            marker="o",
            label="Historical"
        )

        ax2.plot(
            forecast.index,
            forecast.values,
            marker="o",
            linestyle="--",
            label="Forecast"
        )

        ax2.set_title(
            "Historical Demand and Forecast"
        )

        ax2.set_xlabel("Month")
        ax2.set_ylabel("Demand")

        ax2.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig2)

        st.info(
            "The forecast shown here uses the average demand "
            "of the most recent three months as a simple baseline."
        )

    else:

        st.warning(
            "At least 3 months of historical data are required "
            "to generate the forecast."
        )
