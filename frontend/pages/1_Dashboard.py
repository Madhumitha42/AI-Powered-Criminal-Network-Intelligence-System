import streamlit as st
import plotly.express as px
import pandas as pd
import requests

st.set_page_config(page_title="Dashboard | Intelligence Platform", layout="wide")

st.markdown("## 📊 Investigation Command Dashboard")
st.caption("Real-Time Analytics & Cross-Case Intelligence Summary")

API_URL = "http://localhost:8000/api/v1"

# Fetch Cases & Entities from Backend or Fallback
try:
    res_cases = requests.get(f"{API_URL}/cases").json()
    res_entities = requests.get(f"{API_URL}/entities").json()
except Exception:
    res_cases = [
        {"case_id": "CASE-2026-001", "title": "Mumbai Armored Logistics", "crime_type": "Armed Theft", "status": "Under Investigation"},
        {"case_id": "CASE-2026-008", "title": "Pune Warehouse Raid", "crime_type": "Contraband", "status": "Under Investigation"},
        {"case_id": "CASE-2026-014", "title": "Thane Hawala Cash Trail", "crime_type": "Financial Fraud", "status": "Active"},
        {"case_id": "CASE-2026-021", "title": "Nashik Highway Interception", "crime_type": "Smuggling", "status": "Under Investigation"}
    ]
    res_entities = [
        {"type": "Person"}, {"type": "Person"}, {"type": "Vehicle"}, {"type": "Vehicle"},
        {"type": "Location"}, {"type": "Communication"}, {"type": "Organization"}
    ]

# Row 1: High Level Stats
c1, c2, c3, c4 = st.columns(4)
c1.metric("Active Cases", len(res_cases), delta="+2 this week")
c2.metric("Total Extracted Entities", len(res_entities), delta="+14 new")
c3.metric("Cross-Case Patterns", "4 High Severity", delta="2 pending review")
c4.metric("AI Confidence Score", "94.2%", delta="+1.5%")

st.markdown("---")

# Row 2: Analytics Charts
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 🏷️ Case Breakdown by Crime Type")
    df_cases = pd.DataFrame(res_cases)
    if not df_cases.empty and 'crime_type' in df_cases.columns:
        fig_crime = px.pie(
            df_cases, names='crime_type', hole=0.4,
            color_discrete_sequence=['#00F0FF', '#9D00FF', '#00FF88', '#FFB700']
        )
        fig_crime.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0'
        )
        st.plotly_chart(fig_crime, use_container_width=True)

with col_b:
    st.markdown("### 🧩 Extracted Entity Distribution")
    df_entities = pd.DataFrame(res_entities)
    if not df_entities.empty and 'type' in df_entities.columns:
        fig_ent = px.bar(
            df_entities['type'].value_counts().reset_index(),
            x='type', y='count', color='type',
            color_discrete_sequence=['#00F0FF', '#9D00FF', '#00FF88', '#FFB700', '#FF3366']
        )
        fig_ent.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0',
            xaxis_title="Entity Type",
            yaxis_title="Count"
        )
        st.plotly_chart(fig_ent, use_container_width=True)

st.markdown("### 📋 Recent Case Files")
st.dataframe(df_cases, use_container_width=True)
