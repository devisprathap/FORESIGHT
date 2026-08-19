import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():

    # -----------------------------
    # Load Data
    # -----------------------------
    sales = pd.read_csv("data/processed/feature_engineered_sales.csv")
    sku = pd.read_csv("data/processed/cleaned_sku_master.csv")
    inventory = pd.read_csv("data/processed/cleaned_inventory_snapshots.csv")
    risk = pd.read_csv("data/processed/risk_report.csv")

    # -----------------------------
    # Dashboard Title
    # -----------------------------
    st.title(" Company Overview")

    st.write(
        """
        Welcome to **Project FORESIGHT**.

        This dashboard provides an overview of NorthBay Living's sales,
        inventory, customer demand and stock risks.
        """
    )

    # -----------------------------
    # Calculate KPIs
    # -----------------------------
    total_units = sales["units_sold"].sum()

    total_skus = sales["sku_id"].nunique()

    total_categories = sku["category"].nunique()

    total_inventory = inventory["on_hand_units"].sum()

    stockout = (risk["risk_status"] == "Stockout Risk").sum()

    overstock = (risk["risk_status"] == "Overstock").sum()

    # -----------------------------
    # KPI Cards
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric(" Total Units Sold", f"{total_units:,}")

    col2.metric(" Total SKUs", total_skus)

    col3.metric(" Categories", total_categories)

    col4, col5, col6 = st.columns(3)

    col4.metric(" Inventory Units", f"{total_inventory:,}")

    col5.metric(" Stockout Risk", stockout)

    col6.metric(" Overstock", overstock)

    # -----------------------------
    # Sales by Category
    # -----------------------------
    st.subheader(" Sales by Category")

    merged = sales.merge(sku, on="sku_id")

    category_sales = merged.groupby("category")["units_sold"].sum()

    fig, ax = plt.subplots(figsize=(8,4))

    category_sales.plot(kind="bar", ax=ax)

    ax.set_xlabel("Category")

    ax.set_ylabel("Units Sold")

    st.pyplot(fig)

    # -----------------------------
    # Business Snapshot
    # -----------------------------
    st.subheader(" Business Snapshot")

    snapshot = pd.DataFrame({

        "Metric":[
            "Total Units Sold",
            "Total SKUs",
            "Categories",
            "Inventory Units",
            "Stockout Risks",
            "Overstock"
        ],

        "Value":[
            total_units,
            total_skus,
            total_categories,
            total_inventory,
            stockout,
            overstock
        ]

    })

    st.dataframe(snapshot)

    # -----------------------------
    # Business Highlights
    # -----------------------------
    st.subheader(" Business Highlights")

    best_category = category_sales.idxmax()

    st.success(f" Best Selling Category : {best_category}")

    st.info(f" Total Inventory Units : {total_inventory:,}")

    st.warning(f" Stockout Risks : {stockout}")

    st.error(f" Overstock Items : {overstock}")