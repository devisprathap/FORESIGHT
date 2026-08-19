import streamlit as st
import pandas as pd

def show():

    st.title(" Business Recommendations")

    st.write("""
    This page provides inventory and sales recommendations
    based on the demand forecast and stock risk analysis.
    """)

    # ==========================================
    # Load Data
    # ==========================================

    sales = pd.read_csv("data/processed/feature_engineered_sales.csv")
    risk = pd.read_csv("data/processed/risk_report.csv")
    sku = pd.read_csv("data/processed/cleaned_sku_master.csv")

    merged = risk.merge(sku, on="sku_id")

    # ==========================================
    # Calculate KPIs
    # ==========================================

    stockout_count = (risk["risk_status"] == "Stockout Risk").sum()

    overstock_count = (risk["risk_status"] == "Overstock").sum()

    healthy_count = (risk["risk_status"] == "Healthy").sum()

    total_sales = sales["units_sold"].sum()

    total_skus = sales["sku_id"].nunique()

    # ==========================================
    # KPI Cards
    # ==========================================

    col1, col2, col3 = st.columns(3)

    col1.metric(" Total Sales", f"{int(total_sales):,}")

    col2.metric(" Total Products", total_skus)

    col3.metric(" Total Risk Items", stockout_count + overstock_count)

    # ==========================================
    # Risk Summary
    # ==========================================

    st.subheader(" Inventory Risk Summary")

    summary = pd.DataFrame({

        "Risk Status":[
            "Healthy",
            "Stockout Risk",
            "Overstock"
        ],

        "Count":[
            healthy_count,
            stockout_count,
            overstock_count
        ]

    })

    st.dataframe(summary)

    # ==========================================
    # Recommendations
    # ==========================================

    st.subheader(" Business Recommendations")

    st.success("""
    Increase replenishment frequency for products
    identified as Stockout Risk.
    """)

    st.warning("""
    Reduce procurement of Overstock items and
    prioritize clearance promotions.
    """)

    st.info("""
    Use demand forecasts to optimize inventory
    planning for upcoming months.
    """)

    st.info("""
    Increase safety stock for high-demand products
    to minimize lost sales.
    """)

    st.info("""
    Monitor low-performing products and evaluate
    whether to discontinue or promote them.
    """)

    # ==========================================
    # Executive Summary
    # ==========================================

    st.subheader(" Executive Summary")

    st.markdown(f"""
    - **Total Units Sold:** **{int(total_sales):,}**
    - **Total Products:** **{total_skus}**
    - **Healthy Products:** **{healthy_count}**
    - **Stockout Risk Products:** **{stockout_count}**
    - **Overstock Products:** **{overstock_count}**

    ### Key Actions

    ✔ Increase stock for products with high forecasted demand.

    ✔ Reduce excess inventory through promotional campaigns.

    ✔ Review slow-moving products regularly.

    ✔ Monitor inventory health using the dashboard.

    ✔ Use AI demand forecasts to improve procurement planning.
    """)

    # ==========================================
    # Final Message
    # ==========================================

    st.success("""
     Project FORESIGHT enables data-driven inventory planning,
    reduces stockouts, minimizes overstock, and supports
    smarter business decisions through predictive analytics.
    """)