from fastapi import APIRouter, Body
from typing import List, Dict, Any
from backend.database.db import db_manager
from ai_engine.nlp.entity_extractor import entity_extractor
from ai_engine.entity_resolution.resolver import entity_resolver

router = APIRouter(prefix="/entities", tags=["Entities & AI NLP"])

@router.get("")
def get_all_entities():
    return db_manager.get_all_entities()

@router.post("/extract")
def extract_entities_from_text(payload: Dict[str, str] = Body(...)):
    text = payload.get("text", "")
    extracted = entity_extractor.extract_entities_from_text(text)
    db_manager.add_audit_log("investigator", "NLP_EXTRACTION", f"Extracted {sum(len(v) for v in extracted.values())} entities from narrative")
    return extracted

@router.get("/resolution")
def get_entity_resolution_candidates():
    matches = entity_resolver.find_potential_matches()
    return matches
