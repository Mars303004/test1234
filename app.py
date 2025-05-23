import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =================== Style Custom ===================
st.markdown("""
<style>
    .metric-card {
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px;
        background: white;
        border-left: 4px solid #0057c8;
    }
    .metric-title {
        color: #b42020;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #0057c8;
    }
</style>
""", unsafe_allow_html=True)

# =================== Data Dummy ===================
def generate_dummy_data():
    return {
        'financial': {
            'revenue': {'current': 3.2, 'target': 3.5, 'subdiv': {'PRODEV': 1.2, 'PD1': 0.8}},
            'gross_margin': {'current': 38, 'trend': [35, 36, 37, 38, 38.5, 39]},
            'ar_days': {'current': 32, 'subdiv': {'PRODEV': 28, 'PD1': 34}}
        },
        'customer': {
            'csat': {'current': 4.25, 'trend': [4.0, 4.1, 4.25, 4.3]},
            'nps': {'current': 42, 'subdiv': {'PRODEV': 45, 'PD1': 40}}
        }
    }

# =================== Komponen Visual ===================
def create_metric_card(title, value, comparison=None):
    html = f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {f'<div style="color:{"#00aa00" if "+" in comparison else "#b42020"}">{comparison}</div>' if comparison else ''}
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)

# =================== Layout Dashboard ===================
def main():
    st.set_page_config(layout="wide", page_title="BU1 Dashboard", page_icon="📊")
    data = generate_dummy_data()
    
    # Header
    st.markdown("<h1 style='color:#0057c8; border-bottom: 2px solid #b42020; padding-bottom:10px'>BU1 Performance</h1>", 
               unsafe_allow_html=True)
    
    # ========== Financial Perspective ==========
    with st.container():
        st.subheader("💰 Financial Perspective")
        cols = st.columns(4)
        
        with cols[0]:
            if create_metric_card("Revenue", "$3.2M", "+15% vs LV"):
                with st.expander("", expanded=True):
                    tabs = st.tabs(["PRODEV", "PD1", "PD2"])
                    with tabs[0]:
                        fig = px.bar(x=["Q1", "Q2", "Q3"], y=[1.0, 1.2, 1.4])
                        st.plotly_chart(fig, use_container_width=True)
        
        with cols[1]:
            create_metric_card("Gross Margin", "38%", "+2% vs LV")
        
        with cols[2]:
            create_metric_card("AR Days", "32", "-3 days")
        
        with cols[3]:
            create_metric_card("Cost/Project", "$42K", "+5%")

    # ========== Customer Perspective ==========
    with st.container():
        st.subheader("👥 Customer & Service")
        cols = st.columns(3)
        
        with cols[0]:
            create_metric_card("CSAT", "4.25", "+0.3")
        
        with cols[1]:
            create_metric_card("NPS", "42", "+5")
        
        with cols[2]:
            create_metric_card("SLA", "96%", "+5%")

    # ========== Quality Perspective ==========
    with st.container():
        st.subheader("⚙️ Quality Metrics")
        cols = st.columns(3)
        
        with cols[0]:
            create_metric_card("Uptime", "99.95%", "+0.5%")
        
        with cols[1]:
            create_metric_card("Defect Rate", "1.2%", "-0.5%")
        
        with cols[2]:
            create_metric_card("Resolution", "97.2%", "+1.5%")

    # ========== Employee Perspective ==========
    with st.container():
        st.subheader("👨💻 Employee Fulfillment")
        cols = st.columns(4)
        
        with cols[0]:
            create_metric_card("Engagement", "7.8/10", "-0.4")
        
        with cols[1]:
            create_metric_card("Attrition", "8.2%", "+1.5%")
        
        with cols[2]:
            create_metric_card("Training", "42h", "+9%")
        
        with cols[3]:
            create_metric_card("Overtime", "3.2h", "+8.8h")

if __name__ == "__main__":
    main()
