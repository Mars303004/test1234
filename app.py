import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(layout="wide")

# Load data
df = pd.read_csv('data.csv')

# Sidebar
st.sidebar.title('Dashboard Controls')
selected_month = st.sidebar.slider('Select Month', 1, 12, 1)
selected_bu = st.sidebar.radio('Select Business Unit', ['BU1', 'BU2', 'BU3'])

# Main content
st.title(f'{selected_bu} Performance Dashboard')

# Create 4 columns for the perspectives
col1, col2, col3, col4 = st.columns(4)

# 1. Financial Perspective
with col1:
    st.subheader('Financial')
    metrics = ['Revenue', 'Revenue vs Target', 'Gross Margin', 'Cost per Project', 'AR Days']
    
    for metric in metrics:
        value = df[(df['BU'] == selected_bu) & (df['Metric'] == metric) & (df['Month'] == selected_month)]['Value'].values
        value = value[0] if len(value) > 0 else 0
        metric_container = st.container()
        
        with metric_container:
            if st.button(f'{metric}: {value}', key=f'fin_{metric}'):
                subdiv_tab = st.tabs(['PRODEV', 'PD1', 'PD2', 'DOCS', 'ITS', 'CHAPTER'])
                with subdiv_tab[0]:
                    # Example visualization
                    fig = go.Figure()
                    if metric == 'Revenue':
                        fig = px.bar(df[df['Metric'] == metric], x='Month', y='Value', color='BU', title=f'{metric} Trend')
                    elif metric == 'Revenue vs Target':
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = value,
                            title = {'text': metric},
                            gauge = {'axis': {'range': [0, 100]}}
                        ))
                    st.plotly_chart(fig, use_container_width=True)

# 2. Customer & Service
with col2:
    st.subheader('Customer & Service')
    metrics = ['CSAT', 'NPS', 'SLA Achievement Rate', 'Average Response Time', 'Retention Rate']
    
    for metric in metrics:
        value = df[(df['BU'] == selected_bu) & (df['Metric'] == metric) & (df['Month'] == selected_month)]['Value'].values
        value = value[0] if len(value) > 0 else 0
        metric_container = st.container()
        
        with metric_container:
            if st.button(f'{metric}: {value}', key=f'cust_{metric}'):
                subdiv_tab = st.tabs(['PRODEV', 'PD1', 'PD2', 'DOCS'])
                with subdiv_tab[0]:
                    fig = go.Figure()
                    if metric == 'CSAT':
                        fig = px.line(df[df['Metric'] == metric], x='Month', y='Value', color='BU', title=f'{metric} Trend')
                    elif metric == 'NPS':
                        fig = px.scatter(df[df['Metric'] == metric], x='Month', y='Value', title=f'{metric} Trend')
                    st.plotly_chart(fig, use_container_width=True)

# 3. Quality
with col3:
    st.subheader('Quality')
    metrics = ['Defect Rate', 'Uptime', 'Rework Rate', 'Resolution Success Rate', 'Code Review Coverage']
    
    for metric in metrics:
        value = df[(df['BU'] == selected_bu) & (df['Metric'] == metric) & (df['Month'] == selected_month)]['Value'].values
        value = value[0] if len(value) > 0 else 0
        metric_container = st.container()
        
        with metric_container:
            if st.button(f'{metric}: {value}', key=f'qual_{metric}'):
                if metric == 'Uptime':
                    subdiv_tab = st.tabs(['ITS'])
                else:
                    subdiv_tab = st.tabs(['PRODEV', 'PD1', 'PD2', 'DOCS'])
                with subdiv_tab[0]:
                    fig = go.Figure()
                    if metric == 'Uptime':
                        fig = px.pie(names=['Uptime', 'Downtime'], values=[value, 100-value], hole=0.4)
                    elif metric == 'Defect Rate':
                        fig = px.area(df[df['Metric'] == metric], x='Month', y='Value', color='BU', title=f'{metric} Trend')
                    st.plotly_chart(fig, use_container_width=True)

# 4. Employee Fulfillment
with col4:
    st.subheader('Employee Fulfillment')
    metrics = ['Employee Engagement Score', 'Attrition Rate', 'Training Hours per Employee', 'Overtime per FTE', 'Internal Promotion Rate']
    
    for metric in metrics:
        value = df[(df['BU'] == selected_bu) & (df['Metric'] == metric) & (df['Month'] == selected_month)]['Value'].values
        value = value[0] if len(value) > 0 else 0
        metric_container = st.container()
        
        with metric_container:
            if st.button(f'{metric}: {value}', key=f'emp_{metric}'):
                subdiv_tab = st.tabs(['CHAPTER'])
                with subdiv_tab[0]:
                    fig = go.Figure()
                    if metric == 'Employee Engagement Score':
                        fig = px.bar(df[df['Metric'] == metric], x='Month', y='Value', color='BU', title=f'{metric} Trend')
                    elif metric == 'Training Hours per Employee':
                        fig = px.pie(df[df['Metric'] == metric], values='Value', names='BU', title=f'{metric} Distribution')
                    st.plotly_chart(fig, use_container_width=True)

def update_kpi_data(bu, metric, value, month):
    """Update KPI data for specific BU and metric"""
    mask = (df['BU'] == bu) & (df['Metric'] == metric) & (df['Month'] == month)
    df.loc[mask, 'Value'] = value
    df.to_csv('data.csv', index=False)
    st.success(f'Data updated for {bu} - {metric}')
