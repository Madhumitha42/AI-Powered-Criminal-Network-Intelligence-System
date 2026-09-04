# AI-Powered Criminal Network Intelligence & Investigation Support System

> **Tagline:** “Connect the Evidence. Discover the Patterns. Support the Investigation.”  
> **Smart India Hackathon (SIH) Prototype**

---

## 🛡️ Executive Summary & SIH Innovation

Law enforcement investigators handle fragmented multi-case records (Persons, Vehicles, Phone/Emails, Locations, Organizations, Events, Transactions) spread across independent case files. 

This platform automatically ingests unstructured and structured case records, extracts entities using **spaCy NLP**, builds an interactive **Knowledge Graph (NetworkX/Neo4j)**, performs **Behavioral Intelligence Pattern Detection**, calculates **Network Centrality Metrics**, identifies **Multi-Hop Cross-Case Connections**, and renders **Explainable AI (XAI) Cards** with **Human-in-the-Loop Verification**.

---

## ⚖️ Ethical Boundary & Decision Support Architecture

> [!IMPORTANT]
> This system is designed strictly as an **Investigation Support & Network Intelligence Platform**.  
> - ❌ Does NOT predict guilt or make automated arrest recommendations.  
> - ✅ Highlights evidence-backed patterns, cross-case linkages, and network anomalies for investigator review.  
> - ✅ Maintains role-based audit trails for full accountability.

---

## 🏗️ System Architecture

```text
               INVESTIGATOR DASHBOARD
               (Streamlit + Cyber Theme)
                          │
                          ▼
                 FASTAPI BACKEND API
          (Auth, Cases, Network, Patterns, XAI)
       ┌──────────────────┼──────────────────┐
       ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  SQLite /    │   │ NetworkX /   │   │  AI Engine   │
│  PostgreSQL  │   │    Neo4j     │   │ (spaCy, XAI, │
│  App Data    │   │ Knowledge    │   │ Behavioral)  │
│              │   │ Graph        │   │              │
└──────────────┘   └──────────────┘   └──────────────┘
```

---

## 🚀 Quickstart & Execution Instructions

### 1. Prerequisites
- Python 3.9+
- Pip package manager

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Run FastAPI Backend
```bash
uvicorn backend.main:app --reload --port 8000
```
- API Documentation: `http://localhost:8000/docs`

### 4. Run Streamlit Frontend Command Center
```bash
streamlit run frontend/app.py
```
- Frontend UI: `http://localhost:8501`

### 5. Run Automated Verification Tests
```bash
pytest tests/test_ai_engine.py -v
```

---

## 🎬 SIH Demo Storyline (Multi-Hop Cross-Case Discovery)

During your live hackathon presentation:
1. Open **Case Management** and demonstrate loading `CASE-2026-001` through `CASE-2026-021`.
2. Open **Network Explorer** and click **Discover Path** between `P-101 (Ravi Kumar)` and `P-103 (Arun Sharma)`.
3. The system uncovers the hidden 4-step cross-case link:
   `Ravi Kumar (P-101)` ➔ `Vehicle MH-02-AB-9901 (V-101)` ➔ `Alias Kumar (P-102)` ➔ `Burner Phone +91-9876543210 (C-101)` ➔ `Arun Sharma (P-103)`.
4. Demonstrate **AI Insights (XAI)** cards showing evidence pointers, confidence breakdown, and Investigator Confirm/Reject logging in the Audit Log!
