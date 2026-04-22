# flowbeast/drama/schema.py

from typing import List, TypedDict, Optional


# ====================== 基础结构 ======================
class Dialogue(TypedDict):
    speaker: str
    text: str
    emotion: Optional[str]          # 情绪标签（愤怒/震惊/压抑/爆发）
    intensity: Optional[int]        # 情绪强度（1-10）


# ====================== 场景结构 ======================
class Scene(TypedDict):
    id: int

    # --- 爆款核心 ---
    hook: str                      # 开头钩子（前3秒）
    conflict: str                  # 冲突类型（羞辱 / 逆袭 / 打脸 / 背叛）
    emotion_curve: List[str]       # 情绪变化路径

    # --- 内容 ---
    summary: str                   # 场景一句话总结
    dialogue: List[Dialogue]

    # --- 节奏控制 ---
    pace: Optional[str]            # fast / medium / slow
    climax: Optional[bool]         # 是否高潮点


# ====================== 剧本结构 ======================
class Script(TypedDict):
    title: str
    genre: Optional[str]           # 战神 / 校园 / 豪门 / 逆袭
    target_audience: Optional[str] # 用户画像（下沉市场 / 女性 / 爽文用户）

    # --- 爆款建模 ---
    core_hook: str                 # 整体大钩子（标题党核心）
    tags: List[str]                # 标签（系统 / 神豪 / 复仇 / 重生）
    emotion_curve_global: List[str]# 全局情绪曲线

    # --- 内容 ---
    scenes: List[Scene]

    # --- 可选：为FP3做准备 ---
    viral_score: Optional[float]   # 爆款评分（后期回流用）
