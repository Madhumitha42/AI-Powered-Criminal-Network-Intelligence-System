from difflib import SequenceMatcher
from typing import List, Dict, Any
from backend.database.db import db_manager

class EntityResolver:
    def __init__(self, match_threshold: float = 0.75):
        self.match_threshold = match_threshold

    def calculate_similarity(self, str1: str, str2: str) -> float:
        s1 = str1.lower().strip()
        s2 = str2.lower().strip()
        
        # Exact match
        if s1 == s2:
            return 1.0

        # Substring / Alias match (e.g. "Ravi Kumar" vs "R. Kumar" or "Kumar")
        parts1 = set(s1.replace('.', '').split())
        parts2 = set(s2.replace('.', '').split())
        
        if parts1.intersection(parts2) and (len(parts1) == 1 or len(parts2) == 1):
            return 0.85

        # Sequence matcher ratio
        ratio = SequenceMatcher(None, s1, s2).ratio()
        return round(ratio, 2)

    def find_potential_matches(self) -> List[Dict[str, Any]]:
        entities = db_manager.get_all_entities()
        persons = [e for e in entities if e['type'] == 'Person']
        potential_matches = []

        for i in range(len(persons)):
            for j in range(i + 1, len(persons)):
                p1 = persons[i]
                p2 = persons[j]

                sim_score = self.calculate_similarity(p1['name'], p2['name'])

                # Check shared attributes (e.g. phone, vehicle, location)
                shared_factors = []
                p1_details = p1.get('details', {})
                p2_details = p2.get('details', {})

                if p1_details.get('phone') and p1_details.get('phone') == p2_details.get('phone'):
                    sim_score = max(sim_score, 0.95)
                    shared_factors.append(f"Same Phone Identifier ({p1_details.get('phone')})")

                # Shared cases
                cases1 = set(p1.get('associated_cases', []))
                cases2 = set(p2.get('associated_cases', []))
                shared_cases = cases1.intersection(cases2)
                if shared_cases:
                    shared_factors.append(f"Co-occur in cases: {', '.join(shared_cases)}")

                if sim_score >= self.match_threshold or shared_factors:
                    if not shared_factors:
                        shared_factors.append("High Name Similarity Pattern")
                        
                    potential_matches.append({
                        "entity_1": {"id": p1['entity_id'], "name": p1['name'], "cases": p1.get('associated_cases', [])},
                        "entity_2": {"id": p2['entity_id'], "name": p2['name'], "cases": p2.get('associated_cases', [])},
                        "similarity_score": sim_score,
                        "confidence_percent": int(sim_score * 100),
                        "supporting_factors": shared_factors,
                        "status": "Needs Investigator Review"
                    })

        return potential_matches

entity_resolver = EntityResolver()
