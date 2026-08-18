import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():

    st.title(" Inventory Health Dashboard")

    st.write("""
    This dashboard provides insights into the current inventory status,
    helping identify inventory availability and stock distribution.
    """)

    # ==========================================
    # Load Data
    # ==========================================

    inventory = pd.read_csv("data/processed/cleaned_inventory_snapshots.csv")
    sku = pd.read_csv("data/processed/cleaned_sku_master.csv")

    # Merge inventory with SKU details
    merged = inventory.merge(sku, on="sku_id")

    # ==========================================
    # KPI Cards
    # ==========================================

    total_inventory = merged["on_hand_units"].sum()

    average_inventory = merged["on_hand_units"].mean()

    total_skus = merged["sku_id"].nunique()

    low_stock = merged[merged["on_hand_units"] < 20].shape[0]

    high_stock = merged[merged["on_hand_units"] > 200].shape[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(" Total Inventory", f"{int(total_inventory):,}")

    col2.metric(" Average Inventory", f"{average_inventory:.2f}")

    col3.metric(" Total SKUs", total_skus)

    col4, col5 = st.columns(2)

    col4.metric(" Low Stock Items", low_stock)

    col5.metric(" High Stock Items", high_stock)

    # ==========================================
    # Inventory by Category
    # ==========================================

    st.subheader(" Inventory by Category")

    category_inventory = (
        merged.groupby("category")["on_hand_units"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8,5))

    category_inventory.plot(kind="bar", color="steelblue", ax=ax)

    ax.set_xlabel("Category")
    ax.set_ylabel("Inventory Units")

    st.pyplot(fig)

    # ==========================================
    # Top 10 Inventory SKUs
    # ==========================================

    st.subheader(" Top 10 Inventory SKUs")

    top_inventory = (
        merged.groupby("sku_id")["on_hand_units"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10,5))

    top_inventory.plot(kind="bar", color="royalblue", ax=ax)

    ax.set_xlabel("SKU ID")
    ax.set_ylabel("Inventory Units")

    st.pyplot(fig)

    st.dataframe(top_inventory.reset_index())

    # ==========================================
    # Inventory Distribution
    # ==========================================

    st.subheader(" Inventory Distribution")

    fig, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        category_inventory,
        labels=category_inventory.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Inventory Distribution by Category")

    st.pyplot(fig)

    # ==========================================
    # Inventory Summary Table
    # ==========================================

    st.subheader(" Inventory Summary")

    summary = pd.DataFrame({

        "Metric":[
            "Total Inventory",
            "Average Inventory",
            "Low Stock Items",
            "High Stock Items",
            "Total SKUs"
        ],

        "Value":[
            int(total_inventory),
            round(average_inventory,2),
            low_stock,
            high_stock,
            total_skus
        ]

    })

    st.dataframe(summary)

    # ==========================================
    # Business Insights
    # ==========================================

    st.subheader(" Business Insights")

    highest_category = category_inventory.idxmax()

    lowest_category = category_inventory.idxmin()

    st.success(f" Highest Inventory Category : {highest_category}")

    st.warning(f" Lowest Inventory Category : {lowest_category}")

    st.info(f" Low Stock Items : {low_stock}")

    st.info(f"🟢 High Stock Items : {high_stock}")
