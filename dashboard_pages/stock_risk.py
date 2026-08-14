import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():

    st.title("⚠️ Stock Risk Dashboard")

    st.write("""
    Analyze products that are at risk of stockout or overstock
    to support inventory planning and replenishment decisions.
    """)

    # ======================================
    # Load Data
    # ======================================

    risk = pd.read_csv("data/processed/risk_report.csv")
    sku = pd.read_csv("data/processed/cleaned_sku_master.csv")

    merged = risk.merge(sku, on="sku_id")

    # ======================================
    # KPI Cards
    # ======================================

    stockout = (merged["risk_status"] == "Stockout Risk").sum()
    overstock = (merged["risk_status"] == "Overstock").sum()
    healthy = (merged["risk_status"] == "Healthy").sum()

    total_products = merged["sku_id"].nunique()

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    col1.metric("⚠️ Stockout Risk", stockout)
    col2.metric("📦 Overstock", overstock)
    col3.metric("✅ Healthy Products", healthy)
    col4.metric("🛒 Total Products", total_products)

    # ======================================
    # Risk Distribution
    # ======================================

    st.subheader("📊 Risk Distribution")

    risk_counts = merged["risk_status"].value_counts()

    fig, ax = plt.subplots(figsize=(7,5))

    risk_counts.plot(
        kind="bar",
        color=["green", "red", "orange"],
        ax=ax
    )

    ax.set_xlabel("Risk Status")
    ax.set_ylabel("Number of Products")

    st.pyplot(fig)

    # ======================================
    # Risk Percentage
    # ======================================

    st.subheader("🥧 Risk Percentage")

    fig, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        risk_counts,
        labels=risk_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    st.pyplot(fig)

    # ======================================
    # Category-wise Risk
    # ======================================

    st.subheader("📦 Risk by Category")

    category_risk = (
        merged.groupby(["category", "risk_status"])
        .size()
        .unstack(fill_value=0)
    )

    st.dataframe(category_risk)

    category_risk.plot(
        kind="bar",
        figsize=(10,5)
    )

    plt.ylabel("Products")

    st.pyplot(plt)

    # ======================================
    # Detailed Risk Report
    # ======================================

    st.subheader("📋 Detailed Risk Report")

    st.dataframe(
        merged.sort_values("risk_status")
    )

    # ======================================
    # Recommendations
    # ======================================

    st.subheader("💡 Recommendations")

    if stockout > 0:
        st.error(
            f"⚠️ {stockout} products are at Stockout Risk. Replenishment is recommended."
        )

    if overstock > 0:
        st.warning(
            f"📦 {overstock} products are Overstocked. Consider promotions or discounts."
        )

    if healthy > 0:
        st.success(
            f"✅ {healthy} products currently have healthy inventory levels."
        )

    st.info("""
    • Increase inventory for products with Stockout Risk.

    • Reduce purchase quantities for Overstock items.

    • Review inventory weekly.

    • Use demand forecasting to optimize stock levels.
    """)