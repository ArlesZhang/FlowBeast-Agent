from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class GateAction(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    REVIEW = "review"


class CategoryScore(BaseModel):
    name: str
    score: float = Field(ge=0.0, le=1.0)
    weight: float = Field(ge=0.0, le=1.0)
    explanation: str


class ScoreResult(BaseModel):
    category_scores: Dict[str, float]
    weighted_total: float = Field(ge=0.0, le=1.0)
    explanations: Dict[str, str]
    scorer_version: str = "rule-based-v1"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DedupResult(BaseModel):
    is_duplicate: bool
    similarity_score: float
    closest_match: Optional[Dict] = None
    closest_distance: Optional[float] = None
    threshold_used: float
    duplicate_checks_performed: int = 0


class GateDecision(BaseModel):
    candidate_hook: str
    action: GateAction
    score_result: ScoreResult
    dedup_result: DedupResult
    reason: str
    audit_trail: Dict = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
