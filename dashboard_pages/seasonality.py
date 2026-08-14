import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():

    st.title("📅 Seasonality Dashboard")

    st.write("""
    This dashboard analyzes seasonal sales trends to identify
    peak and low demand periods throughout the year.
    """)

    # ======================================
    # Load Data
    # ======================================

    sales = pd.read_csv("data/processed/feature_engineered_sales.csv")

    sales["date"] = pd.to_datetime(sales["date"])

    sales["month"] = sales["date"].dt.month
    sales["month_name"] = sales["date"].dt.month_name()

    sales["week"] = sales["date"].dt.isocalendar().week
    sales["day_name"] = sales["date"].dt.day_name()

    # ======================================
    # KPI Cards
    # ======================================

    monthly_sales = sales.groupby("month_name")["units_sold"].sum()

    peak_month = monthly_sales.idxmax()
    low_month = monthly_sales.idxmin()

    peak_sales = monthly_sales.max()
    low_sales = monthly_sales.min()

    col1, col2 = st.columns(2)

    col1.metric("🏆 Peak Sales Month", peak_month)

    col2.metric("📉 Lowest Sales Month", low_month)

    # ======================================
    # Monthly Sales Trend
    # ======================================

    st.subheader("📈 Monthly Sales Trend")

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    monthly_sales = (
        sales.groupby("month_name")["units_sold"]
        .sum()
        .reindex(month_order)
    )

    fig, ax = plt.subplots(figsize=(10,5))

    monthly_sales.plot(
        marker="o",
        linewidth=3,
        ax=ax
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Units Sold")

    st.pyplot(fig)

    # ======================================
    # Weekly Sales
    # ======================================

    st.subheader("📊 Weekly Sales Trend")

    weekly_sales = sales.groupby("week")["units_sold"].sum()

    fig, ax = plt.subplots(figsize=(10,5))

    weekly_sales.plot(
        color="green",
        ax=ax
    )

    ax.set_xlabel("Week")
    ax.set_ylabel("Units Sold")

    st.pyplot(fig)

    # ======================================
    # Day-wise Sales
    # ======================================

    st.subheader("📅 Day-wise Sales")

    day_order = [
        "Monday","Tuesday","Wednesday",
        "Thursday","Friday","Saturday","Sunday"
    ]

    day_sales = (
        sales.groupby("day_name")["units_sold"]
        .sum()
        .reindex(day_order)
    )

    fig, ax = plt.subplots(figsize=(8,5))

    day_sales.plot(
        kind="bar",
        color="royalblue",
        ax=ax
    )

    ax.set_ylabel("Units Sold")

    st.pyplot(fig)

    # ======================================
    # Monthly Sales Table
    # ======================================

    st.subheader("📋 Monthly Sales Summary")

    summary = monthly_sales.reset_index()

    summary.columns = ["Month", "Units Sold"]

    st.dataframe(summary)

    # ======================================
    # Business Insights
    # ======================================

    st.subheader("💡 Seasonal Insights")

    st.success(
        f"🏆 Highest demand occurs in **{peak_month}** with **{peak_sales:,} units sold**."
    )

    st.warning(
        f"📉 Lowest demand occurs in **{low_month}** with **{low_sales:,} units sold**."
    )

    st.info("""
    **Recommendations:**
    - Increase inventory before high-demand months.
    - Run promotional campaigns during low-demand months.
    - Plan procurement using seasonal demand patterns.
    - Align staffing and logistics with expected sales peaks.
    """)