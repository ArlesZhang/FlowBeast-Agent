import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from flowbeast.core.config import settings
from flowbeast.drama.generator import generate_script
from flowbeast.drama.audio import generate_audio

# ====================== 全局配置 ======================
AUDIO_PROVIDER = "edge"


# ====================== 主流水线 ======================
def run_full_pipeline(topic: str):
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    logger.info(f"🚀 FlowBeast 启动 | topic={topic} | run_id={run_id}")

    # ====================== 1. 大脑（IP2）======================
    try:
       result = generate_script(topic) 
       script = result["script"]   
       meta = result["meta"]            
    
       logger.success(f"✅ 剧本生成成功 | Model: {meta['model']}")

    except Exception as e:
        logger.exception(f"❌ 剧本生成失败: {e}")
        return

    # ====================== 2. 存储（统一路径）======================
    base_path = Path(settings.DATA_SAVE_PATH) / run_id
    audio_path = base_path / "audio"

    base_path.mkdir(parents=True, exist_ok=True)
    audio_path.mkdir(parents=True, exist_ok=True)

    script_file = base_path / "script.json"

    with open(script_file, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    logger.success(f"📦 剧本已存储: {script_file}")

    # ====================== 3. 产能（音频生成）======================
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

    # ====================== 4. 总结（为未来数据回流准备）======================
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

# ====================== 5. 生产报告（为 FP2/自进化准备） ======================
    report = {
        "run_id": run_id,
        "topic": topic,
        "model": meta.get("model"),
        "status": "completed" if fail_count == 0 else "partial",
        
        # --- 核心指标回流 ---
        "analytics": {
            "total_scenes": len(script.get("scenes", [])),
            "audio_assets": success_count,
            "core_hook": script.get("core_hook", ""),
            "global_emotion_curve": script.get("emotion_curve_global", []),
        },
        
        # --- 时间线 ---
        "created_at": meta.get("timestamp"),
        "finished_at": datetime.now().isoformat()
    }

    report_file = base_path / "production_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    logger.success(f"📊 生产报告已生成: {report_file}")


# ====================== 批量入口（测试 / 数据采集）======================
if __name__ == "__main__":
    test_topics = [
        "逆袭：被开除后的百亿首富",
        "校园：穷小子获得神豪系统",
        "战神：归来发现女儿住狗窝"
    ]

    for topic in test_topics:
        run_full_pipeline(topic)
