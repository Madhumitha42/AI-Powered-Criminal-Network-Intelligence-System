from typing import List, Dict, Any
from backend.database.db import db_manager

class TemporalAnalyzer:
    def __init__(self):
        pass

    def get_timeline_events(self, case_id: str = None) -> List[Dict[str, Any]]:
        cases = db_manager.get_all_cases()
        timeline = []

        for c in cases:
            if case_id and c['case_id'] != case_id:
                continue

            timeline.append({
                "id": c['case_id'],
                "date": c['date'],
                "event_type": "Case Recorded",
                "title": c['title'],
                "crime_type": c['crime_type'],
                "location": c['location'],
                "summary": c['summary'],
                "assigned_officer": c['assigned_officer']
            })

        # Sort chronologically
        timeline = sorted(timeline, key=lambda x: x['date'])
        return timeline

temporal_analyzer = TemporalAnalyzer()
