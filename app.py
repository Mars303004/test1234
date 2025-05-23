import streamlit as st
import pandas as pd
import plotly.express as px

# HARUS DIPANGGIL DI AWAL
st.set_page_config(
    layout="wide",
    page_title="BU1 Dashboard",
    page_icon="📊"
)

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

# =================== Layout Dashboard ===================
def main():
    # Header
    st.markdown("<h1 style='color:#0057c8; border-bottom: 2px solid #b42020; padding-bottom:10px'>BU1 Performance</h1>", 
               unsafe_allow_html=True)
    
    # ========== Financial Perspective ==========
    with st.container():
        st.subheader("💰 Financial Perspective")
        cols = st.columns(4)
        
        with cols[0]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Revenue</div>
                <div class="metric-value">$3.2M</div>
                <div style="color:#00aa00">+15% vs LV</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Kolom lainnya...

if __name__ == "__main__":
    main()
