import streamlit as st
import pandas as pd


def show():

    st.title(" Executive Summary")

    try:
        sales = pd.read_csv(
            "data/processed/feature_engineered_sales.csv"
        )

        inventory = pd.read_csv(
            "data/processed/cleaned_inventory_snapshots.csv"
        )

        risk = pd.read_csv(
            "data/processed/risk_report.csv"
        )

    except Exception as e:
        st.error("Error loading data")
        st.exception(e)
        return

    st.success("Executive Summary loaded successfully!")

    st.subheader(" Key Business Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Sales Records",
        f"{len(sales):,}"
    )

    col2.metric(
        "Inventory Records",
        f"{len(inventory):,}"
    )

    col3.metric(
        "Risk Records",
        f"{len(risk):,}"
    )

    st.divider()

    st.subheader(" Sales Data Preview")

    st.dataframe(
        sales.head(10),
        use_container_width=True
    )

    st.subheader(" Inventory Data Preview")

    st.dataframe(
        inventory.head(10),
        use_container_width=True
    )

    st.subheader("Risk Data Preview")

    st.dataframe(
        risk.head(10),
        use_container_width=True
    )

    st.success(
        "FORESIGHT analysis combines sales, demand and inventory "
        "information to support business decisions."
    )