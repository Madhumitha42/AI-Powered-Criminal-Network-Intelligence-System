from fastapi import APIRouter, Query
from typing import Optional
from graph_engine.graph_analysis import graph_analyzer

router = APIRouter(prefix="/network", tags=["Graph Network Analysis"])

@router.get("/analyze")
def analyze_network(case_id: Optional[str] = Query(None)):
    result = graph_analyzer.analyze_network(case_filter=case_id)
    return result

@router.get("/cross-case-path")
def get_cross_case_path(start: str = Query(...), end: str = Query(...)):
    paths = graph_analyzer.discover_cross_case_paths(start, end)
    return {"start": start, "end": end, "shortest_paths": paths}
