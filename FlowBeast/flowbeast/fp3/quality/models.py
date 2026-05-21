from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

# FP3质量评估相关数据模型
class GateAction(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    REVIEW = "review"

# 质量评估结果模型
class CategoryScore(BaseModel):
    name: str
    score: float = Field(ge=0.0, le=1.0)
    weight: float = Field(ge=0.0, le=1.0)
    explanation: str

# 计算加权总分
class ScoreResult(BaseModel):
    category_scores: Dict[str, float]
    weighted_total: float = Field(ge=0.0, le=1.0)
    explanations: Dict[str, str]
    scorer_version: str = "rule-based-v1"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# 重复性检测结果模型
class DedupResult(BaseModel):
    is_duplicate: bool
    similarity_score: float
    closest_match: Optional[Dict] = None
    closest_distance: Optional[float] = None
    threshold_used: float
    duplicate_checks_performed: int = 0

# 最终决策模型
class GateDecision(BaseModel):
    candidate_hook: str
    action: GateAction
    score_result: ScoreResult
    dedup_result: DedupResult
    reason: str
    audit_trail: Dict = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
