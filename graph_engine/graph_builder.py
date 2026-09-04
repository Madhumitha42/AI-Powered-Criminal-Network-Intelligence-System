import networkx as nx
from typing import Dict, Any, List
from backend.database.db import db_manager

class GraphBuilder:
    def __init__(self):
        self.G = nx.Graph()
        self.build_graph()

    def build_graph(self):
        self.G.clear()
        
        entities = db_manager.get_all_entities()
        relationships = db_manager.get_all_relationships()
        cases = db_manager.get_all_cases()

        # Add Cases as Nodes
        for c in cases:
            self.G.add_node(
                c['case_id'],
                label=c['title'],
                type='Case',
                crime_type=c['crime_type'],
                date=c['date'],
                location=c['location']
            )

        # Add Entities as Nodes
        for e in entities:
            self.G.add_node(
                e['entity_id'],
                label=e['name'],
                type=e['type'],
                details=e['details'],
                cases=e['associated_cases']
            )
            # Connect Entity to its Cases
            for case_id in e['associated_cases']:
                if self.G.has_node(case_id):
                    self.G.add_edge(e['entity_id'], case_id, label='APPEARS_IN', confidence=1.0, case_id=case_id)

        # Add Entity-to-Entity Relationships
        for r in relationships:
            if self.G.has_node(r['source']) and self.G.has_node(r['target']):
                self.G.add_edge(
                    r['source'],
                    r['target'],
                    label=r['type'],
                    confidence=r['confidence'],
                    case_id=r['case_id']
                )

        return self.G

    def get_networkx_graph(self) -> nx.Graph:
        return self.G

graph_builder = GraphBuilder()
