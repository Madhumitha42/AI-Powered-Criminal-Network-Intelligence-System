import streamlit as st
import requests

st.set_page_config(page_title="Entity Explorer | Intelligence Platform", layout="wide")

st.markdown("## 👤 Entity Intelligence Profile Explorer")
st.caption("Detailed Profile, Aliases, Associated Assets & Cross-Case Links")

API_URL = "http://localhost:8000/api/v1"

try:
    entities = requests.get(f"{API_URL}/entities").json()
except Exception:
    entities = []

if not entities:
    st.info("No entities currently available. Please start backend service.")
else:
    entity_names = [f"{e['name']} ({e['type']} - {e['entity_id']})" for e in entities]
    selected_str = st.selectbox("🔍 Search & Select Entity:", entity_names)
    
    selected_id = selected_str.split("-")[-1].replace(")", "").strip()
    target_ent = next((e for e in entities if e['entity_id'] == selected_id or e['name'] in selected_str), entities[0])

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
            <div class="hud-card" style="text-align: center;">
                <div style="font-size: 3rem;">👤</div>
                <h3 style="color: #00F0FF; margin: 10px 0;">{target_ent['name']}</h3>
                <span class="badge-active">{target_ent['type']}</span>
                <hr style="border-color: rgba(0,240,255,0.2); margin: 15px 0;">
                <div style="text-align: left; font-size: 0.9rem;">
                    <p><b>Entity ID:</b> {target_ent['entity_id']}</p>
                    <p><b>Associated Cases:</b> {', '.join(target_ent.get('associated_cases', []))}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🔍 Extracted Metadata & Attribute Matrix")
        st.json(target_ent.get('details', {}))

        st.markdown("### 🔗 Cross-Case Connections")
        cases = target_ent.get('associated_cases', [])
        if cases:
            for c in cases:
                st.markdown(f"- 📌 **{c}**: Documented co-occurrence in official record.")
        else:
            st.caption("No multi-case records attached.")
