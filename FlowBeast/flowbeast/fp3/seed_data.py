# flowbeast/fp3/seed_data.py
# 仅作为演示，不建议作为主要生产脚本

from flowbeast.fp3.store import FP3Store
from flowbeast.fp3.embedding import embed_text
from loguru import logger

def run_seeding():
    store = FP3Store()
    seeds = [
        {"content": "程序员穿越修仙界，用重构逻辑改写功法", "hooks": ["代码即神通"], "style": "drama"},
        {"content": "冷艳总裁开除赘婿，发现他是全球芯片大亨", "hooks": ["身份反转"], "style": "drama"}
    ]
    
    for item in seeds:
        vec = embed_text(item["content"])
        store.add([vec], [item])
    
    store.save()
    logger.success(f"✅ 成功注入 {len(seeds)} 条爆款种子数据")
