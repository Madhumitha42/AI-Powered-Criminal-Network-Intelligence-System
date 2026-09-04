import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Reports & Audit | Intelligence Platform", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "..", "styles", "cyber_theme.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("## 📜 Reports & Security Audit Trail")
st.caption("Master Investigation Export & Role-Based Action Logs")

API_URL = "http://localhost:8000/api/v1"

tab1, tab2 = st.tabs(["📄 Master Investigation Summary", "🔒 Audit Trail Logs"])

with tab1:
    st.markdown("### 📊 Investigation Intelligence Summary Report")
    try:
        rep = requests.get(f"{API_URL}/reports/summary").json()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Cases", rep.get("total_cases", 0))
        c2.metric("Total Entities", rep.get("total_entities", 0))
        c3.metric("Relationships", rep.get("total_relationships", 0))
        c4.metric("Audit Log Entries", rep.get("audit_entries_count", 0))

        st.markdown("---")
        st.write("#### 📑 Cases Included in Master Report:")
        for c in rep.get("cases_overview", []):
            st.markdown(f"- 📌 **[{c['case_id']}] {c['title']}**: {c['summary']} *(Officer: {c['assigned_officer']})*")

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="💾 DOWNLOAD MASTER REPORT (JSON)",
            data=json.dumps(rep, indent=2),
            file_name="criminal_network_intelligence_report.json",
            mime="application/json"
        )
    except Exception as e:
        st.error(f"Error fetching report: {e}")

with tab2:
    st.markdown("### 🕵️ Role-Based Audit Trail")
    try:
        logs = requests.get(f"{API_URL}/reports/audit-logs").json()
        if logs:
            st.dataframe(logs, use_container_width=True)
        else:
            st.info("No audit entries recorded yet.")
    except Exception as e:
        st.error(f"Error fetching audit logs: {e}")
