import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database.db import db_manager
from ai_engine.nlp.entity_extractor import entity_extractor
from ai_engine.entity_resolution.resolver import entity_resolver
from graph_engine.graph_analysis import graph_analyzer
from ai_engine.behavior_engine.pattern_detector import pattern_detector
from ai_engine.explainability.xai_explainer import xai_explainer

def test_database_seeding():
    cases = db_manager.get_all_cases()
    assert len(cases) >= 6
    entities = db_manager.get_all_entities()
    assert len(entities) >= 5

def test_nlp_extraction():
    text = "Armored truck intercepted by suspect Ravi Kumar with vehicle MH-02-AB-9901 and burner phone +91-9876543210 near Bandra."
    res = entity_extractor.extract_entities_from_text(text)
    assert len(res["communications"]) >= 1
    assert len(res["vehicles"]) >= 1

def test_entity_resolution():
    score = entity_resolver.calculate_similarity("Ravi Kumar", "R. Kumar")
    assert score >= 0.75

def test_graph_analysis_and_cross_case_path():
    net = graph_analyzer.analyze_network()
    assert net["total_nodes"] > 0
    
    # Path discovery test: P-101 to P-103
    paths = graph_analyzer.discover_cross_case_paths("P-101", "P-103")
    assert len(paths) >= 1
    assert paths[0][0] == "P-101"
    assert paths[0][-1] == "P-103"

def test_pattern_detection_and_xai():
    patterns = pattern_detector.detect_all_patterns()
    assert len(patterns) >= 1
    cards = xai_explainer.generate_xai_cards()
    assert len(cards) >= 1
    assert "confidence_score" in cards[0]
