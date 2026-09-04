from typing import List, Dict, Any
from backend.database.db import db_manager
from graph_engine.graph_analysis import graph_analyzer

class PatternDetector:
    def __init__(self):
        pass

    def detect_all_patterns(self) -> List[Dict[str, Any]]:
        patterns = []

        # 1. Cross-Case Vehicle Sharing Pattern
        patterns.extend(self._detect_cross_case_vehicle_patterns())

        # 2. Repeated Location Pattern
        patterns.extend(self._detect_repeated_location_patterns())

        # 3. Communication Bridge Pattern
        patterns.extend(self._detect_communication_bridge_patterns())

        # 4. Multi-Case Entity Co-occurrence
        patterns.extend(self._detect_entity_cooccurrence_patterns())

        return patterns

    def _detect_cross_case_vehicle_patterns(self) -> List[Dict[str, Any]]:
        results = []
        entities = db_manager.get_all_entities()
        vehicles = [e for e in entities if e['type'] == 'Vehicle']

        for v in vehicles:
            cases = v.get('associated_cases', [])
            if len(cases) > 1:
                results.append({
                    "pattern_id": f"PAT-VEH-{v['entity_id']}",
                    "pattern_type": "Cross-Case Vehicle Association",
                    "title": f"Vehicle {v['name']} linked across {len(cases)} distinct cases",
                    "description": f"Vehicle identifier {v['name']} was recorded in multiple case files ({', '.join(cases)}). Potential mobile asset across operations.",
                    "severity": "High",
                    "confidence": 0.94,
                    "involved_entities": [v['entity_id'], v['name']],
                    "cases": cases,
                    "explanation": [
                        f"Same plate registration ({v['name']}) identified in {len(cases)} separate incidents.",
                        f"Cases involved: {', '.join(cases)}.",
                        "Requires vehicle movement timeline inspection."
                    ]
                })
        return results

    def _detect_repeated_location_patterns(self) -> List[Dict[str, Any]]:
        results = []
        entities = db_manager.get_all_entities()
        locations = [e for e in entities if e['type'] == 'Location']

        for loc in locations:
            cases = loc.get('associated_cases', [])
            if len(cases) > 1:
                results.append({
                    "pattern_id": f"PAT-LOC-{loc['entity_id']}",
                    "pattern_type": "Repeated Location Hotspot",
                    "title": f"Location '{loc['name']}' reoccurs in {len(cases)} cases",
                    "description": f"Geographical venue '{loc['name']}' appears as an operational nexus in multiple cases.",
                    "severity": "Medium",
                    "confidence": 0.88,
                    "involved_entities": [loc['entity_id'], loc['name']],
                    "cases": cases,
                    "explanation": [
                        f"Location appears across cases: {', '.join(cases)}.",
                        "Spatial overlap detected among disparate records."
                    ]
                })
        return results

    def _detect_communication_bridge_patterns(self) -> List[Dict[str, Any]]:
        results = []
        entities = db_manager.get_all_entities()
        comms = [e for e in entities if e['type'] == 'Communication']

        for c in comms:
            details = c.get('details', {})
            linked_persons = details.get('linked_persons', [])
            cases = c.get('associated_cases', [])
            if len(linked_persons) > 1 or len(cases) > 1:
                results.append({
                    "pattern_id": f"PAT-COMM-{c['entity_id']}",
                    "pattern_type": "Communication Bridge Hub",
                    "title": f"Identifier {c['name']} bridges multiple actors/cases",
                    "description": f"Communication identifier {c['name']} acts as a central link between distinct entities and cases.",
                    "severity": "High",
                    "confidence": 0.96,
                    "involved_entities": [c['entity_id']] + linked_persons,
                    "cases": cases,
                    "explanation": [
                        f"Used across cases: {', '.join(cases)}.",
                        f"Linked individuals: {', '.join(linked_persons)}.",
                        "Burner phone or shared communications relay pattern."
                    ]
                })
        return results

    def _detect_entity_cooccurrence_patterns(self) -> List[Dict[str, Any]]:
        results = []
        network_data = graph_analyzer.analyze_network()
        top_nodes = network_data.get("top_central_nodes", [])

        for node in top_nodes:
            if node.get("betweenness_centrality", 0) > 0.15:
                results.append({
                    "pattern_id": f"PAT-CENT-{node['id']}",
                    "pattern_type": "High Betweenness Network Nexus",
                    "title": f"Entity '{node['label']}' acts as key bridge node",
                    "description": f"Network topology analysis identifies '{node['label']}' with high betweenness centrality ({node['betweenness_centrality']}), connecting separate sub-clusters.",
                    "severity": "High",
                    "confidence": 0.91,
                    "involved_entities": [node['id'], node['label']],
                    "cases": node.get('cases', []),
                    "explanation": [
                        f"Betweenness Centrality metric: {node['betweenness_centrality']}.",
                        "High probability of acting as an intermediary node across sub-networks."
                    ]
                })
        return results

pattern_detector = PatternDetector()
