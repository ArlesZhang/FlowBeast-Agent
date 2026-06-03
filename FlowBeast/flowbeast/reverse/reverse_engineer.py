# flowbeast/reverse/reverse_engineer.py

"""
逆向工程 CLI：将真实漫剧/短剧拆解为 ViralScript 档案，注入 FP3 知识库。

用法：
    uv run python -m flowbeast.reverse.reverse_engineer              # 交互模式
    uv run python -m flowbeast.reverse.reverse_engineer --input f.json  # 从 JSON 导入
    uv run python -m flowbeast.reverse.reverse_engineer --dir ./analyses/ # 批量导入
    uv run python -m flowbeast.reverse.reverse_engineer --from-script script.json  # 从已有脚本提取
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger

# Add project root to path for module execution
REPO_ROOT = Path(__file__).parent.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flowbeast.fp3.schema import (
    ViralScript, HookStructure, ConflictPattern, EmotionalCurve,
    PacingProfile, CharacterArchetype,
)
from flowbeast.fp3.builder import build_fp3

OUTPUT_DIR = Path("flowbeast/data/reverse_engineered")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _ask(prompt: str, default: str = "", required: bool = False) -> str:
    """Prompt with optional default and required enforcement."""
    display = f"{prompt}"
    if default:
        display += f" [{default}]"
    display += ": "

    while True:
        val = input(display).strip()
        if val:
            return val
        if default:
            return default
        if not required:
            return ""
        print("  (必填，不能为空)")


def _ask_int(prompt: str, default: int = 0) -> int:
    while True:
        val = input(f"{prompt} [{default}]: ").strip()
        if not val:
            return default
        try:
            return int(val)
        except ValueError:
            print("  (请输入整数)")


def _ask_float(prompt: str, default: float = 0.0) -> float:
    while True:
        val = input(f"{prompt} [{default}]: ").strip()
        if not val:
            return default
        try:
            return float(val)
        except ValueError:
            print("  (请输入数字)")


def _ask_list(prompt: str, default: list = None) -> list:
    if default is None:
        default = []
    display = f"{prompt}"
    if default:
        display += f" [{', '.join(default)}]"
    val = input(display + ": ").strip()
    if not val and default:
        return list(default)
    if not val:
        return []
    return [x.strip() for x in val.split(",") if x.strip()]


def _ask_choice(prompt: str, choices: list, default_idx: int = 0) -> str:
    print(f"  {prompt}")
    for i, c in enumerate(choices):
        marker = " >" if i == default_idx else "  "
        print(f"    {marker} {i}: {c}")
    while True:
        val = input(f"  选择编号 [{default_idx}]: ").strip()
        if not val:
            return choices[default_idx]
        try:
            idx = int(val)
            if 0 <= idx < len(choices):
                return choices[idx]
        except ValueError:
            pass
        print(f"  (请输入 0-{len(choices) - 1})")


# ====================== Interactive Mode ======================

def interactive_mode() -> Optional[ViralScript]:
    """Step-by-step interactive builder for ViralScript."""
    print("\n" + "=" * 60)
    print("  FlowBeast 逆向工程工具 — 交互式模式")
    print("  将真实漫剧/短剧拆解为 ViralScript 档案")
    print("=" * 60 + "\n")

    # --- Section 1: Source ---
    print("--- [1/7] 来源信息 ---")
    source_title = _ask("剧名", required=True)
    source_platform = _ask_choice("平台", ["红果短剧", "抖音", "快手", "B站", "其他"], 0)
    source_url = _ask("URL（可选）", required=False)
    views = _ask("播放量（可选，如 500万）", required=False)
    viral_metrics = {"views": views} if views else None

    # --- Section 2: Hook Anatomy ---
    print("\n--- [2/7] Hook 解剖 ---")
    opening_line = _ask("第一句台词/画面文字", required=True)
    hook_type = _ask_choice("Hook 类型", [
        "悬念开场", "冲突爆发", "身份错位", "反常行为", "极端情境", "直接宣言"
    ], 0)
    time_to_hook = _ask_choice("钩子出现时机", ["immediate", "within_3s", "delayed"], 0)
    audience_question = _ask("观众看完 hook 后产生的疑问", required=True)
    emotional_payload = _ask("hook 传递的核心情绪", required=True)

    hook_structure = HookStructure(
        opening_line=opening_line,
        hook_type=hook_type,
        time_to_hook=time_to_hook,
        audience_question=audience_question,
        emotional_payload=emotional_payload,
    )

    # --- Section 3: Conflict Pattern ---
    print("\n--- [3/7] 冲突模式 ---")
    conflict_type = _ask("核心冲突类型（如 权力碾压/身份揭露/逻辑反杀）", required=True)
    escalation_raw = _ask("升级曲线（逗号分隔，如 压抑,升级,爆发,反转）", default="压抑,升级,爆发,反转")
    escalation_curve = [x.strip() for x in escalation_raw.split(",")]
    reversal_count = _ask_int("反转次数", 1)
    highest_stakes = _ask_choice("最高赌注", ["尊严", "生存", "情感", "自由", "真相"], 0)

    conflict_pattern = ConflictPattern(
        conflict_type=conflict_type,
        escalation_curve=escalation_curve,
        reversal_count=reversal_count,
        highest_stakes=highest_stakes,
    )

    # --- Section 4: Emotional Curve ---
    print("\n--- [4/7] 情绪曲线 ---")
    emotion_raw = _ask("完整情绪序列（逗号分隔）", default="压抑,震惊,愤怒,爽点")
    curve_sequence = [x.strip() for x in emotion_raw.split(",")]
    peak_emotion = _ask("峰值情绪", default=curve_sequence[-2] if len(curve_sequence) >= 2 else "愤怒")
    peak_position = _ask_choice("峰值位置", ["early", "middle", "late"], 1)
    resolution_type = _ask_choice("结局类型", ["爽点收尾", "悬念留白", "情感余韵", "开放式"], 0)

    emotional_curve = EmotionalCurve(
        curve_sequence=curve_sequence,
        peak_emotion=peak_emotion,
        peak_position=peak_position,
        resolution_type=resolution_type,
    )

    # --- Section 5: Pacing ---
    print("\n--- [5/7] 节奏分析 ---")
    duration_sec = _ask_int("总时长（秒）", 180)
    scene_count = _ask_int("场景数", 5)
    avg_scene = round(duration_sec / max(scene_count, 1), 1)
    beat_raw = _ask("beat 分布（格式: tension=3,payoff=2,reveal=1）", default="tension=3,payoff=2,reveal=1,setup=1")
    beat_distribution = {}
    for pair in beat_raw.split(","):
        pair = pair.strip()
        if "=" in pair:
            k, v = pair.split("=", 1)
            try:
                beat_distribution[k.strip()] = int(v.strip())
            except ValueError:
                pass

    pacing_profile = PacingProfile(
        duration_sec=duration_sec,
        scene_count=scene_count,
        beat_distribution=beat_distribution,
        avg_scene_duration=avg_scene,
    )

    # --- Section 6: Characters ---
    print("\n--- [6/7] 角色原型 ---")
    characters = []
    while True:
        name = _ask(f"角色 {len(characters) + 1} 名称（留空结束）")
        if not name:
            break
        role = _ask_choice("  角色功能", ["protagonist", "antagonist", "mentor", "ally", "neutral"], 0)
        archetype = _ask("  原型标签（如 隐忍逆袭/冷面霸总）", required=True)
        arc = _ask("  转变弧线（一句话描述）", required=True)
        characters.append(CharacterArchetype(name=name, role=role, archetype=archetype, transformation_arc=arc))

    # --- Section 7: Production Notes ---
    print("\n--- [7/7] 制作笔记 ---")
    genre = _ask("题材类型（如 逆袭/战神/豪门/悬疑）", required=True)
    tags_raw = _ask("标签（逗号分隔）", default="逆袭,爽点,身份反转")
    tags = [x.strip() for x in tags_raw.split(",")]
    music_style = _ask("BGM 风格（可选）")
    voice_style = _ask("配音风格（可选）")
    visual_notes = _ask("视觉风格笔记（可选）")
    techniques_raw = _ask("特殊技法（逗号分隔，可选）")
    special_techniques = [x.strip() for x in techniques_raw.split(",") if x.strip()] if techniques_raw else []
    semantic_summary = _ask("一句话总结：这部剧为什么火？（可选）")

    quality_label = _ask_choice("质量标签", ["viral", "average", "failed"], 0)

    # --- Build ---
    script = ViralScript(
        source_title=source_title,
        source_platform=source_platform,
        source_url=source_url or None,
        viral_metrics=viral_metrics,
        quality_label=quality_label,
        genre=genre,
        tags=tags,
        hook_structure=hook_structure,
        conflict_pattern=conflict_pattern,
        emotional_curve=emotional_curve,
        pacing_profile=pacing_profile,
        characters=characters,
        music_style=music_style or None,
        voice_style=voice_style or None,
        visual_style_notes=visual_notes or None,
        special_techniques=special_techniques,
        semantic_summary=semantic_summary or None,
    )

    return script


# ====================== File Import ======================

def load_from_file(path: Path) -> ViralScript:
    """Load a ViralScript from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return ViralScript(**data)


def load_from_dir(dir_path: Path) -> list[ViralScript]:
    """Load all ViralScript JSON files from a directory."""
    scripts = []
    for p in sorted(dir_path.glob("*.json")):
        if p.name.startswith("TEMPLATE"):
            continue
        try:
            scripts.append(load_from_file(p))
            logger.info(f"  已加载: {p.name}")
        except Exception as e:
            logger.warning(f"  跳过 {p.name}: {e}")
    return scripts


# ====================== Script Analysis ======================

def analyze_generated_script(script_json: dict) -> ViralScript:
    """
    从 FlowBeast 生成的 script.json 自动提取 ViralScript 解剖信息。
    Heuristic-based：尽可能从已有字段中推断，缺失部分给默认值。
    """
    scenes = script_json.get("scenes", [])
    dialogue_count = sum(len(s.get("dialogue", [])) for s in scenes)
    conflict = scenes[0].get("conflict", "未知") if scenes else "未知"
    emotion_global = script_json.get("emotion_curve_global", ["压抑", "爽点"])
    core_hook = script_json.get("core_hook", "")
    genre = script_json.get("genre", "通用")
    tags = script_json.get("tags", [])
    title = script_json.get("title", "未命名")

    # Collect beat distribution from scenes if available
    beat_dist = {}
    for scene in scenes:
        c = scene.get("conflict", "")
        beat_dist[c] = beat_dist.get(c, 0) + 1

    total_duration = dialogue_count * 3  # rough estimate: 3s per dialogue

    return ViralScript(
        source_title=title,
        source_platform="FlowBeast",
        viral_metrics=None,
        quality_label="average",  # generated content defaults to average
        genre=genre,
        tags=tags,
        hook_structure=HookStructure(
            opening_line=core_hook,
            hook_type="悬念开场",
            time_to_hook="immediate",
            audience_question="",
            emotional_payload=emotion_global[0] if emotion_global else "压抑",
        ),
        conflict_pattern=ConflictPattern(
            conflict_type=conflict,
            escalation_curve=emotion_global,
            reversal_count=0,
            highest_stakes="尊严",
        ),
        emotional_curve=EmotionalCurve(
            curve_sequence=emotion_global,
            peak_emotion=emotion_global[-1] if emotion_global else "爽点",
            peak_position="late",
            resolution_type="爽点收尾",
        ),
        pacing_profile=PacingProfile(
            duration_sec=total_duration,
            scene_count=len(scenes),
            beat_distribution=beat_dist,
            avg_scene_duration=round(total_duration / max(len(scenes), 1), 1),
        ),
        characters=[],
        music_style=None,
        voice_style=None,
        visual_style_notes=None,
        special_techniques=[],
        semantic_summary=f"FlowBeast 生成 | conflict={conflict}",
    )


# ====================== Save & Inject ======================

def save_script(script: ViralScript, filename: str = None) -> Path:
    """Save ViralScript to JSON with proper Chinese encoding."""
    if filename is None:
        safe_title = "".join(c if c.isalnum() or '一' <= c <= '鿿' else "_" for c in script.source_title[:20])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{safe_title}.json"

    path = OUTPUT_DIR / filename
    data = script.model_dump()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.success(f"  已保存: {path}")
    return path


def inject_to_fp3(script: ViralScript) -> None:
    """Inject ViralScript into FP3 knowledge base."""
    logger.info(f"  正在注入 FP3: [{script.hook[:30]}...]")
    build_fp3([script])
    logger.success(f"  注入成功: [{script.source_title}]")


# ====================== Ingestion Gate ======================

def _gate_before_inject(script: ViralScript, auto_confirm: bool) -> bool:
    """
    Run QualityGate before FP3 injection.

    Returns True if injection should proceed, False if skipped.

    GateAction.ACCEPT  → proceed
    GateAction.REVIEW  → ask user (or auto-proceed if auto_confirm)
    GateAction.REJECT  → always skip (auto_confirm does NOT bypass)
    """
    from flowbeast.observe.quality import GateAction, create_quality_gate

    try:
        gate = create_quality_gate(calibrated=True)
        unit = script.to_viral_unit()
        import asyncio
        decision = asyncio.run(gate.evaluate(unit))
    except Exception as e:
        logger.warning(f"  ⚠️ 入库门控异常，降级放行: {e}")
        return True

    score = decision.score_result.weighted_total
    action = decision.action
    hook_preview = script.hook[:50]

    if action == GateAction.ACCEPT:
        logger.info(f"  ✅ 入库门控通过 | score={score:.3f} | {hook_preview}...")
        return True

    if action == GateAction.REVIEW:
        logger.warning(f"  ⏳ 入库门控 REVIEW | score={score:.3f} | {decision.reason}")
        if auto_confirm:
            logger.info(f"  --yes 模式，自动注入")
            return True
        confirm = input(f"  是否仍要注入? (y/n): ")
        return confirm.strip().lower() == "y"

    # REJECT
    logger.error(f"  ❌ 入库门控拒绝 | score={score:.3f} | {decision.reason}")
    return False


# ====================== Main ======================

def main():
    parser = argparse.ArgumentParser(description="FlowBeast 逆向工程工具")
    parser.add_argument("--input", type=str, help="从单个 JSON 文件导入")
    parser.add_argument("--dir", type=str, help="从目录批量导入 JSON 文件")
    parser.add_argument("--from-script", type=str, help="从 FlowBeast 生成的 script.json 自动提取")
    parser.add_argument("--no-inject", action="store_true", help="仅保存 JSON，不注入 FP3")
    parser.add_argument("--yes", action="store_true", help="自动确认 REVIEW 区入库（不跳过 REJECT）")
    args = parser.parse_args()

    scripts_to_process = []

    if args.input:
        path = Path(args.input)
        if not path.exists():
            logger.error(f"文件不存在: {path}")
            sys.exit(1)
        scripts_to_process.append(("file", load_from_file(path)))

    elif args.dir:
        dir_path = Path(args.dir)
        if not dir_path.exists():
            logger.error(f"目录不存在: {dir_path}")
            sys.exit(1)
        loaded = load_from_dir(dir_path)
        for s in loaded:
            scripts_to_process.append(("batch", s))

    elif args.from_script:
        path = Path(args.from_script)
        if not path.exists():
            logger.error(f"文件不存在: {path}")
            sys.exit(1)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Handle nested structure (production report has "script" key)
        script_body = data.get("script", data)
        scripts_to_process.append(("extracted", analyze_generated_script(script_body)))

    else:
        # Interactive mode
        script = interactive_mode()
        if script:
            scripts_to_process.append(("interactive", script))

    if not scripts_to_process:
        logger.warning("没有数据可处理")
        return

    for source_type, script in scripts_to_process:
        print(f"\n{'=' * 50}")
        print(f"  来源: {source_type}")
        print(f"  标题: {script.source_title}")
        print(f"  平台: {script.source_platform}")
        print(f"  Hook: {script.hook[:50]}...")
        print(f"  质量: {script.quality_label}")
        print(f"{'=' * 50}")

        # Save
        save_script(script)

        # Inject (with ingestion gate)
        if not args.no_inject:
            if _gate_before_inject(script, auto_confirm=args.yes):
                inject_to_fp3(script)
            else:
                logger.warning(f"  ⏭️ 跳过注入: [{script.source_title}]")

    print(f"\n  共处理 {len(scripts_to_process)} 条档案")


if __name__ == "__main__":
    main()
