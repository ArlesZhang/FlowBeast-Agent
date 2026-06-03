"""
GRAFT v0: Viral structure extraction and transfer operator.

Role: Retrieves a ViralScript from FP3, extracts its Hook Structure and
Conflict Pattern, then builds a generation prompt that transfers these
viral structures onto a new topic.

Workflow: topic → FP3 retrieve → extract (Hook + Conflict) → build GRAFT prompt
→ generate_script (called by pipeline with GRAFT prompt override)

This is the first real VTO operator — the core differentiator of FlowBeast.
"""

import json
from typing import Optional

from loguru import logger


class GRAFTResult:
    """Result of a GRAFT operation."""
    def __init__(
        self,
        topic: str,
        source_viral_script: Optional[dict],
        extracted_hook_structure: Optional[dict],
        extracted_conflict_pattern: Optional[dict],
        graft_prompt: str,
        graft_applied: bool,
    ):
        self.topic = topic
        self.source_viral_script = source_viral_script
        self.extracted_hook_structure = extracted_hook_structure
        self.extracted_conflict_pattern = extracted_conflict_pattern
        self.graft_prompt = graft_prompt
        self.graft_applied = graft_applied

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "graft_applied": self.graft_applied,
            "source_viral_script": self.source_viral_script,
            "extracted_hook_structure": self.extracted_hook_structure,
            "extracted_conflict_pattern": self.extracted_conflict_pattern,
            "graft_prompt_summary": self.graft_prompt[:200] if self.graft_prompt else "",
        }


def graft_operator(topic: str) -> GRAFTResult:
    """
    GRAFT v0: Extract viral structure from FP3 and transfer to new topic.

    Steps:
    1. Retrieve best matching ViralScript from FP3
    2. Extract Hook Structure (type, opening pattern, emotional payload)
    3. Extract Conflict Pattern (type, escalation curve, reversal mechanics)
    4. Build a GRAFT prompt that forces the LLM to use these structures
    """
    # Step 1: Retrieve from FP3
    source_script = _retrieve_viral_script(topic)

    if source_script is None:
        logger.warning("⚠️ GRAFT: no viral script retrieved, falling back to standard generation")
        return GRAFTResult(
            topic=topic,
            source_viral_script=None,
            extracted_hook_structure=None,
            extracted_conflict_pattern=None,
            graft_prompt="",
            graft_applied=False,
        )

    # Step 2: Extract Hook Structure
    hook_structure = _extract_hook_structure(source_script)

    # Step 3: Extract Conflict Pattern
    conflict_pattern = _extract_conflict_pattern(source_script)

    # Step 4: Build GRAFT prompt
    graft_prompt = _build_graft_prompt(topic, hook_structure, conflict_pattern, source_script)

    logger.info(
        f"🌿 GRAFT v0 applied | hook_type={hook_structure.get('hook_type', 'N/A')} "
        f"| conflict_type={conflict_pattern.get('conflict_type', 'N/A')} "
        f"| source={source_script.get('source_title', 'seed')}"
    )

    return GRAFTResult(
        topic=topic,
        source_viral_script=_summarize_viral_script(source_script),
        extracted_hook_structure=hook_structure,
        extracted_conflict_pattern=conflict_pattern,
        graft_prompt=graft_prompt,
        graft_applied=True,
    )


def _retrieve_viral_script(topic: str) -> Optional[dict]:
    """Retrieve the best matching ViralScript from FP3 for the given topic."""
    try:
        from flowbeast.fp3.retriever import FP3Retriever

        retriever = FP3Retriever()
        examples = retriever.retrieve(topic, k=1, use_feedback_boost=True)

        if examples:
            return examples[0]
        return None
    except Exception as e:
        logger.error(f"❌ GRAFT retrieval failed: {e}")
        return None


def _extract_hook_structure(viral_script: dict) -> dict:
    """
    Extract Hook Structure from a ViralScript.

    Returns a dict with the structural anatomy of the hook, ready for transfer.
    """
    hs = viral_script.get("hook_structure", {})

    return {
        "hook_type": hs.get("hook_type", "冲突爆发"),
        "opening_line": hs.get("opening_line", viral_script.get("hook", "")),
        "time_to_hook": hs.get("time_to_hook", "immediate"),
        "audience_question": hs.get("audience_question", ""),
        "emotional_payload": hs.get("emotional_payload", ""),
        "source_hook": viral_script.get("hook", ""),
    }


def _extract_conflict_pattern(viral_script: dict) -> dict:
    """
    Extract Conflict Pattern from a ViralScript.

    Returns the conflict engine's structural anatomy.
    """
    cp = viral_script.get("conflict_pattern", {})

    return {
        "conflict_type": cp.get("conflict_type", "权力碾压"),
        "escalation_curve": cp.get("escalation_curve", ["压抑", "升级", "爆发", "反转"]),
        "reversal_count": cp.get("reversal_count", 1),
        "highest_stakes": cp.get("highest_stakes", "尊严"),
    }


def _build_graft_prompt(
    topic: str,
    hook_structure: dict,
    conflict_pattern: dict,
    source_script: dict,
) -> str:
    """
    Build a GRAFT-enhanced prompt that forces the LLM to use the
    extracted viral structure for the new topic.

    This is NOT string concatenation — it's a structural template
    that instructs the LLM to transplant narrative architecture.
    """
    escalation_steps = " → ".join(conflict_pattern.get("escalation_curve", []))

    prompt = f"""你是爆款短剧编剧。请使用以下 GRAFT 病毒结构来创作新剧本。

## 任务主题
{topic}

## GRAFT 病毒结构（必须遵循）

### 一、钩子结构（Hook Architecture）
- **钩子类型**: {hook_structure.get('hook_type', '')}
- **开场模式**: {hook_structure.get('opening_line', '')}
- **触发时机**: {hook_structure.get('time_to_hook', '')}
- **观众疑问**: {hook_structure.get('audience_question', '')}
- **情绪载荷**: {hook_structure.get('emotional_payload', '')}

### 二、冲突引擎（Conflict Engine）
- **冲突类型**: {conflict_pattern.get('conflict_type', '')}
- **升级曲线**: {escalation_steps}
- **反转次数**: {conflict_pattern.get('reversal_count', 1)}
- **最高赌注**: {conflict_pattern.get('highest_stakes', '')}

### 三、参考源（仅供风格参考，不要复制内容）
- 原标题: {source_script.get('source_title', 'N/A')}
- 原始Hook: {source_script.get('hook', '')[:100]}
- 叙事模式: {source_script.get('pattern', '')}

## 结构迁移指令

你必须做到以下几点：

1. **钩子迁移**: 将原始钩子的结构类型应用到新主题。如果原始是"身份错位"型钩子，新剧本也必须在开场建立身份错位，但内容完全关于"{topic}"。

2. **冲突引擎迁移**: 新剧本必须使用相同的冲突类型和升级曲线。冲突的驱动力必须一致，但冲突双方和具体情节必须完全围绕"{topic}"。

3. **情绪载荷保留**: 开场必须触发与原始钩子相同的情绪反应（{hook_structure.get('emotional_payload', '')}），但通过"{topic}"的新情境来实现。

4. **反转机制**: 保持{conflict_pattern.get('reversal_count', 1)}次反转的节奏，反转的触发条件必须来自"{topic}"的内在逻辑。

5. **最高赌注对齐**: 新剧本中角色失去的东西，必须在情感上等价于"{conflict_pattern.get('highest_stakes', '')}"。

## 输出格式

输出 JSON 格式，包含以下字段：
- title: 剧本标题
- core_hook: 核心钩子（一句话）
- genre: 类型
- tags: 标签列表
- emotion_curve_global: 全局情绪曲线标签列表
- scenes: 场景列表，每个场景包含 id, setting, beat_type, dialogue（含 speaker, text, emotion, intensity）

请确保输出纯 JSON，不含其他文字。"""

    return prompt


def _summarize_viral_script(viral_script: dict) -> dict:
    """Create a UI-friendly summary of the source viral script."""
    hs = viral_script.get("hook_structure", {})
    cp = viral_script.get("conflict_pattern", {})

    return {
        "source_title": viral_script.get("source_title", "seed_data"),
        "source_platform": viral_script.get("source_platform", "N/A"),
        "genre": viral_script.get("genre", ""),
        "hook_type": hs.get("hook_type", ""),
        "conflict_type": cp.get("conflict_type", ""),
        "hook_preview": viral_script.get("hook", "")[:150],
        "similarity_score": viral_script.get("_similarity", 0),
    }
