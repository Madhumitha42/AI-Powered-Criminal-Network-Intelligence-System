from fastapi import APIRouter
from ai_engine.behavior_engine.pattern_detector import pattern_detector
from ai_engine.behavior_engine.anomaly_detector import anomaly_detector
from ai_engine.behavior_engine.temporal_analyzer import temporal_analyzer

router = APIRouter(prefix="/patterns", tags=["Behavioral Intelligence"])

@router.get("/analyze")
def analyze_patterns():
    patterns = pattern_detector.detect_all_patterns()
    anomalies = anomaly_detector.detect_anomalies()
    return {
        "total_patterns": len(patterns),
        "total_anomalies": len(anomalies),
        "patterns": patterns,
        "anomalies": anomalies
    }

@router.get("/timeline")
def get_timeline(case_id: str = None):
    return temporal_analyzer.get_timeline_events(case_id=case_id)
