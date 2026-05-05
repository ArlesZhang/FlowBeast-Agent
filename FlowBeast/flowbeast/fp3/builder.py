from loguru import logger
from .schema import ViralUnit
from .embedding import embed_unit
from .store import FP3Store

# workflow: seed_data.py --> embedding.py --> builder.py --> store.py --> retriever.py
def build_fp3(units: list[ViralUnit]):
    """核心构建函数：将 ViralUnit 列表转化为向量库"""
    store = FP3Store()
    
    vectors = []
    items = []
    
    for u in units:
        logger.debug(f"正在处理基因: {u.hook[:15]}...")
        # 调用 embedding.py 里的向量化工具
        vec = embed_unit(u)
        vectors.append(vec)
        items.append(u.model_dump()) # Pydantic v2 使用 model_dump()
    
    store.add(vectors, items)
    store.save()
    logger.success(f"🔥 FP3 索引构建成功！已入库 {len(units)} 条爆款基因。")

if __name__ == "__main__":
    from .seed_data import get_demo_units
    build_fp3(get_demo_units())
