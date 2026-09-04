from fastapi import APIRouter
from backend.models.schemas import HumanReviewAction
from ai_engine.explainability.xai_explainer import xai_explainer
from backend.database.db import db_manager
import datetime

router = APIRouter(prefix="/insights", tags=["Explainable AI & Human Review"])

@router.get("")
def get_xai_insights():
    cards = xai_explainer.generate_xai_cards()
    return cards

@router.post("/review")
def record_human_review(action: HumanReviewAction):
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO reviews VALUES (?, ?, ?, ?)
    ''', (action.insight_id, action.action, action.notes or "", datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

    db_manager.add_audit_log(
        user="investigator",
        action="HUMAN_REVIEW",
        details=f"Insight {action.insight_id} set to {action.action}. Notes: {action.notes}"
    )

    return {"status": "Success", "insight_id": action.insight_id, "action": action.action}
