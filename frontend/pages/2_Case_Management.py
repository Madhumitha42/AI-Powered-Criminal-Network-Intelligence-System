import streamlit as st
import requests

st.set_page_config(page_title="Case Management | Intelligence Platform", layout="wide")

st.markdown("## 📁 Case Management & AI Ingestion")
st.caption("Upload Unformatted Case Files & Execute AI NLP Entity Extraction")

API_URL = "http://localhost:8000/api/v1"

tab1, tab2 = st.tabs(["📂 Active Cases", "➕ Ingest New Case Narrative"])

with tab1:
    try:
        cases = requests.get(f"{API_URL}/cases").json()
        for c in cases:
            with st.expander(f"📌 [{c['case_id']}] {c['title']} ({c['date']})"):
                col1, col2 = st.columns(2)
                col1.write(f"**Crime Type:** {c['crime_type']}")
                col1.write(f"**Location:** {c['location']}")
                col2.write(f"**Status:** {c['status']}")
                col2.write(f"**Assigned Officer:** {c['assigned_officer']}")
                st.write(f"**Case Summary:** {c['summary']}")
    except Exception as e:
        st.error(f"Backend API Offline. Run uvicorn backend.main:app --reload. Error: {e}")

with tab2:
    st.markdown("### 🤖 NLP Automated Entity & Relationship Extraction")
    case_id = st.text_input("Case ID", value="CASE-2026-099")
    title = st.text_input("Case Title", value="Interstate Highway Hijack Investigation")
    officer = st.text_input("Assigned Investigator", value="Insp. V. Deshmukh")
    
    narrative = st.text_area(
        "Raw Case Narrative / Interrogation Notes",
        value="Armored van stopped at Bandra West by suspect Ravi Kumar driving black SUV MH-02-AB-9901. Suspect used burner phone +91-9876543210 and fled towards Pune Warehouse.",
        height=150
    )

    if st.button("⚡ EXECUTE AI NLP EXTRACTION"):
        with st.spinner("Extracting entities & relationships using spaCy NLP..."):
            try:
                res = requests.post(f"{API_URL}/entities/extract", json={"text": narrative}).json()
                st.success("AI Entity Extraction Complete!")
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Persons Found", len(res.get("persons", [])))
                c2.metric("Vehicles Found", len(res.get("vehicles", [])))
                c3.metric("Phone Identifiers", len(res.get("communications", [])))
                c4.metric("Locations Found", len(res.get("locations", [])))

                st.json(res)
            except Exception as ex:
                st.error(f"Error calling extraction endpoint: {ex}")
