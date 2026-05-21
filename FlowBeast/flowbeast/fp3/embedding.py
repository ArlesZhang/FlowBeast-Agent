"""FP3 Embedding — delegates to core.providers for real vector generation."""

from flowbeast.core.providers import embed_text as _core_embed


def embed_text(text: str) -> list:
    """将文本转化为 embedding 向量。"""
    return _core_embed(text)


def embed_unit(unit) -> list:
    """将 ViralUnit 转化为可嵌入的文本，然后获取向量。"""
    text = f"hook: {unit.hook} pattern: {unit.pattern} emotion: {' '.join(unit.emotion)}"
    return embed_text(text)
