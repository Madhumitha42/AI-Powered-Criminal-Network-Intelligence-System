from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.models.schemas import CaseBase, CaseCreate
from backend.database.db import db_manager

router = APIRouter(prefix="/cases", tags=["Case Management"])

@router.get("", response_model=List[CaseBase])
def get_all_cases():
    return db_manager.get_all_cases()

@router.get("/{case_id}", response_model=CaseBase)
def get_case(case_id: str):
    cases = db_manager.get_all_cases()
    for c in cases:
        if c['case_id'] == case_id:
            return c
    raise HTTPException(status_code=404, detail="Case not found")

@router.post("", response_model=CaseBase)
def create_case(case_data: CaseCreate):
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        case_data.case_id, case_data.title, case_data.crime_type,
        case_data.date, case_data.location, case_data.summary,
        case_data.status, case_data.assigned_officer
    ))
    conn.commit()
    conn.close()

    db_manager.add_audit_log("investigator", "CREATE_CASE", f"Created case {case_data.case_id}")
    return case_data
