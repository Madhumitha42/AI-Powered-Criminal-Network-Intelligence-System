import streamlit as st
import requests

st.set_page_config(page_title="Behavioral Intelligence | Intelligence Platform", layout="wide")

st.markdown("## 🧠 Behavioral Pattern Intelligence Engine")
st.caption("Recurring Interactions, Vehicle Overlaps, Location Hotspots & Communication Relay Hubs")

API_URL = "http://localhost:8000/api/v1"

try:
    patterns_data = requests.get(f"{API_URL}/patterns/analyze").json()
    patterns = patterns_data.get("patterns", [])
    anomalies = patterns_data.get("anomalies", [])
except Exception:
    patterns = []
    anomalies = []

col1, col2 = st.columns(2)
col1.metric("Detected Recurring Patterns", len(patterns))
col2.metric("Network Statistical Anomalies", len(anomalies))

st.markdown("---")

tab1, tab2 = st.tabs(["🔁 Recurring Patterns", "⚠️ Statistical Anomalies"])

with tab1:
    if patterns:
        for p in patterns:
            with st.container():
                st.markdown(f"""
                    <div class="hud-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="color: #00F0FF; margin: 0;">{p['title']}</h4>
                            <span class="badge-high">Severity: {p['severity']}</span>
                        </div>
                        <p style="color: #E2E8F0; margin-top: 10px;">{p['description']}</p>
                        <div style="font-size: 0.85rem; color: #94A3B8;">
                            <b>Confidence Score:</b> {int(p['confidence']*100)}% | <b>Cases Involved:</b> {', '.join(p['cases'])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No behavioral patterns detected.")

with tab2:
    if anomalies:
        for a in anomalies:
            st.markdown(f"""
                <div class="hud-card" style="border-color: rgba(255, 183, 0, 0.4);">
                    <h4 style="color: #FFB700;">⚠️ {a['title']}</h4>
                    <p>{a['reason']}</p>
                    <div style="font-size: 0.85rem; color: #94A3B8;">
                        Entity: <b>{a['entity_name']}</b> | Cases: {', '.join(a.get('cases', []))}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No anomalies detected.")
