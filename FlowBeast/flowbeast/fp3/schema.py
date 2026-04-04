from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ViralMaterial(BaseModel):
    """FP3 存储的基本单元"""
    content: str
    style: str = "drama"
    hooks: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RetrievalResult(BaseModel):
    """检索返回的包装类，带上相似度分数"""
    material: ViralMaterial
    score: float
