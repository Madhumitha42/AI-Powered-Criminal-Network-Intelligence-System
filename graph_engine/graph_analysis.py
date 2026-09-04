import networkx as nx
from typing import Dict, Any, List
from graph_engine.graph_builder import graph_builder

class GraphAnalyzer:
    def __init__(self):
        pass

    def analyze_network(self, case_filter: str = None) -> Dict[str, Any]:
        G = graph_builder.get_networkx_graph()

        if case_filter:
            # Subgraph filtered by case
            nodes_in_case = [
                n for n, d in G.nodes(data=True) 
                if n == case_filter or (d.get('cases') and case_filter in d.get('cases'))
            ]
            subG = G.subgraph(nodes_in_case)
        else:
            subG = G

        if subG.number_of_nodes() == 0:
            return {
                "total_nodes": 0,
                "total_edges": 0,
                "density": 0.0,
                "connected_components": 0,
                "top_central_nodes": [],
                "nodes": [],
                "edges": []
            }

        # Centrality metrics
        deg_centrality = nx.degree_centrality(subG)
        bet_centrality = nx.betweenness_centrality(subG)

        nodes_data = []
        for n, d in subG.nodes(data=True):
            deg = subG.degree(n)
            nodes_data.append({
                "id": n,
                "label": d.get("label", n),
                "type": d.get("type", "Unknown"),
                "degree": deg,
                "degree_centrality": round(deg_centrality.get(n, 0.0), 3),
                "betweenness_centrality": round(bet_centrality.get(n, 0.0), 3),
                "cases": d.get("cases", [])
            })

        # Sort top central nodes
        top_central = sorted(nodes_data, key=lambda x: x["betweenness_centrality"], reverse=True)[:5]

        edges_data = []
        for u, v, d in subG.edges(data=True):
            edges_data.append({
                "source": u,
                "target": v,
                "label": d.get("label", "LINKED"),
                "confidence": d.get("confidence", 1.0),
                "case_id": d.get("case_id", "N/A")
            })

        density = round(nx.density(subG), 4)
        num_components = nx.number_connected_components(subG)

        return {
            "total_nodes": subG.number_of_nodes(),
            "total_edges": subG.number_of_edges(),
            "density": density,
            "connected_components": num_components,
            "top_central_nodes": top_central,
            "nodes": nodes_data,
            "edges": edges_data
        }

    def discover_cross_case_paths(self, start_node: str, end_node: str) -> List[List[str]]:
        G = graph_builder.get_networkx_graph()
        if not G.has_node(start_node) or not G.has_node(end_node):
            return []
        try:
            paths = list(nx.all_shortest_paths(G, source=start_node, target=end_node))
            return paths
        except nx.NetworkXNoPath:
            return []

graph_analyzer = GraphAnalyzer()
