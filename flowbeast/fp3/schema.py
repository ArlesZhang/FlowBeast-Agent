"""
FP3 Schema: dual schema for viral content knowledge base.

Role: Defines ViralUnit (3-field legacy) and ViralScript (enriched drama anatomy).
ViralScript sub-models: HookStructure, ConflictPattern, EmotionalCurve,
PacingProfile, CharacterArchetype. ViralScript.to_viral_unit() provides
backward compatibility with existing ViralUnit code paths.
"""

from pydantic import BaseModel
from typing import Dict, List, Literal, Optional


class ViralUnit(BaseModel):
    """FP3 存储的基本单元：爆款基因"""
    hook: str         # 开头钩子
    pattern: str      # 叙事模式
    emotion: List[str] # 情感标签


# ====================== ViralScript Sub-models ======================

class HookStructure(BaseModel):
    """解剖钩子：第一句话如何抓住观众"""
    opening_line: str           # 第一句台词/画面文字
    hook_type: str              # "悬念开场" / "冲突爆发" / "身份错位" 等
    time_to_hook: str           # "immediate" / "within_3s" / "delayed"
    audience_question: str      # 观众看完 hook 后产生的疑问
    emotional_payload: str      # hook 传递的核心情绪


class ConflictPattern(BaseModel):
    """冲突模式：整部剧的冲突引擎"""
    conflict_type: str          # "权力碾压" / "身份揭露" / "逻辑反杀" 等
    escalation_curve: List[str] # ["压抑", "升级", "爆发", "反转"]
    reversal_count: int
    highest_stakes: str         # "尊严" / "生存" / "情感"


class EmotionalCurve(BaseModel):
    """情绪曲线：观众情绪走势"""
    curve_sequence: List[str]   # ["压抑", "震惊", "愤怒", "爽点"]
    peak_emotion: str
    peak_position: str          # "early" / "middle" / "late"
    resolution_type: str        # "爽点收尾" / "悬念留白" / "情感余韵"


class PacingProfile(BaseModel):
    """节奏档案：时长与 beat 分布"""
    duration_sec: int
    scene_count: int
    beat_distribution: Dict[str, int]
    avg_scene_duration: float


class CharacterArchetype(BaseModel):
    """角色原型"""
    name: str
    role: str                   # "protagonist" / "antagonist" / "mentor"
    archetype: str              # "隐忍逆袭" / "冷面霸总" / "伪善反派"
    transformation_arc: str


# ====================== ViralScript ======================

class ViralScript(BaseModel):
    """
    增强型爆款档案：完整解剖一部漫剧/短剧。
    与 ViralUnit 并存，ViralScript 可降级为 ViralUnit（向后兼容）。
    """
    # 来源
    source_title: str
    source_platform: str                     # "红果短剧" / "抖音" / "快手"
    source_url: Optional[str] = None
    viral_metrics: Optional[Dict] = None     # {"views": ..., "likes": ...}

    # 质量标签（支持正负样本学习）
    quality_label: Literal["viral", "average", "failed"] = "viral"

    # 核心解剖
    genre: str
    tags: List[str]
    hook_structure: HookStructure
    conflict_pattern: ConflictPattern
    emotional_curve: EmotionalCurve
    pacing_profile: PacingProfile
    characters: List[CharacterArchetype] = []

    # 制作笔记
    music_style: Optional[str] = None
    voice_style: Optional[str] = None
    visual_style_notes: Optional[str] = None
    special_techniques: List[str] = []

    # Prompt-centric fields (v0.4.0 — Viral Prompt Compiler)
    prompt_atoms: List[str] = []              # atom_id references to PromptAtom instances
    vertical_name: Optional[str] = None       # which vertical library this script uses

    # 语义层（保留 latent 表达空间，防过度模板化）
    latent_embedding: Optional[List[float]] = None
    semantic_summary: Optional[str] = None   # "这部剧为什么火"一句话

    # 向后兼容属性（从子结构计算，供 FAISS 搜索用）
    @property
    def hook(self) -> str:
        return self.hook_structure.opening_line

    @property
    def pattern(self) -> str:
        return f"{self.genre} | {self.conflict_pattern.conflict_type}"

    @property
    def emotion(self) -> List[str]:
        return self.emotional_curve.curve_sequence

    def to_viral_unit(self) -> ViralUnit:
        """降级为三字段 ViralUnit，供现有搜索管线用。"""
        return ViralUnit(hook=self.hook, pattern=self.pattern, emotion=self.emotion)
