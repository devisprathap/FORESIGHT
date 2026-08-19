import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():

    # ============================================
    # Load Data
    # ============================================

    sales = pd.read_csv("data/processed/feature_engineered_sales.csv")

    sales["date"] = pd.to_datetime(sales["date"])

    # ============================================
    # Dashboard Title
    # ============================================

    st.title(" Sales Performance Dashboard")

    st.write("""
    This dashboard analyzes sales performance over time,
    helping understand sales trends and business growth.
    """)

    # ============================================
    # KPI Cards
    # ============================================

    total_sales = sales["units_sold"].sum()

    avg_daily_sales = sales["units_sold"].mean()

    total_transactions = len(sales)

    total_skus = sales["sku_id"].nunique()

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    col1.metric(" Total Units Sold", f"{int(total_sales):,}")

    col2.metric(" Average Daily Sales", f"{avg_daily_sales:.2f}")

    col3.metric(" Total Sales Records", total_transactions)

    col4.metric(" Total Products", total_skus)

    # ============================================
    # Monthly Sales Trend
    # ============================================

    st.subheader(" Monthly Sales Trend")

    sales["month"] = sales["date"].dt.month

    monthly_sales = sales.groupby("month")["units_sold"].sum()

    fig, ax = plt.subplots(figsize=(10,5))

    monthly_sales.plot(marker="o", linewidth=3, ax=ax)

    ax.set_xlabel("Month")
    ax.set_ylabel("Units Sold")
    ax.set_title("Monthly Sales Trend")

    st.pyplot(fig)

    # ============================================
    # Weekly Sales Trend
    # ============================================

    st.subheader(" Weekly Sales Trend")

    sales["week"] = sales["date"].dt.isocalendar().week

    weekly_sales = sales.groupby("week")["units_sold"].sum()

    fig, ax = plt.subplots(figsize=(10,5))

    weekly_sales.plot(marker="o", color="green", ax=ax)

    ax.set_xlabel("Week")
    ax.set_ylabel("Units Sold")
    ax.set_title("Weekly Sales Trend")

    st.pyplot(fig)

    # ============================================
    # Daily Sales Trend
    # ============================================

    st.subheader(" Daily Sales Trend")

    daily_sales = sales.groupby("date")["units_sold"].sum()

    fig, ax = plt.subplots(figsize=(12,5))

    daily_sales.plot(color="orange", ax=ax)

    ax.set_xlabel("Date")
    ax.set_ylabel("Units Sold")
    ax.set_title("Daily Sales")

    st.pyplot(fig)

    # ============================================
    # Highest & Lowest Month
    # ============================================

    highest_month = monthly_sales.idxmax()
    highest_value = monthly_sales.max()

    lowest_month = monthly_sales.idxmin()
    lowest_value = monthly_sales.min()

    st.subheader(" Sales Highlights")

    col1, col2 = st.columns(2)

    col1.success(
        f"Highest Sales Month : Month {highest_month}\n\nUnits Sold : {highest_value:,}"
    )

    col2.error(
        f"Lowest Sales Month : Month {lowest_month}\n\nUnits Sold : {lowest_value:,}"
    )

    # ============================================
    # Monthly Sales Table
    # ============================================

    st.subheader(" Monthly Sales Summary")

    monthly_df = monthly_sales.reset_index()

    monthly_df.columns = ["Month", "Units Sold"]

    st.dataframe(monthly_df)

    # ============================================
    # Business Insights
    # ============================================

    st.subheader(" Business Insights")

    st.success(f" /Peak Sales Month : {highest_month}")

    st.warning(f" Lowest Sales Month : {lowest_month}")

    st.info(f" Total Units Sold : {total_sales:,}")

    st.info(f"Average Daily Sales : {avg_daily_sales:.2f}")