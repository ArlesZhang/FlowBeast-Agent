"""FP3 Embedding — delegates to core.providers for real vector generation."""

from flowbeast.core.providers import embed_text as _core_embed


def embed_text(text: str) -> list:
    """将文本转化为 embedding 向量。"""
    return _core_embed(text)


def embed_unit(unit) -> list:
    """将 ViralUnit 或 ViralScript 转化为可嵌入的文本，然后获取向量。

    ViralScript 使用深层结构拼接的高可读性拉片文本，保留 hook_structure、
    conflict_pattern、emotional_curve 等字段作为语义锚点，防止降级抹杀灵魂。
    """
    if hasattr(unit, "hook_structure"):  # ViralScript
        text = (
            f"hook_type: {unit.hook_structure.hook_type} | "
            f"opening: {unit.hook_structure.opening_line} | "
            f"audience_question: {unit.hook_structure.audience_question} | "
            f"genre: {unit.genre} tags: {' '.join(unit.tags)} | "
            f"conflict: {unit.conflict_pattern.conflict_type} | "
            f"escalation: {' '.join(unit.conflict_pattern.escalation_curve)} | "
            f"emotion_curve: {' '.join(unit.emotional_curve.curve_sequence)} | "
            f"peak: {unit.emotional_curve.peak_emotion} at {unit.emotional_curve.peak_position} | "
            f"resolution: {unit.emotional_curve.resolution_type} | "
            f"beats: {unit.pacing_profile.beat_distribution} | "
            f"techniques: {' '.join(unit.special_techniques)}"
        )
    else:
        # ViralUnit legacy
        text = f"hook: {unit.hook} pattern: {unit.pattern} emotion: {' '.join(unit.emotion)}"
    return embed_text(text)
