import argparse
import sys
from pathlib import Path

from loguru import logger

# 1. 将项目根目录加入 sys.path，保证可 import flowbeast
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 2. 核心依赖：与 flowbeast.drama.pipeline.run_full_pipeline 对齐
try:
    from flowbeast.core.config import FP3_INDEX_PATH
    from flowbeast.drama.pipeline import run_full_pipeline
    from flowbeast.fp3.seed_data import run_seeding
except ImportError as e:
    logger.error(f"❌ 模块导入失败: {e}")
    logger.info(f"📂 当前项目根目录: {BASE_DIR!s}")
    sys.exit(1)

logger.success("✅ FlowBeast 核心模块加载成功")


def main() -> None:
    parser = argparse.ArgumentParser(description="FlowBeast Viral Prompt Compiler")
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Topic for drama generation (default: hardcoded xianxia topic)",
    )
    args = parser.parse_args()

    logger.info("🔥 FlowBeast 启动（全链路：剧本 JSON + 配音 + 报告）...")

    if not FP3_INDEX_PATH.exists():
        logger.warning(
            f"📍 未检测到知识库索引 ({FP3_INDEX_PATH.name})，正在执行种子注入..."
        )
        try:
            run_seeding()
            logger.success("✨ FP3 种子数据注入成功！")
        except Exception as e:
            logger.error(f"❌ 种子注入失败: {e}")
            return
    else:
        logger.info("✅ 已检测到知识库索引，跳过种子注入。")

    target_topic = (
        args.topic
        or "程序员穿越到修仙界，发现灵气其实是某种高维代码，"
        "他通过重构底层逻辑实现 root 权限"
    )
    logger.info(f"🚀 主题: {target_topic}")

    try:
        result = run_full_pipeline(target_topic)
    except Exception as e:
        logger.exception(f"❌ 流水线异常，请检查 LLM API 与 .env: {e}")
        return

    if result is None:
        logger.error("❌ 流水线未正常结束（如剧本生成失败）。")
        return

    print("\n" + "🎬" + "=" * 58)
    print("本 run 产出路径")
    print("-" * 60)
    print(f"run_id     : {result['run_id']}")
    print(f"目录       : {result['base_path']}")
    print(f"剧本 JSON  : {result['script_path']}")
    print(f"生产报告   : {result['report_path']}")
    print(f"音频目录   : {result['audio_path']}")
    print("=" * 60 + "🏁\n")

    logger.success("🏁 全链路跑通。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 已手动停止。")
