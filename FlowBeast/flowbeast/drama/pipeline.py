import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from flowbeast.core.config import settings
from flowbeast.drama.generator import generate_script
from flowbeast.drama.audio import generate_audio

# ====================== 全局配置 ======================
AUDIO_PROVIDER = "edge"

# 输出质量门控阈值（与 FP3 入库阈值不同）
OUTPUT_QUALITY_ACCEPT = 0.65
OUTPUT_QUALITY_REJECT = 0.45
OUTPUT_QUALITY_MAX_RETRIES = 2


# ====================== 输出质量门控 ======================
def _run_output_quality_gate(script: dict) -> dict:
    """
    Score generated script through QualityGate (rule-based, free, no LLM calls).
    Returns {"passed": bool, "score": float, "action": str, "reason": str}
    """
    try:
        from flowbeast.fp3.schema import ViralUnit
        from flowbeast.fp3.quality import GateAction
        from flowbeast.fp3.quality.scorer import RuleBasedScorer
        from flowbeast.fp3.quality.dedup import EmbeddingDeduplicator
        from flowbeast.fp3.quality.gate import QualityGate
        from flowbeast.fp3.quality.config import quality_settings
        from flowbeast.fp3.store import FP3Store

        # 从脚本中提取 ViralUnit 用于评分
        unit = ViralUnit(
            hook=script.get("core_hook", ""),
            pattern=script.get("genre", "") + " | " + ", ".join(script.get("tags", [])[:2]),
            emotion=script.get("emotion_curve_global", []),
        )

        store = FP3Store()
        scorer = RuleBasedScorer(weights=quality_settings.weights_dict)
        deduplicator = EmbeddingDeduplicator(
            similarity_threshold=quality_settings.DEDUP_SIMILARITY_THRESHOLD,
            search_k=quality_settings.DEDUP_SEARCH_K,
        )
        gate = QualityGate(
            scorer=scorer,
            deduplicator=deduplicator,
            store=store,
            accept_threshold=OUTPUT_QUALITY_ACCEPT,
            review_threshold=OUTPUT_QUALITY_REJECT,
        )

        import asyncio
        decision = asyncio.run(gate.evaluate(unit))

        return {
            "passed": decision.action in (GateAction.ACCEPT, GateAction.REVIEW),
            "score": decision.score_result.weighted_total,
            "action": decision.action.value,
            "reason": decision.reason,
        }

    except Exception as e:
        logger.warning(f"⚠️ 输出质量门控失败，放行: {e}")
        return {"passed": True, "score": 0.0, "action": "pass_through", "reason": str(e)}


# ====================== 主流水线 ======================
def run_full_pipeline(topic: str):
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    logger.info(f"🚀 FlowBeast 启动 | topic={topic} | run_id={run_id}")

    # ====================== 1. 大脑（IP2）======================
    script = None
    meta = None
    quality_result = None
    generation_attempts = 0

    for retry in range(OUTPUT_QUALITY_MAX_RETRIES + 1):
        generation_attempts += 1
        logger.info(f"📝 第 {generation_attempts} 次脚本生成...")

        try:
            result = generate_script(topic, auto_trend=True)
            script = result["script"]
            meta = result["meta"]

            logger.success(f"✅ 剧本生成成功 | Model: {meta['model']}")

        except Exception as e:
            logger.exception(f"❌ 剧本生成失败: {e}")
            return None

        # ====================== 2. 输出质量门控 ======================
        quality_result = _run_output_quality_gate(script)
        logger.info(
            f"🔍 质量评分: {quality_result['score']:.2f} | "
            f"结果: {quality_result['action']} | "
            f"原因: {quality_result['reason']}"
        )

        if quality_result.get("passed", True):
            break

        # 质量不达标，重试
        if retry < OUTPUT_QUALITY_MAX_RETRIES:
            logger.warning(
                f"⚠️ 质量未达标（{quality_result['score']:.2f} < {OUTPUT_QUALITY_REJECT}），"
                f"第 {retry + 1} 次重试生成..."
            )
        else:
            logger.error(
                f"❌ 连续 {generation_attempts} 次生成质量未达标，"
                f"以最低分通过（宁缺毋滥原则：本次标记为 low_quality）"
            )
            meta["low_quality"] = True

    # ====================== 3. 存储（统一路径）======================
    base_path = Path(settings.FLOWBEAST_OUTPUT_DIR) / run_id
    audio_path = base_path / "audio"

    base_path.mkdir(parents=True, exist_ok=True)
    audio_path.mkdir(parents=True, exist_ok=True)

    script_file = base_path / "script.json"

    with open(script_file, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    logger.success(f"📦 剧本已存储: {script_file}")

    # ====================== 4. 产能（音频生成）======================
    logger.info(f"🎬 开始配音 | provider={AUDIO_PROVIDER}")

    success_count = 0
    fail_count = 0

    for scene in script.get("scenes", []):
        scene_id = scene.get("id", 0)

        for line_id, line in enumerate(scene.get("dialogue", [])):
            try:
                output_path = generate_audio(
                    text=line["text"],
                    scene_id=scene_id,
                    line_id=line_id,
                    speaker=line["speaker"],
                    provider=AUDIO_PROVIDER,
                    output_dir=str(audio_path),
                    emotion=line.get("emotion"),
                    intensity=line.get("intensity"),
                )

                logger.info(f"🎧 S{scene_id}-L{line_id} -> {Path(output_path).name}")
                success_count += 1

            except Exception as e:
                logger.error(f"❌ S{scene_id}-L{line_id} 失败: {e}")
                fail_count += 1

    # ====================== 5. 总结 ======================
    logger.success(
        f"""
✨ Pipeline 完成
-------------------------
topic       : {topic}
run_id      : {run_id}
script_path : {script_file}
audio_dir   : {audio_path}
success     : {success_count}
failed      : {fail_count}
-------------------------
"""
    )

    # ====================== 6. 生产报告（为 FP2/自进化准备） ======================
    report = {
        "run_id": run_id,
        "topic": topic,
        "model": meta.get("model"),
        "status": "completed" if fail_count == 0 else "partial",
        "generation_attempts": generation_attempts,

        # --- 质量门控 ---
        "quality": {
            "score": quality_result.get("score", 0),
            "action": quality_result.get("action", ""),
            "reason": quality_result.get("reason", ""),
        },

        # --- 核心指标回流 ---
        "analytics": {
            "total_scenes": len(script.get("scenes", [])),
            "audio_assets": success_count,
            "core_hook": script.get("core_hook", ""),
            "global_emotion_curve": script.get("emotion_curve_global", []),
        },

        # --- 时间线 ---
        "created_at": meta.get("timestamp"),
        "finished_at": datetime.now().isoformat(),
    }

    report_file = base_path / "production_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    logger.success(f"📊 生产报告已生成: {report_file}")

    return {
        "run_id": run_id,
        "base_path": base_path,
        "script_path": script_file,
        "report_path": report_file,
        "audio_path": audio_path,
    }


# ====================== 批量入口（测试 / 数据采集）======================
if __name__ == "__main__":
    test_topics = [
        "OpenAI,Meta,Google同时宣布'超级Agent'计划后，人类第一次发现：公司不再需要员工了",
        "2030年，99%的白领被AI淘汰，而真正掌控世界的，只剩下那1%拥有Agent矩阵的人",
        "全球第一批Agent创业公司出现后，普通人第一次被系统性淘汰",
    ]

    for topic in test_topics:
        run_full_pipeline(topic)
