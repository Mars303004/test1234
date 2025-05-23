import streamlit as st
import pandas as pd
import plotly.express as px

# Load all BU data from a single CSV
all_data = pd.read_csv("/mnt/data/data.csv")

# Sidebar filters
st.sidebar.title("Filter")
selected_month = st.sidebar.selectbox("Pilih Bulan", sorted(all_data['Bulan'].unique()))
selected_bu = st.sidebar.radio("Pilih BU", ["BU1", "BU2", "BU3"])

# Filter data
df = all_data[(all_data['BU'] == selected_bu) & (all_data['Bulan'] == selected_month)]

# Perspective and KPI structure
perspectives = {
    "1. Financial": [
        "Revenue", "Revenue vs Target", "Gross Margin", "Cost per Project", "AR Days"
    ],
    "2. Customer & Service": [
        "Customer Satisfaction (CSAT)", "Net Promoter Score (NPS)", "SLA Achievement Rate",
        "Average Response Time", "Retention Rate"
    ],
    "3. Quality (Product & Service)": [
        "Defect Rate", "Uptime / System Availability", "Rework Rate",
        "Resolution Success Rate", "Code Review Coverage"
    ],
    "4. Employee Fulfillment": [
        "Employee Engagement Score", "Attrition Rate", "Training Hours per Employee",
        "Overtime per FTE", "Internal Promotion Rate"
    ]
}

# Header
st.markdown(f"<h2 style='text-align: center;'>📊 {selected_bu} Performance</h2>", unsafe_allow_html=True)

# Function to create a grid of KPIs per perspective
def display_kpis(perspective, kpis):
    st.markdown(f"<h4 style='margin-top: 20px; color: #0f098e'>{perspective}</h4>", unsafe_allow_html=True)
    cols = st.columns(len(kpis))
    for col, kpi in zip(cols, kpis):
        with col:
            if st.button(kpi, key=kpi):
                st.session_state['popup_kpi'] = kpi
                st.session_state['popup_perspective'] = perspective

# Display all perspectives with KPIs
for perspective, kpis in perspectives.items():
    display_kpis(perspective, kpis)

# Pop-up simulation (placeholder for modal)
if 'popup_kpi' in st.session_state:
    st.markdown("""
        <style>
        .popup { position: fixed; top: 10%; left: 10%; width: 80%; height: 80%; background: white; 
                 border: 2px solid #000; padding: 20px; z-index: 1000; overflow: auto; }
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.3); 
                   z-index: 999; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="popup">', unsafe_allow_html=True)
        st.markdown(f"### {st.session_state['popup_kpi']} ({selected_bu})")

        # Determine subdivs by perspective and KPI
        subdivs = []
        p = st.session_state['popup_perspective']
        k = st.session_state['popup_kpi']
        if p == "1. Financial":
            subdivs = ["PRODEV", "PD1", "PD2", "DOCS", "ITS", "CHAPTER"]
        elif p == "2. Customer & Service":
            subdivs = ["PRODEV", "PD1", "PD2", "DOCS"]
        elif p == "3. Quality (Product & Service)":
            subdivs = ["ITS"] if k == "Uptime / System Availability" else ["PRODEV", "PD1", "PD2", "DOCS"]
        elif p == "4. Employee Fulfillment":
            subdivs = ["CHAPTER"]

        selected_subdiv = st.selectbox("Pilih Subdiv", subdivs)
        chart_df = df[(df['Perspective'] == p.split('. ')[1]) & (df['KPI'] == k) & (df['Subdiv'] == selected_subdiv)]

        # Dummy chart visualization (replace with real logic)
        if not chart_df.empty:
            fig = px.line(chart_df, x="Bulan", y="Value", title=f"Trend {k} ({selected_subdiv})")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Data tidak tersedia untuk KPI dan subdiv ini.")

        if st.button("Tutup"):
            del st.session_state['popup_kpi']
            del st.session_state['popup_perspective']

        st.markdown('</div>', unsafe_allow_html=True)
