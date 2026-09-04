import numpy as np
from typing import List, Dict, Any
from backend.database.db import db_manager
from graph_engine.graph_analysis import graph_analyzer

try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

class AnomalyDetector:
    def __init__(self):
        pass

    def detect_anomalies(self) -> List[Dict[str, Any]]:
        anomalies = []
        network_data = graph_analyzer.analyze_network()
        nodes = network_data.get("nodes", [])

        if not nodes:
            return []

        # Prepare feature matrix for anomaly detection [degree, degree_centrality, betweenness_centrality, case_count]
        features = []
        node_map = []

        for n in nodes:
            deg = n.get("degree", 0)
            deg_cent = n.get("degree_centrality", 0.0)
            bet_cent = n.get("betweenness_centrality", 0.0)
            case_cnt = len(n.get("cases", []))
            
            features.append([deg, deg_cent, bet_cent, case_cnt])
            node_map.append(n)

        if HAS_SKLEARN and len(features) >= 3:
            X = np.array(features)
            clf = IsolationForest(contamination=0.15, random_state=42)
            preds = clf.fit_predict(X)

            for idx, pred in enumerate(preds):
                if pred == -1:  # Anomaly detected
                    target = node_map[idx]
                    anomalies.append({
                        "anomaly_id": f"ANO-{target['id']}",
                        "title": f"Unusual High-Connectivity Anomaly: {target['label']}",
                        "entity_id": target['id'],
                        "entity_name": target['label'],
                        "entity_type": target['type'],
                        "reason": f"Statistical outlier in connection density (Degree={target['degree']}, Betweenness={target['betweenness_centrality']}).",
                        "severity": "High",
                        "confidence": 0.92,
                        "cases": target.get("cases", [])
                    })
        else:
            # Fallback heuristic anomaly detection
            for n in nodes:
                if n.get("degree", 0) >= 3 or n.get("betweenness_centrality", 0.0) > 0.2:
                    anomalies.append({
                        "anomaly_id": f"ANO-{n['id']}",
                        "title": f"Structural Network Anomaly: {n['label']}",
                        "entity_id": n['id'],
                        "entity_name": n['label'],
                        "entity_type": n['type'],
                        "reason": f"Disproportionate graph degree ({n['degree']}) and betweenness centrality.",
                        "severity": "Medium",
                        "confidence": 0.85,
                        "cases": n.get("cases", [])
                    })

        return anomalies

anomaly_detector = AnomalyDetector()
