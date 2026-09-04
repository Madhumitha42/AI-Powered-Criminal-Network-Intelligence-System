from typing import List, Dict, Any
from ai_engine.behavior_engine.pattern_detector import pattern_detector
from ai_engine.behavior_engine.anomaly_detector import anomaly_detector

class XAIExplainer:
    def __init__(self):
        pass

    def generate_xai_cards(self) -> List[Dict[str, Any]]:
        cards = []
        
        # 1. Patterns to XAI Cards
        patterns = pattern_detector.detect_all_patterns()
        for idx, p in enumerate(patterns):
            cards.append({
                "insight_id": f"XAI-PAT-{idx+1:03d}",
                "title": p["title"],
                "category": p["pattern_type"],
                "summary": p["description"],
                "confidence_score": p["confidence"],
                "confidence_level": "High" if p["confidence"] >= 0.90 else "Medium",
                "reasoning_factors": p["explanation"],
                "supporting_evidence": [
                    {"type": "Case Association", "ref": f"Cases: {', '.join(p['cases'])}"},
                    {"type": "Entity Connection", "ref": f"Entities: {', '.join(p['involved_entities'])}"}
                ],
                "investigator_action": "Pending Review"
            })

        # 2. Anomalies to XAI Cards
        anomalies = anomaly_detector.detect_anomalies()
        for idx, a in enumerate(anomalies):
            cards.append({
                "insight_id": f"XAI-ANO-{idx+1:03d}",
                "title": a["title"],
                "category": "Behavioral Anomaly",
                "summary": a["reason"],
                "confidence_score": a["confidence"],
                "confidence_level": "High" if a["confidence"] >= 0.90 else "Medium",
                "reasoning_factors": [
                    a["reason"],
                    f"Entity '{a['entity_name']}' flagged as statistical outlier in network graph.",
                    f"Associated cases: {', '.join(a.get('cases', []))}"
                ],
                "supporting_evidence": [
                    {"type": "Graph Metric", "ref": f"Node ID: {a['entity_id']}"},
                    {"type": "Case Records", "ref": f"Cases: {', '.join(a.get('cases', []))}"}
                ],
                "investigator_action": "Pending Review"
            })

        return cards

xai_explainer = XAIExplainer()
