from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    role: str
    token: str

class CaseBase(BaseModel):
    case_id: str
    title: str
    crime_type: str
    date: str
    location: str
    summary: str
    status: str = "Active"
    assigned_officer: str

class CaseCreate(CaseBase):
    pass

class EntityBase(BaseModel):
    entity_id: str
    name: str
    type: str  # Person, Vehicle, Location, Communication, Organization
    details: Dict[str, Any] = {}
    associated_cases: List[str] = []

class RelationshipBase(BaseModel):
    source: str
    target: str
    relationship_type: str
    confidence: float
    case_id: str
    evidence_ref: Optional[str] = None

class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    case_count: int = 1
    degree: int = 0
    betweenness: float = 0.0

class GraphEdge(BaseModel):
    source: str
    target: str
    label: str
    confidence: float
    case_id: str

class NetworkAnalysisResult(BaseModel):
    total_nodes: int
    total_edges: int
    density: float
    connected_components: int
    top_central_nodes: List[Dict[str, Any]]
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class PatternResult(BaseModel):
    pattern_id: str
    pattern_type: str
    title: str
    description: str
    severity: str  # High, Medium, Low
    confidence: float
    involved_entities: List[str]
    cases: List[str]
    explanation: List[str]

class XAICard(BaseModel):
    insight_id: str
    title: str
    category: str
    summary: str
    confidence_score: float
    confidence_level: str
    reasoning_factors: List[str]
    supporting_evidence: List[Dict[str, Any]]
    investigator_action: str = "Pending Review"

class HumanReviewAction(BaseModel):
    insight_id: str
    action: str  # CONFIRM, REJECT, MARK_FOR_REVIEW
    notes: Optional[str] = None

class AuditLogEntry(BaseModel):
    log_id: str
    timestamp: str
    user: str
    action: str
    details: str
