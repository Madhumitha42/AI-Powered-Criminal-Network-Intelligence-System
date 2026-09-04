import streamlit as st
import requests

st.set_page_config(page_title="AI Insights & XAI | Intelligence Platform", layout="wide")

st.markdown("## 🧠 Explainable AI (XAI) Cards & Investigator Review")
st.caption("Transparent Reasoning, Confidence Scores, Evidence Pointers & Human-in-the-Loop Action")

API_URL = "http://localhost:8000/api/v1"

try:
    insights = requests.get(f"{API_URL}/insights").json()
except Exception:
    insights = []

if not insights:
    st.info("No AI insights currently generated.")
else:
    for card in insights:
        st.markdown(f"""
            <div class="hud-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="badge-active">{card['category']}</span>
                        <h3 style="color: #00F0FF; margin: 8px 0;">🧠 {card['title']}</h3>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: #00FF88;">
                            {int(card['confidence_score']*100)}%
                        </div>
                        <div style="font-size: 0.75rem; color: #94A3B8;">Confidence: {card['confidence_level']}</div>
                    </div>
                </div>
                <p style="color: #E2E8F0; margin: 12px 0;">{card['summary']}</p>
                <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; margin-bottom: 15px;">
                    <b style="color: #00FFFF;">WHY THIS NETWORK / PATTERN WAS FLAGGED:</b>
                    <ul style="color: #94A3B8; margin-top: 5px;">
                        {''.join([f'<li>✓ {factor}</li>' for factor in card['reasoning_factors']])}
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_act1, col_act2, col_act3, col_notes = st.columns([1, 1, 1.5, 3])
        
        with col_act1:
            if st.button("✅ CONFIRM", key=f"conf_{card['insight_id']}"):
                requests.post(f"{API_URL}/insights/review", json={"insight_id": card['insight_id'], "action": "CONFIRM"})
                st.success("Confirmed lead logged in audit trail!")
        
        with col_act2:
            if st.button("❌ REJECT", key=f"rej_{card['insight_id']}"):
                requests.post(f"{API_URL}/insights/review", json={"insight_id": card['insight_id'], "action": "REJECT"})
                st.warning("Rejected lead logged in audit trail!")

        with col_act3:
            if st.button("🔍 MARK FOR REVIEW", key=f"rev_{card['insight_id']}"):
                requests.post(f"{API_URL}/insights/review", json={"insight_id": card['insight_id'], "action": "MARK_FOR_REVIEW"})
                st.info("Marked for senior review!")

        st.markdown("<hr style='border-color: rgba(0, 240, 255, 0.15); margin: 20px 0;'>", unsafe_allow_html=True)
