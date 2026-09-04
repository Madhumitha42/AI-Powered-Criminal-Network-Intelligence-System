import streamlit as st
import plotly.express as px
import pandas as pd
import requests

st.set_page_config(page_title="Timeline Analysis | Intelligence Platform", layout="wide")

st.markdown("## ⏳ Temporal Sequence & Timeline Analysis")
st.caption("Chronological Progression of Incidents, Vehicle Movements & Multi-Case Events")

API_URL = "http://localhost:8000/api/v1"

try:
    events = requests.get(f"{API_URL}/patterns/timeline").json()
except Exception:
    events = []

if events:
    df_events = pd.DataFrame(events)
    df_events['date'] = pd.to_datetime(df_events['date'])

    fig_timeline = px.scatter(
        df_events, x="date", y="title", color="crime_type",
        size_max=20, text="id", hover_data=["location", "assigned_officer"],
        color_discrete_sequence=['#00F0FF', '#9D00FF', '#00FF88', '#FFB700']
    )
    fig_timeline.update_traces(marker=dict(size=14, line=dict(width=2, color='#00F0FF')))
    fig_timeline.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#E2E8F0',
        xaxis_title="Date of Incident",
        yaxis_title="Case Title"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

    st.markdown("### 📜 Chronological Event Log")
    for ev in events:
        st.markdown(f"""
            <div class="hud-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #00F0FF; font-weight: bold;">[{ev['date']}] {ev['id']}: {ev['title']}</span>
                    <span class="badge-active">{ev['crime_type']}</span>
                </div>
                <p style="margin-top: 8px; color: #E2E8F0;">{ev['summary']}</p>
                <div style="font-size: 0.8rem; color: #94A3B8;">📍 Location: {ev['location']} | 👮 Officer: {ev['assigned_officer']}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("No timeline events available.")
