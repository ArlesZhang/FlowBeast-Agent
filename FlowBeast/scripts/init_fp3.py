from flowbeast.fp3.schema import ViralUnit
from flowbeast.fp3.store import FP3Store
from flowbeast.fp3.embedding import embed_unit
from loguru import logger

def run_init():
    store = FP3Store()
    units = [
        ViralUnit(hook="他程序员出身，却在修仙界重写底层协议", pattern="降维打击", emotion=["shock", "cool"]),
        ViralUnit(hook="她被开除后，前东家求她回去救命", pattern="身份反转", emotion=["satisfaction"])
    ]
    
    vectors = []
    items = []
    for u in units:
        vectors.append(embed_unit(u))
        items.append(u.dict())
    
    store.add(vectors, items)
    store.save()
    logger.success("✅ FP3 初始基因库构建完成！")

if __name__ == "__main__":
    run_init()
