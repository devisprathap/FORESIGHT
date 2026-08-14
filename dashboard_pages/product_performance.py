import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():

    st.title("📦 Product Performance Dashboard")

    st.write("""
    Analyze the performance of individual products and categories
    based on sales data.
    """)

    # ===============================
    # Load Data
    # ===============================

    sales = pd.read_csv("data/processed/feature_engineered_sales.csv")
    sku = pd.read_csv("data/processed/cleaned_sku_master.csv")

    merged = sales.merge(sku, on="sku_id")

    # ===============================
    # Product Sales
    # ===============================

    product_sales = (
        merged.groupby("sku_id")["units_sold"]
        .sum()
        .sort_values(ascending=False)
    )

    best_sku = product_sales.idxmax()
    best_units = product_sales.max()

    worst_sku = product_sales.idxmin()
    worst_units = product_sales.min()

    total_products = merged["sku_id"].nunique()
    avg_sales = product_sales.mean()

    # ===============================
    # KPI Cards
    # ===============================

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    col1.metric("🏆 Best Selling SKU", best_sku)

    col2.metric("📉 Lowest Selling SKU", worst_sku)

    col3.metric("📦 Total Products", total_products)

    col4.metric("📊 Average Sales per SKU", round(avg_sales,2))

    # ===============================
    # Top 10 Products
    # ===============================

    st.subheader("🔥 Top 10 Products")

    fig, ax = plt.subplots(figsize=(10,5))

    product_sales.head(10).plot(
        kind="bar",
        color="royalblue",
        ax=ax
    )

    ax.set_xlabel("SKU")
    ax.set_ylabel("Units Sold")
    ax.set_title("Top 10 Products")

    st.pyplot(fig)

    # ===============================
    # Bottom 10 Products
    # ===============================

    st.subheader("📉 Bottom 10 Products")

    fig, ax = plt.subplots(figsize=(10,5))

    product_sales.tail(10).plot(
        kind="bar",
        color="tomato",
        ax=ax
    )

    ax.set_xlabel("SKU")
    ax.set_ylabel("Units Sold")
    ax.set_title("Bottom 10 Products")

    st.pyplot(fig)

    # ===============================
    # Category Performance
    # ===============================

    st.subheader("📊 Category Performance")

    category_sales = (
        merged.groupby("category")["units_sold"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8,5))

    category_sales.plot(
        kind="bar",
        color="steelblue",
        ax=ax
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Units Sold")

    st.pyplot(fig)

    # ===============================
    # Category Distribution
    # ===============================

    st.subheader("🥧 Category Sales Distribution")

    fig, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        category_sales,
        labels=category_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )

    st.pyplot(fig)

    # ===============================
    # Product Performance Table
    # ===============================

    st.subheader("📋 Product Performance Table")

    performance = (
        merged.groupby(["sku_id","category"])["units_sold"]
        .sum()
        .reset_index()
        .sort_values("units_sold", ascending=False)
    )

    st.dataframe(performance)

    # ===============================
    # Business Insights
    # ===============================

    st.subheader("💡 Business Insights")

    st.success(
        f"🏆 Best Selling Product : {best_sku} ({best_units} units)"
    )

    st.warning(
        f"📉 Lowest Selling Product : {worst_sku} ({worst_units} units)"
    )

    st.info(
        f"📦 Total Products : {total_products}"
    )

    st.info(
        f"📊 Average Sales per Product : {avg_sales:.2f}"
    )