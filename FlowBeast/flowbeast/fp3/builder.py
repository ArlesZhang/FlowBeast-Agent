"""
FP3 Builder: constructs and saves the FAISS vector knowledge base.

Role: Accepts ViralUnit or ViralScript entries, embeds them via cloud API,
stores vectors + metadata in FAISS index. Called during FP3 initialization
and when reverse-engineered ViralScript records are injected.

Workflow: seed_data.py / reverse_engineered/ → embedding.py → this → store.py → retriever.py
"""

from typing import Union

from loguru import logger
from .schema import ViralUnit, ViralScript
from .embedding import embed_unit
from .store import FP3Store


def build_fp3(units: list[Union[ViralUnit, ViralScript]]):
    """核心构建函数：将 ViralUnit / ViralScript 列表转化为向量库"""
    store = FP3Store()

    vectors = []
    items = []

    for u in units:
        hook_preview = u.hook[:15] if hasattr(u, "hook") else str(u)[:15]
        logger.debug(f"正在处理基因: {hook_preview}...")
        vec = embed_unit(u)
        vectors.append(vec)
        items.append(u.model_dump())

    store.add(vectors, items)
    store.save()
    logger.success(f"🔥 FP3 索引构建成功！已入库 {len(units)} 条爆款基因。")

if __name__ == "__main__":
    from .seed_data import get_demo_units
    build_fp3(get_demo_units())
