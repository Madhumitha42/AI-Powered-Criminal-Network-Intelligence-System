import streamlit as st
import streamlit.components.v1 as components
import requests
from pyvis.network import Network
import tempfile
import os

st.set_page_config(page_title="Network Explorer | Intelligence Platform", layout="wide")

st.markdown("## 🕸️ Interactive Knowledge Graph Network Explorer")
st.caption("Multi-Layer Entity Graph, Centrality Metrics & Cross-Case Link Discovery")

API_URL = "http://localhost:8000/api/v1"

# Controls & Filters
col_f1, col_f2 = st.columns(2)
with col_f1:
    case_filter = st.selectbox("📌 Filter Graph by Case ID:", ["ALL CASES", "CASE-2026-001", "CASE-2026-008", "CASE-2026-014", "CASE-2026-021"])
with col_f2:
    highlight_centrality = st.checkbox("💡 Highlight High-Betweenness Hub Nodes", value=True)

# Fetch Network Data
try:
    c_param = None if case_filter == "ALL CASES" else case_filter
    net_data = requests.get(f"{API_URL}/network/analyze", params={"case_id": c_param}).json()
except Exception:
    net_data = {"total_nodes": 0, "total_edges": 0, "density": 0, "top_central_nodes": [], "nodes": [], "edges": []}

# Metrics Banner
m1, m2, m3, m4 = st.columns(4)
m1.metric("Graph Nodes", net_data.get("total_nodes", 0))
m2.metric("Graph Edges", net_data.get("total_edges", 0))
m3.metric("Network Density", net_data.get("density", 0.0))
m4.metric("Sub-Components", net_data.get("connected_components", 0))

st.markdown("---")

# Render Interactive PyVis Graph
st.markdown("### 🌐 Live Knowledge Graph")

if net_data.get("nodes"):
    net = Network(height="550px", width="100%", bgcolor="#07090E", font_color="#E2E8F0")
    
    # Node Colors
    COLOR_MAP = {
        "Person": "#00F0FF",
        "Vehicle": "#9D00FF",
        "Location": "#00FF88",
        "Communication": "#FFB700",
        "Case": "#FF3366",
        "Organization": "#00FFFF"
    }

    for n in net_data["nodes"]:
        node_color = COLOR_MAP.get(n.get("type"), "#E2E8F0")
        size = 25 if n.get("betweenness_centrality", 0) > 0.15 and highlight_centrality else 18
        title_hover = f"<b>{n['label']}</b><br>Type: {n['type']}<br>Degree: {n['degree']}<br>Betweenness: {n['betweenness_centrality']}"
        net.add_node(n["id"], label=n["label"], color=node_color, size=size, title=title_hover)

    for e in net_data["edges"]:
        net.add_edge(e["source"], e["target"], title=f"Type: {e['label']}<br>Confidence: {e['confidence']}", color="rgba(0, 240, 255, 0.4)", width=2)

    net.set_options("""
    var options = {
      "nodes": { "font": { "size": 14, "color": "#ffffff" } },
      "edges": { "smooth": { "type": "continuous" } },
      "physics": { "stabilization": false, "barnesHut": { "gravitationalConstant": -4000 } }
    }
    """)

    # Save to temp HTML and render in Streamlit
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        net.save_graph(tmp.name)
        with open(tmp.name, 'r', encoding='utf-8') as f:
            html_content = f.read()
        components.html(html_content, height=570)
else:
    st.info("No graph data retrieved from backend server.")

# Multi-Hop Cross-Case Discovery Tool
st.markdown("### 🔀 Multi-Hop Cross-Case Path Finder")
cp1, cp2, cp3 = st.columns([1, 1, 1])
with cp1:
    start_node = st.text_input("Start Entity ID", value="P-101")
with cp2:
    end_node = st.text_input("Target Entity ID", value="P-103")
with cp3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 DISCOVER PATH"):
        try:
            path_res = requests.get(f"{API_URL}/network/cross-case-path", params={"start": start_node, "end": end_node}).json()
            paths = path_res.get("shortest_paths", [])
            if paths:
                st.success(f"Discovered Cross-Case Connection Path!")
                for p in paths:
                    st.write(" ➔ ".join(p))
            else:
                st.warning("No direct network path found between selected entities.")
        except Exception as e:
            st.error(f"Error fetching cross-case path: {e}")
