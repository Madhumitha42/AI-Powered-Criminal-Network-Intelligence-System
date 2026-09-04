from fastapi import APIRouter
from backend.database.db import db_manager

router = APIRouter(prefix="/reports", tags=["Reports & Audit Logs"])

@router.get("/audit-logs")
def get_audit_logs():
    return db_manager.get_audit_logs()

@router.get("/summary")
def get_investigation_summary():
    cases = db_manager.get_all_cases()
    entities = db_manager.get_all_entities()
    relationships = db_manager.get_all_relationships()
    logs = db_manager.get_audit_logs()

    return {
        "title": "Criminal Network Intelligence Master Investigation Report",
        "total_cases": len(cases),
        "total_entities": len(entities),
        "total_relationships": len(relationships),
        "audit_entries_count": len(logs),
        "cases_overview": cases,
        "recent_audit_trail": logs[:10]
    }
