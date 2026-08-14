import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():

    st.title("🎯 Promotion Analysis")

    st.write("""
    Analyze the impact of promotional campaigns on product demand
    and sales performance.
    """)

    # ======================================
    # Load Data
    # ======================================

    sales = pd.read_csv("data/processed/feature_engineered_sales.csv")
    sku = pd.read_csv("data/processed/cleaned_sku_master.csv")

    merged = sales.merge(sku, on="sku_id")

    # ======================================
    # Promotion Summary
    # ======================================

    promo_sales = merged[merged["promo_flag"] == 1]["units_sold"].sum()
    nonpromo_sales = merged[merged["promo_flag"] == 0]["units_sold"].sum()

    promo_records = (merged["promo_flag"] == 1).sum()
    nonpromo_records = (merged["promo_flag"] == 0).sum()

    col1, col2 = st.columns(2)

    col1.metric("🎯 Promotion Sales", f"{int(promo_sales):,}")

    col2.metric("📦 Non-Promotion Sales", f"{int(nonpromo_sales):,}")

    col3, col4 = st.columns(2)

    col3.metric("Promotion Records", promo_records)

    col4.metric("Non-Promotion Records", nonpromo_records)

    # ======================================
    # Sales Comparison
    # ======================================

    st.subheader("📊 Promotion vs Non-Promotion Sales")

    comparison = pd.Series({
        "Promotion": promo_sales,
        "No Promotion": nonpromo_sales
    })

    fig, ax = plt.subplots(figsize=(6,4))

    comparison.plot(kind="bar", color=["royalblue","orange"], ax=ax)

    ax.set_ylabel("Units Sold")

    st.pyplot(fig)

    # ======================================
    # Category-wise Promotion Sales
    # ======================================

    st.subheader("📦 Promotion Sales by Category")

    category_sales = (
        merged[merged["promo_flag"] == 1]
        .groupby("category")["units_sold"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8,5))

    category_sales.plot(kind="bar", color="steelblue", ax=ax)

    ax.set_xlabel("Category")
    ax.set_ylabel("Units Sold")

    st.pyplot(fig)

    # ======================================
    # Average Demand Comparison
    # ======================================

    st.subheader("📈 Average Demand")

    avg = merged.groupby("promo_flag")["units_sold"].mean()

    fig, ax = plt.subplots(figsize=(6,4))

    avg.index = ["No Promotion", "Promotion"]

    avg.plot(kind="bar", color=["gray","green"], ax=ax)

    ax.set_ylabel("Average Units Sold")

    st.pyplot(fig)

    # ======================================
    # Promotion Summary Table
    # ======================================

    st.subheader("📋 Promotion Summary")

    summary = pd.DataFrame({

        "Metric":[
            "Promotion Sales",
            "Non-Promotion Sales",
            "Average Promotion Demand",
            "Average Non-Promotion Demand"
        ],

        "Value":[
            promo_sales,
            nonpromo_sales,
            round(avg["Promotion"],2),
            round(avg["No Promotion"],2)
        ]

    })

    st.dataframe(summary)

    # ======================================
    # Business Insights
    # ======================================

    st.subheader("💡 Business Insights")

    if promo_sales > nonpromo_sales:

        st.success(
            "✅ Promotions generated higher sales than non-promotional periods."
        )

    else:

        st.warning(
            "⚠ Promotions did not outperform non-promotional sales."
        )

    best_category = category_sales.idxmax()

    st.info(f"🏆 Best Promotion Category: {best_category}")