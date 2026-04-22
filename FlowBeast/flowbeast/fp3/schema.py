from pydantic import BaseModel
from typing import List

class ViralUnit(BaseModel):
    """FP3 存储的基本单元：爆款基因"""
    hook: str         # 开头钩子
    pattern: str      # 叙事模式
    emotion: List[str] # 情感标签
