import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():

    # =====================================
    # Load Data
    # =====================================
    sales = pd.read_csv("data/processed/feature_engineered_sales.csv")
    sku = pd.read_csv("data/processed/cleaned_sku_master.csv")

    # Merge datasets
    merged = sales.merge(sku, on="sku_id")

    st.title(" Customer Demand Analysis")

    st.write(
        """
        This page analyzes customer demand by identifying the highest and
        lowest selling products and demand across product categories.
        """
    )

    # =====================================
    # Top 10 Products
    # =====================================

    st.subheader(" Top 10 Most Demanded Products")

    top_products = (
        merged.groupby("sku_id")["units_sold"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10,5))

    top_products.plot(kind="bar", color="royalblue", ax=ax)

    ax.set_xlabel("SKU ID")
    ax.set_ylabel("Units Sold")
    ax.set_title("Top 10 Products")

    st.pyplot(fig)

    st.dataframe(top_products.reset_index())

    # =====================================
    # Bottom 10 Products
    # =====================================

    st.subheader(" Bottom 10 Products")

    bottom_products = (
        merged.groupby("sku_id")["units_sold"]
        .sum()
        .sort_values()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10,5))

    bottom_products.plot(kind="bar", color="tomato", ax=ax)

    ax.set_xlabel("SKU ID")
    ax.set_ylabel("Units Sold")
    ax.set_title("Bottom 10 Products")

    st.pyplot(fig)

    st.dataframe(bottom_products.reset_index())

    # =====================================
    # Category-wise Demand
    # =====================================

    st.subheader(" Category-wise Demand")

    category_demand = (
        merged.groupby("category")["units_sold"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8,5))

    category_demand.plot(kind="bar", color="steelblue", ax=ax)

    ax.set_xlabel("Category")
    ax.set_ylabel("Units Sold")

    st.pyplot(fig)

    st.dataframe(category_demand.reset_index())

    # =====================================
    # Pie Chart
    # =====================================

    st.subheader(" Demand Share by Category")

    fig, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        category_demand,
        labels=category_demand.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Category Demand Share")

    st.pyplot(fig)

    # =====================================
    # Demand Summary
    # =====================================

    st.subheader(" Customer Demand Summary")

    total_units = merged["units_sold"].sum()

    best_category = category_demand.idxmax()

    worst_category = category_demand.idxmin()

    summary = pd.DataFrame({

        "Metric":[
            "Total Units Sold",
            "Best Selling Category",
            "Lowest Selling Category",
            "Number of Products"
        ],

        "Value":[
            total_units,
            best_category,
            worst_category,
            merged["sku_id"].nunique()
        ]

    })

    st.dataframe(summary)

    # =====================================
    # Business Insights
    # =====================================

    st.subheader(" Business Insights")

    st.success(f" Highest Demand Category : {best_category}")

    st.warning(f" Lowest Demand Category : {worst_category}")

    st.info(f" Total Units Sold : {total_units:,}")