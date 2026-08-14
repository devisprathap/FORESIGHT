


import streamlit as st

from dashboard_pages import company_overview
from dashboard_pages import sales_performance
from dashboard_pages import customer_demand
from dashboard_pages import product_performance
from dashboard_pages import inventory_health
from dashboard_pages import stock_risk
from dashboard_pages import promotion_analysis
from dashboard_pages import seasonality
from dashboard_pages import forecast
from dashboard_pages import executive_summary
from dashboard_pages import recommendation
import streamlit as st


st.set_page_config(
    page_title="Project FORESIGHT",
    page_icon="📊",
    layout="wide"
)





st.markdown("""
<style>

/* Hide Streamlit's default page navigation */
[data-testid="stSidebarNav"] {
    display: none;
}

/* Your existing sidebar color */
[data-testid="stSidebar"]{
    background:#1565C0;
}

[data-testid="stSidebar"] *{
    color:white;
}

</style>
""", unsafe_allow_html=True)






st.markdown("""
<style>
.main{
background:#F4F9FF;
}

h1{
color:#1565C0;
text-align:center;
}

[data-testid="stSidebar"]{
background:#1565C0;
}

[data-testid="stSidebar"] *{
color:white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📊 PROJECT FORESIGHT</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Demand Forecasting & Inventory Intelligence</h3>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    [
        "Company Overview",
        "Sales Performance",
        "Customer Demand",
        "Product Performance",
        "Inventory Health",
        "Stock Risk",
        "Promotion Analysis",
        "Seasonality",
        "Forecast",
        "Executive Summary",
        "Recommendation"
    ]
)

if page == "Company Overview":
    company_overview.show()

elif page == "Sales Performance":
    sales_performance.show()

elif page == "Customer Demand":
    customer_demand.show()

elif page == "Product Performance":
    product_performance.show()

elif page == "Inventory Health":
    inventory_health.show()

elif page == "Stock Risk":
    stock_risk.show()

elif page == "Promotion Analysis":
    promotion_analysis.show()

elif page == "Seasonality":
    seasonality.show()

elif page == "Forecast":
    forecast.show()

elif page == "Executive Summary":
    executive_summary.show()

elif page == "Recommendation":
    recommendation.show()