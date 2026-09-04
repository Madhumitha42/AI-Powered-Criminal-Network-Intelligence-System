import streamlit as st
import os
import requests

# Page Config
st.set_page_config(
    page_title="Criminal Network Intelligence System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "styles", "cyber_theme.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# API Base URL
API_URL = "http://localhost:8000/api/v1"

# Sidebar Branding
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-size: 2.5rem;">🛡️</div>
            <div style="font-family: 'Orbitron', sans-serif; font-weight: 800; font-size: 1.1rem; color: #00F0FF; margin-top: 5px;">
                CRIMINAL NETWORK
            </div>
            <div style="font-size: 0.75rem; color: #94A3B8; letter-spacing: 1px;">
                INTELLIGENCE SYSTEM
            </div>
        </div>
        <hr style="border-color: rgba(0, 240, 255, 0.2); margin: 15px 0;">
    """, unsafe_allow_html=True)
    
    st.markdown("### 👤 Active Investigator")
    st.info("Log In Status: **Inspector V. Deshmukh** (ADMIN)")
    st.caption("Smart India Hackathon (SIH) Prototype Build")
    st.markdown("---")
    st.caption("🔒 Decision-Support System: Human Verification Required")

# Hero Section
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("""
        <div style="padding-top: 20px;">
            <span class="badge-active">AI-POWERED INVESTIGATION SUPPORT</span>
            <h1 style="font-size: 2.8rem; margin: 15px 0; line-height: 1.2;">
                AI-POWERED<br>
                <span style="color: #00F0FF; text-shadow: 0 0 20px rgba(0,240,255,0.6);">CRIMINAL NETWORK</span><br>
                ANALYSIS SYSTEM
            </h1>
            <p style="font-size: 1.1rem; color: #94A3B8; margin-bottom: 25px; line-height: 1.6;">
                <i>“Connect the Evidence. Discover the Patterns. Support the Investigation.”</i>
            </p>
            <p style="font-size: 0.95rem; color: #E2E8F0; line-height: 1.6;">
                Automated multi-case knowledge graph construction, entity resolution, behavioral pattern detection, and explainable AI intelligence leads for authorized law enforcement investigators.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 EXPLORE NETWORK GRAPH →"):
        st.switch_page("pages/4_Network_Explorer.py")

with col2:
    st.markdown("""
        <div class="hud-card" style="text-align: center; padding: 30px;">
            <div style="position: relative; width: 220px; height: 220px; margin: 0 auto; border-radius: 50%; border: 2px dashed #00F0FF; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 30px rgba(0,240,255,0.3);">
                <div style="position: absolute; width: 160px; height: 160px; border-radius: 50%; border: 1px solid #9D00FF; box-shadow: 0 0 15px rgba(157,0,255,0.4);"></div>
                <div style="font-size: 3rem;">🧠</div>
            </div>
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.2rem; color: #00FFFF; margin-top: 15px;">
                BEHAVIORAL AI KNOWLEDGE CORE
            </div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 5px;">
                Person • Vehicle • Location • Comms • Case • Organization
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Dashboard HUD Stats Cards
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
        <div class="hud-card">
            <div class="metric-label">Cases Analyzed</div>
            <div class="metric-value">12,846</div>
            <div style="font-size: 0.75rem; color: #00FF88;">+100 SIH Demo Dataset</div>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
        <div class="hud-card">
            <div class="metric-label">Entities Extracted</div>
            <div class="metric-value">8,327</div>
            <div style="font-size: 0.75rem; color: #00F0FF;">Person, Vehicle, Comms</div>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
        <div class="hud-card">
            <div class="metric-label">Networks Detected</div>
            <div class="metric-value">3,142</div>
            <div style="font-size: 0.75rem; color: #9D00FF;">Cross-Case Overlaps</div>
        </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
        <div class="hud-card">
            <div class="metric-label">Analysis Accuracy</div>
            <div class="metric-value">98.7%</div>
            <div style="font-size: 0.75rem; color: #00FF88;">Explainable AI Lead Precision</div>
        </div>
    """, unsafe_allow_html=True)

# System Status HUD
st.markdown("### 📡 System Operations & Data Streams")
st1, st2, st3, st4 = st.columns(4)

with st1:
    st.success("System Status: **ACTIVE**")
with st2:
    st.info("Data Sources Connected: **24**")
with st3:
    st.warning("Relationships Processed: **156,892**")
with st4:
    st.error("Audit Logs Recorded: **100%**")

st.progress(83, text="AI Behavioral Pattern Engine: 83% Analysis Complete")
