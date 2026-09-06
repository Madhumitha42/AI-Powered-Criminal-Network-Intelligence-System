# 🛡️ AI-Powered Criminal Network Intelligence System

> **“Connect the Evidence. Discover the Patterns. Support the Investigation.”**

An advanced, full-stack decision-support system designed for law enforcement investigators to transform fragmented, multi-case records into interactive **Knowledge Graphs**, detect hidden criminal network patterns, perform spaCy NLP entity extraction, and provide Explainable AI (XAI) leads with full audit accountability.

---

## 🌐 Live System Links

- **Interactive Web Application (GitHub Pages):** [https://madhumitha42.github.io/AI-Powered-Criminal-Network-Intelligence-System/](https://madhumitha42.github.io/AI-Powered-Criminal-Network-Intelligence-System/)
- **Full Python Streamlit Command Center:** [https://criminal-network-intelligence.streamlit.app](https://criminal-network-intelligence.streamlit.app)

---

## 🚀 Key System Features

### 📁 1. Multi-Case Data Ingestion & spaCy NLP Extraction Sandbox
- Upload or paste unformatted interrogation notes, FIRs, and witness statements.
- Automatically extract structured entities: **Persons** (with alias resolution), **Vehicles** (Indian registration formats), **Phone Identifiers**, and **Locations**.

### 👤 2. Entity Intelligence Profile Explorer
- Centralized attribute matrix and dossier view for all extracted entities.
- Inspect connected case records, known aliases, phone call logs, and vehicle registrations.

### 🕸️ 3. Interactive Knowledge Graph & Multi-Hop Path Finder
- Render dynamic multi-layer entity graphs powered by **Vis.js** / **NetworkX**.
- Custom node physics, color-coded node types (Person, Vehicle, Communication, Location, Case), and node centrality scaling.
- **Multi-Hop Path Discovery:** Find hidden connections between seemingly unrelated suspects across multiple independent case files (e.g. *Suspect A ➔ Vehicle ➔ Operator B ➔ Burner Phone ➔ Suspect C*).

### 🧠 4. Behavioral Pattern Intelligence & Anomaly Engine
- Detect recurring vehicle sharing across independent crime scenes.
- Identify communication relay bridge hubs and frequent location hotspots.
- Flag statistical network anomalies using **IsolationForest** machine learning models.

### ⏳ 5. Temporal Incident Progression & Interactive Timeline
- Visualize multi-case events chronologically using interactive **Plotly** scatter flows.
- Trace the timeline of vehicle movements, phone calls, and cargo interceptions.

### 💡 6. Explainable AI (XAI) Cards & Investigator Review (Human-in-the-Loop)
- Transparent reasoning factors explaining *why* a particular network or pattern was flagged.
- Confidence score percentages and direct evidence pointers.
- Human-in-the-Loop review actions (**✅ CONFIRM**, **❌ REJECT**, **🔍 MARK FOR REVIEW**).

### 📜 7. Master Case Summary & Investigator Audit Log Stream
- Export complete investigation reports in structured JSON format.
- Real-time role-based audit logging ensuring 100% accountability for every investigator action.

---

## ⚖️ Ethical Boundary & Decision Support Architecture

> [!IMPORTANT]
> **Strict Decision-Support Boundaries:**
> - ❌ This system **does NOT predict guilt** or generate automated arrest recommendations.
> - ✅ Highlights evidence-backed cross-case patterns and network linkages for human investigator review.
> - ✅ Maintains full role-based audit trail logging for judicial transparency and accountability.

---

## 🛠️ Technology Stack

- **Frontend Web Portal:** HTML5, CSS3 (Dark Cyber Glassmorphic Theme), JavaScript (ES6+), Vis.js Network Canvas
- **Python Application Engine:** Streamlit (UI Framework), FastAPI (RESTful API Router), Uvicorn
- **AI & Data Engines:** spaCy (NLP Named Entity Recognition), NetworkX (Knowledge Graph Analytics), Scikit-Learn (IsolationForest Anomaly Detection), Plotly & PyVis
- **Data Validation & Storage:** Pydantic (v2 / Fallback), SQLite / PostgreSQL Dual Adapter

---

## 💻 Local Installation & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Madhumitha42/AI-Powered-Criminal-Network-Intelligence-System.git
cd AI-Powered-Criminal-Network-Intelligence-System
