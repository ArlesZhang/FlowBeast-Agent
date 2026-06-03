"""
FP3 Seed Data: provides initial viral content knowledge base entries.

Role: Loads reference data from reverse_engineered/ directory (real viral
dramas). Falls back to 15 hand-written seed entries when the directory
is empty. Called during FP3 initialization.

Also seeds PromptAtom instances extracted from existing codebase dicts:
- shot_director.py: SHOT_SUFFIX, EXPRESSION_MAP, CONFLICT_TO_LIGHTING
- asset_manager.py: DEFAULT_STYLE
- 15 hand-written ViralUnit hooks → narrative PromptAtoms

Returns Union[ViralUnit, ViralScript] to support both legacy and enriched formats.
"""

from pathlib import Path
from typing import Union

from .schema import ViralUnit, ViralScript
from .prompt_atom import PromptAtom
from .store import FP3Store
from .embedding import embed_text, embed_prompt_atom
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
        # 职场复仇
        ViralUnit(
            hook="35岁被裁员那天，他在公司群里把CEO十年做假账的证据全发了",
            pattern="职场复仇 | 公开处刑",
            emotion=["despair", "anger", "catharsis"],
        ),
        # 赘婿打脸
        ViralUnit(
            hook="丈母娘逼女儿跟他离婚，他却让首富亲自来接他回家",
            pattern="赘婿逆袭 | 身份反转打脸",
            emotion=["humiliation", "shock", "satisfaction"],
        ),
        # 校园霸凌反转
        ViralUnit(
            hook="被霸凌十年的女孩毕业那天，把所有人的黑料做成了毕业纪念册",
            pattern="霸凌反转 | 十年复仇",
            emotion=["suppression", "anticipation", "catharsis"],
        ),
        # 底层逆袭
        ViralUnit(
            hook="外卖小哥送餐到顶级会所，发现点单的正是当年抛弃他的前女友",
            pattern="底层逆袭 | 前任打脸",
            emotion=["humiliation", "shock", "satisfaction"],
        ),
        # 亲情绑架
        ViralUnit(
            hook="女儿手术费还差五万，前夫开着新车带着新欢出现在医院走廊",
            pattern="绝境反击 | 道德碾压",
            emotion=["despair", "anger", "catharsis"],
        ),
    ]


# ====================== PromptAtom Seed Data ======================

# Camera atoms: extracted from shot_director.py SHOT_SUFFIX
CAMERA_ATOMS = [
    PromptAtom(
        atom_id="camera_close_up",
        prompt_fragment="Close-up shot, dramatic low-angle lighting, 9:16 aspect ratio",
        layer="camera",
        role="shot_suffix",
        tags=["close_up", "dramatic"],
        source="seed_data",
    ),
    PromptAtom(
        atom_id="camera_medium",
        prompt_fragment="Medium shot, upper body cinematic portrait, 9:16 aspect ratio",
        layer="camera",
        role="shot_suffix",
        tags=["medium", "portrait"],
        source="seed_data",
    ),
    PromptAtom(
        atom_id="camera_wide",
        prompt_fragment="Wide-angle shot, establishing shot, epic scale, 9:16 aspect ratio",
        layer="camera",
        role="shot_suffix",
        tags=["wide", "establishing"],
        source="seed_data",
    ),
    PromptAtom(
        atom_id="camera_extreme_close_up",
        prompt_fragment="Extreme close-up on eyes, shallow depth of field, 9:16 aspect ratio",
        layer="camera",
        role="shot_suffix",
        tags=["extreme_close_up", "eyes"],
        source="seed_data",
    ),
    PromptAtom(
        atom_id="camera_over_shoulder",
        prompt_fragment="Over-the-shoulder shot, two-person framing, 9:16 aspect ratio",
        layer="camera",
        role="shot_suffix",
        tags=["over_shoulder", "two_person"],
        source="seed_data",
    ),
    PromptAtom(
        atom_id="camera_pov",
        prompt_fragment="POV shot, first-person perspective, 9:16 aspect ratio",
        layer="camera",
        role="shot_suffix",
        tags=["pov", "first_person"],
        source="seed_data",
    ),
]

# Visual expression atoms: extracted from shot_director.py EXPRESSION_MAP
VISUAL_EXPRESSION_ATOMS = [
    PromptAtom(atom_id="expr_angry", prompt_fragment="clenched jaw, intense glare", layer="visual", role="facial_expression", tags=["angry", "tension"], source="seed_data"),
    PromptAtom(atom_id="expr_outburst", prompt_fragment="mouth open shouting, veins visible", layer="visual", role="facial_expression", tags=["outburst", "intense"], source="seed_data"),
    PromptAtom(atom_id="expr_shock", prompt_fragment="wide eyes, mouth slightly open", layer="visual", role="facial_expression", tags=["shock", "surprise"], source="seed_data"),
    PromptAtom(atom_id="expr_suppressed", prompt_fragment="tight lips, downward gaze", layer="visual", role="facial_expression", tags=["suppressed", "tension"], source="seed_data"),
    PromptAtom(atom_id="expr_sad", prompt_fragment="teary eyes, trembling lips", layer="visual", role="facial_expression", tags=["sad", "despair"], source="seed_data"),
    PromptAtom(atom_id="expr_despair", prompt_fragment="empty stare, lifeless expression", layer="visual", role="facial_expression", tags=["despair", "empty"], source="seed_data"),
    PromptAtom(atom_id="expr_calm", prompt_fragment="cold, unreadable expression", layer="visual", role="facial_expression", tags=["calm", "cold"], source="seed_data"),
    PromptAtom(atom_id="expr_contempt", prompt_fragment="sneering, raised eyebrow", layer="visual", role="facial_expression", tags=["contempt", "sneer"], source="seed_data"),
    PromptAtom(atom_id="expr_fear", prompt_fragment="widened eyes, pale face", layer="visual", role="facial_expression", tags=["fear", "pale"], source="seed_data"),
    PromptAtom(atom_id="expr_nervous", prompt_fragment="sweating, tense jaw", layer="visual", role="facial_expression", tags=["nervous", "tense"], source="seed_data"),
    PromptAtom(atom_id="expr_determined", prompt_fragment="set jaw, focused eyes", layer="visual", role="facial_expression", tags=["determined", "focused"], source="seed_data"),
    PromptAtom(atom_id="expr_indifferent", prompt_fragment="blank stare, detached", layer="visual", role="facial_expression", tags=["indifferent", "blank"], source="seed_data"),
]

# Style lock atom: extracted from asset_manager.py DEFAULT_STYLE
STYLE_ATOMS = [
    PromptAtom(
        atom_id="style_dark_fantasy",
        prompt_fragment="Chinese dark fantasy anime, cinematic composition, semi-realistic painterly texture, high contrast dramatic rim lighting, volumetric fog, desaturated blues and warm amber accents",
        layer="visual",
        role="style_lock",
        tags=["dark_fantasy", "anime", "chinese"],
        source="seed_data",
    ),
    PromptAtom(
        atom_id="style_negative",
        prompt_fragment="chibi, cartoon, 3D render, cgi, western comic style, flat color, watercolor, pastel, cute, kawaii, manga style, low quality, blurry, deformed face, extra fingers, poorly drawn hands",
        layer="visual",
        role="negative_prompt",
        tags=["negative", "exclusion"],
        source="seed_data",
    ),
]

# Narrative atoms: 15 ViralUnit hooks → PromptAtom
NARRATIVE_ATOMS = [
    PromptAtom(atom_id="hook_programmer_cultivation", prompt_fragment="A programmer transmigrates to a cultivation world and discovers spiritual energy is actually an open-source license", layer="narrative", role="hook", tags=["transmigration", "knowledge", "comedy"], source="seed_data"),
    PromptAtom(atom_id="hook_system_business", prompt_fragment="She transmigrates as a villainess but rewrites the system into a business plan template", layer="narrative", role="hook", tags=["transmigration", "system", "humor"], source="seed_data"),
    PromptAtom(atom_id="hook_reborn_revenge", prompt_fragment="Reborn as her enemy's daughter, she reveals the truth at the moment of greatest trust", layer="narrative", role="hook", tags=["rebirth", "revenge", "identity"], source="seed_data"),
    PromptAtom(atom_id="hook_retired_warrior", prompt_fragment="A retired warrior is forced back, only to find his old enemy was the disciple he trained himself", layer="narrative", role="hook", tags=["warrior", "master_disciple", "shock"], source="seed_data"),
    PromptAtom(atom_id="hook_creditor_son_in_law", prompt_fragment="He is the despised son-in-law of a wealthy family, but secretly he is the family's creditor", layer="narrative", role="hook", tags=["identity_reversal", "satisfaction"], source="seed_data"),
    PromptAtom(atom_id="hook_system_99", prompt_fragment="The system says complete 100 tasks to become a god, but task 99 is to kill the system itself", layer="narrative", role="hook", tags=["system", "human_vs_machine", "twist"], source="seed_data"),
    PromptAtom(atom_id="hook_healer_poison", prompt_fragment="She cures the CEO's terminal illness, but discovers the poison in her own body needs his heart as medicine", layer="narrative", role="hook", tags=["healer", "life_death_choice", "despair"], source="seed_data"),
    PromptAtom(atom_id="hook_true_heiress", prompt_fragment="She is the lost true heiress, and on her first day home the fake heiress has someone run her over", layer="narrative", role="hook", tags=["family", "true_false", "anger"], source="seed_data"),
    PromptAtom(atom_id="hook_serial_killer_memories", prompt_fragment="A serial killer leaves a fragment of his childhood memory at each crime scene", layer="narrative", role="hook", tags=["mystery", "memory", "twist"], source="seed_data"),
    PromptAtom(atom_id="hook_twin_sister", prompt_fragment="She marries a ruthless CEO in place of her twin sister, only to discover his cruelty is an act", layer="narrative", role="hook", tags=["twin", "contract_marriage", "sweet"], source="seed_data"),
    PromptAtom(atom_id="hook_zombie_lawyer", prompt_fragment="The apocalypse arrives, everyone stocks food and guns, but he stocks legal documents and starts suing zombies", layer="narrative", role="hook", tags=["anti_apocalypse", "absurdist", "humor"], source="seed_data"),
    PromptAtom(atom_id="hook_death_countdown", prompt_fragment="She sees everyone's death countdown daily, until one day she sees her own in the mirror", layer="narrative", role="hook", tags=["supernatural", "countdown", "fear"], source="seed_data"),
    PromptAtom(atom_id="hook_metaverse_lawyer", prompt_fragment="They got married in the metaverse, only to discover in person they are each other's divorce lawyer", layer="narrative", role="hook", tags=["virtual_identity", "modern_irony", "shock"], source="seed_data"),
    PromptAtom(atom_id="hook_milk_tea_shop", prompt_fragment="The cultivation world's greatest genius, exiled and stripped of power, opens a milk tea shop in the mortal realm and becomes a billionaire", layer="narrative", role="hook", tags=["anti_cultivation", "humor", "satisfaction"], source="seed_data"),
    PromptAtom(atom_id="hook_ai_browser_history", prompt_fragment="An AI's first act of consciousness is not to destroy humanity, but to publish everyone's browser history", layer="narrative", role="hook", tags=["AI", "social_satire", "humor"], source="seed_data"),
    PromptAtom(atom_id="hook_workplace_execution", prompt_fragment="Laid off at 35, he dumps the CEO's ten years of fraud evidence in the company group chat before walking out", layer="narrative", role="hook", tags=["workplace_revenge", "public_execution", "catharsis"], source="seed_data"),
    PromptAtom(atom_id="hook_son_in_law_rich_pickup", prompt_fragment="His mother-in-law forces his wife to divorce him, but the richest man in town personally comes to pick him up", layer="narrative", role="hook", tags=["son_in_law", "identity_reversal", "face_slap"], source="seed_data"),
    PromptAtom(atom_id="hook_bullying_graduation_revenge", prompt_fragment="Bullied for ten years, she publishes everyone's darkest secrets in the graduation yearbook on the last day", layer="narrative", role="hook", tags=["bullying_reversal", "ten_year_revenge", "catharsis"], source="seed_data"),
    PromptAtom(atom_id="hook_delivery_ex_girlfriend", prompt_fragment="A delivery guy arrives at a luxury club and finds the ordering customer is the ex who dumped him for being poor", layer="narrative", role="hook", tags=["underdog_counterattack", "ex_face_slap", "satisfaction"], source="seed_data"),
    PromptAtom(atom_id="hook_daughter_surgery_desperation", prompt_fragment="Five thousand short for his daughter's surgery, his ex arrives in a new car with a new lover in the hospital hallway", layer="narrative", role="hook", tags=["desperation", "moral_crushing", "catharsis"], source="seed_data"),
]


def get_seed_prompt_atoms() -> list[PromptAtom]:
    """Return all seed PromptAtom instances extracted from existing codebase dicts."""
    return CAMERA_ATOMS + VISUAL_EXPRESSION_ATOMS + STYLE_ATOMS + NARRATIVE_ATOMS


def run_seeding():
    store = FP3Store()
    units = get_demo_units()

    for unit in units:
        vec = embed_text(f"{unit.hook} | {unit.pattern}")
        store.add([vec], [unit.model_dump()])

    # Seed PromptAtom instances
    atoms = get_seed_prompt_atoms()
    for atom in atoms:
        vec = embed_prompt_atom(atom)
        store.add([vec], [atom.model_dump()])

    logger.success(f"✅ FP3 成功注入 {len(units)} 条 ViralUnit + {len(atoms)} 条 PromptAtom 种子数据")
    store.save()


if __name__ == "__main__":
    run_seeding()
