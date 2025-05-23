import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =================== Data Dummy Lengkap ===================
def generate_dummy_data():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    subdivisions = ['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER']
    
    data = {
        # Financial Perspective
        'revenue': {
            'current': 3.2, 
            'target': 3.5,
            'trend': [2.8, 3.0, 3.1, 3.2, 3.3, 3.4],
            'by_subdiv': {'PRODEV': 1.2, 'PD1': 0.8, 'PD2': 0.7, 'DOCS': 0.5}
        },
        'gross_margin': {
            'current': 38,
            'trend': [35, 36, 37, 38, 38.5, 39]
        },
        'ar_days': {
            'current': 32,
            'trend': [35, 34, 33, 32, 31, 30]
        },
        
        # Customer Perspective
        'csat': {
            'current': 4.25,
            'trend': [4.0, 4.1, 4.2, 4.25, 4.3, 4.35],
            'by_bu': {'BU1': 4.25, 'BU2': 4.1, 'BU3': 4.0}
        },
        'nps': {
            'current': 42,
            'trend': [38, 40, 41, 42, 43, 44]
        },
        'sla': {
            'current': 96,
            'by_bu': {'BU1': 96, 'BU2': 92, 'BU3': 89}
        },
        
        # Quality Perspective
        'uptime': {
            'current': 99.95,
            'by_its': {'ITS1': 99.9, 'ITS2': 99.96, 'ITS3': 99.97}
        },
        'defect_rate': {
            'current': 1.2,
            'trend': [1.5, 1.4, 1.3, 1.2, 1.1, 1.0]
        },
        
        # Employee Perspective
        'engagement': {
            'current': 7.8,
            'by_chapter': {'Chapter A': 7.5, 'Chapter B': 8.1, 'Chapter C': 7.9}
        },
        'attrition': {
            'current': 8.2,
            'trend': [9.0, 8.5, 8.3, 8.2, 8.0, 7.8]
        }
    }
    
    return data

# =================== Visualisasi ===================
def create_gauge(value, title, min_val, max_val, target=None):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta" if target else "gauge+number",
        value = value,
        title = {'text': title},
        delta = {'reference': target} if target else None,
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "#0057c8"},
            'steps': [
                {'range': [min_val, max_val*0.8], 'color': "#f0f0f0"},
                {'range': [max_val*0.8, max_val], 'color': "#d3d3d3"}
            ]
        }
    ))
    return fig

def create_radar_chart(data, categories, title):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(data.values()),
        theta=categories,
        fill='toself',
        line_color='#0057c8'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), title=title)
    return fig

# =================== Dashboard ===================
def main():
    st.set_page_config(layout="wide", page_title="IT Company Dashboard", page_icon="📊")
    data = generate_dummy_data()
    
    # Sidebar
    with st.sidebar:
        st.header("Filters")
        selected_month = st.selectbox("Month", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
        selected_bu = st.radio("Business Unit", ["BU1", "BU2", "BU3"])
    
    # Header
    st.markdown(f"<h1 style='color:#0057c8;'>{selected_bu} Performance</h1>", unsafe_allow_html=True)
    
    # ========== Financial Perspective ==========
    with st.container():
        st.subheader("📈 Financial Perspective")
        cols = st.columns(5)
        
        # Revenue
        with cols[0]:
            st.metric("Revenue", f"${data['revenue']['current']}M", "+15% vs LV")
            if st.button("📊 Revenue", key="rev_btn"):
                st.session_state.selected_kpi = 'revenue'
        
        # Gross Margin
        with cols[1]:
            st.metric("Gross Margin", f"{data['gross_margin']['current']}%", "+2% vs LV")
            if st.button("📊 Gross Margin", key="gm_btn"):
                st.session_state.selected_kpi = 'gross_margin'
        
        # AR Days
        with cols[2]:
            st.metric("AR Days", data['ar_days']['current'], "-3 days vs LV")
            if st.button("📊 AR Days", key="ar_btn"):
                st.session_state.selected_kpi = 'ar_days'
        
        # Revenue vs Target
        with cols[3]:
            fig = create_gauge(
                (data['revenue']['current']/data['revenue']['target'])*100,
                "Revenue vs Target",
                0,
                120,
                100
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Trend Chart
        with cols[4]:
            fig = px.line(
                x=["Jan","Feb","Mar","Apr","May","Jun"],
                y=data['revenue']['trend'],
                title="Revenue Trend"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== Customer Perspective ==========
    with st.container():
        st.subheader("👥 Customer & Service")
        cols = st.columns(5)
        
        # CSAT
        with cols[0]:
            st.metric("CSAT", data['csat']['current'], "+0.3 vs LV")
            if st.button("📊 CSAT", key="csat_btn"):
                with st.expander("CSAT Details"):
                    fig = create_radar_chart(
                        data['csat']['by_bu'],
                        list(data['csat']['by_bu'].keys()),
                        "CSAT per BU"
                    )
                    st.plotly_chart(fig)
        
        # NPS
        with cols[1]:
            st.metric("NPS", data['nps']['current'], "+5 vs LV")
            if st.button("📊 NPS", key="nps_btn"):
                with st.expander("NPS Trend"):
                    fig = px.line(
                        x=months,
                        y=data['nps']['trend'],
                        title="NPS Trend"
                    )
                    st.plotly_chart(fig)
        
        # SLA
        with cols[2]:
            st.metric("SLA Achievement", f"{data['sla']['current']}%", "+5% vs LV")
        
        # Retention
        with cols[3]:
            st.metric("Retention Rate", "94%", "+5% vs LV")
        
        # Response Time
        with cols[4]:
            st.metric("Avg Response Time", "2.4h", "-0.8h vs LV")
    
    # ========== Quality Perspective ==========
    with st.container():
        st.subheader("⚙️ Quality Perspective")
        cols = st.columns(4)
        
        # Uptime
        with cols[0]:
            st.metric("System Uptime", f"{data['uptime']['current']}%", "+0.5% vs LV")
        
        # Defect Rate
        with cols[1]:
            st.metric("Defect Rate", f"{data['defect_rate']['current']}%", "-0.5% vs LV")
        
        # Resolution Rate
        with cols[2]:
            st.metric("Resolution Success", "97.2%", "+1.5% vs LV")
        
        # Rework Rate
        with cols[3]:
            st.metric("Rework Rate", "3.8%", "-0.6% vs LV")
    
    # ========== Employee Perspective ==========
    with st.container():
        st.subheader("👨💻 Employee Fulfillment")
        cols = st.columns(4)
        
        # Engagement
        with cols[0]:
            st.metric("Engagement Score", data['engagement']['current'], "-0.4 vs LV")
        
        # Attrition
        with cols[1]:
            st.metric("Attrition Rate", f"{data['attrition']['current']}%", "+1.5% vs LV")
        
        # Training Hours
        with cols[2]:
            st.metric("Training Hours", "42h", "+9% vs LV")
        
        # Overtime
        with cols[3]:
            st.metric("Overtime", "3.2h", "+8.8h vs LV")

if __name__ == "__main__":
    main()
