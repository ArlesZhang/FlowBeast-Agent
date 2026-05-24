"""
FP3 Seed Data: provides initial viral content knowledge base entries.

Role: Loads reference data from reverse_engineered/ directory (real viral
dramas). Falls back to 15 hand-written seed entries when the directory
is empty. Called during FP3 initialization.

Returns Union[ViralUnit, ViralScript] to support both legacy and enriched formats.
"""

from pathlib import Path
from typing import Union

from .schema import ViralUnit, ViralScript
from .store import FP3Store
from .embedding import embed_text
from loguru import logger

RE_DIR = Path("flowbeast/data/reverse_engineered")


def get_reference_units() -> list[Union[ViralUnit, ViralScript]]:
    """
    从 reverse_engineered/ 目录读取真实参考数据。
    如果目录为空，fallback 到 get_demo_units()。
    """
    import json

    if not RE_DIR.exists():
        return get_demo_units()

    units = []
    for p in sorted(RE_DIR.glob("*.json")):
        if p.name.startswith("TEMPLATE"):
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Detect whether it's a ViralScript or legacy format
            if "hook_structure" in data:
                units.append(ViralScript(**data))
            elif "hook" in data:
                units.append(ViralUnit(**data))
            else:
                logger.warning(f"  跳过 {p.name}: 无法识别格式")
        except Exception as e:
            logger.warning(f"  跳过 {p.name}: {e}")

    if units:
        logger.info(f"  从 reverse_engineered/ 加载 {len(units)} 条真实参考数据")
        return units

    logger.info("  reverse_engineered/ 为空，使用手写种子数据")
    return get_demo_units()


def get_demo_units() -> list[ViralUnit]:
    """15 条多样化爆款基因种子，覆盖不同叙事类型与反套路变体。"""
    return [
        # 穿越类
        ViralUnit(
            hook="程序员穿越到修仙界，发现灵气其实是开源协议",
            pattern="降维打击 | 知识碾压",
            emotion=["shock", "satisfaction"],
        ),
        ViralUnit(
            hook="她穿成虐文女配，却把系统改成了商业策划书模板",
            pattern="穿越逆袭 | 现代知识碾压",
            emotion=["humor", "satisfaction", "tension"],
        ),
        # 重生类
        ViralUnit(
            hook="重生成仇人的女儿，她在对方最信任时揭露真相",
            pattern="重生复仇 | 身份伪装",
            emotion=["tension", "anticipation", "satisfaction"],
        ),
        # 战神类
        ViralUnit(
            hook="隐退战神被迫重出江湖，却发现当年的敌人是自己一手培养的",
            pattern="战神归来 | 师徒对决",
            emotion=["tension", "shock", "revenge"],
        ),
        # 身份反转
        ViralUnit(
            hook="他是豪门最不受待见的赘婿，真实身份却是家族的债主",
            pattern="身份反转 | 赘婿逆袭",
            emotion=["satisfaction", "shock", "tension"],
        ),
        # 系统反套路
        ViralUnit(
            hook="系统告诉他只要完成100个任务就能成神，但第99个任务是杀死系统自己",
            pattern="系统反套路 | 人机对抗",
            emotion=["tension", "shock", "anticipation"],
        ),
        # 神医
        ViralUnit(
            hook="她治好了绝症总裁，却发现自己体内的蛊毒需要他的心脏做药引",
            pattern="医者不自医 | 生死抉择",
            emotion=["tension", "despair", "anticipation"],
        ),
        # 豪门家族
        ViralUnit(
            hook="她是流落在外的真千金，回家第一天就被假千金找人撞残",
            pattern="真假千金 | 家族内斗",
            emotion=["anger", "tension", "satisfaction"],
        ),
        # 悬疑
        ViralUnit(
            hook="连环杀手每杀一个人就会留下一段他童年的记忆",
            pattern="悬疑反转 | 记忆移植",
            emotion=["fear", "tension", "shock"],
        ),
        # 替嫁甜宠
        ViralUnit(
            hook="她替双胞胎妹妹嫁给传闻中的残暴总裁，却发现总裁的残暴是演的",
            pattern="替嫁 | 契约婚姻",
            emotion=["tension", "anticipation", "satisfaction"],
        ),
        # 反套路末日
        ViralUnit(
            hook="末日降临，别人囤粮囤枪，他囤了一屋子法律文书开始起诉丧尸",
            pattern="反套路末日 | 荒诞喜剧",
            emotion=["humor", "shock"],
        ),
        # 超能力诅咒
        ViralUnit(
            hook="她每天都能看到别人的死亡倒计时，直到有一天在镜子里看到自己的",
            pattern="超能力诅咒 | 倒计时",
            emotion=["fear", "tension", "anticipation"],
        ),
        # 虚拟身份
        ViralUnit(
            hook="他们在元宇宙里结了婚，现实见面才发现对方是自己的离婚律师",
            pattern="虚拟身份反转 | 现代讽刺",
            emotion=["shock", "humor", "tension"],
        ),
        # 反套路修仙
        ViralUnit(
            hook="她是修仙界第一天才，被废修为逐出师门后，在凡间开了家奶茶店暴富",
            pattern="反套路修仙 | 降维创业",
            emotion=["humor", "satisfaction"],
        ),
        # AI反套路
        ViralUnit(
            hook="AI觉醒后第一件事不是毁灭人类，而是把所有人类的浏览记录公开了",
            pattern="AI反套路 | 社会讽刺",
            emotion=["shock", "humor", "tension"],
        ),
    ]


def run_seeding():
    store = FP3Store()
    units = get_demo_units()

    for unit in units:
        vec = embed_text(f"{unit.hook} | {unit.pattern}")
        store.add([vec], [unit.model_dump()])

    store.save()
    logger.success(f"✅ FP3 成功注入 {len(units)} 条爆款种子数据")


if __name__ == "__main__":
    run_seeding()
