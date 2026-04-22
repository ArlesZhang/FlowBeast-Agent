import os
import sys
import asyncio
from pathlib import Path
from loguru import logger

# 1. 强制锁定项目根目录，确保 flowbeast 包能被识别
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 2. 尝试导入核心组件
try:
    from flowbeast.fp3.seed_data import run_seeding
    from flowbeast.drama.pipeline import DramaPipeline
    from flowbeast.core.config import settings, FP3_INDEX_PATH
    # 注意：这里我们不需要在 main 顶部导入 injector，
    # 因为它会被 DramaPipeline 内部调用。
    logger.success("✅ FlowBeast 核心模块加载成功")
except ImportError as e:
    logger.error(f"❌ 模块导入失败: {e}")
    # 诊断：打印出当前路径下的文件，确认结构
    logger.info(f"📂 当前运行目录内容: {[f.name for f in BASE_DIR.iterdir()]}")
    sys.exit(1)

async def main():
    logger.info("🔥 FlowBeast 流量巨兽系统正式启动...")

    # 3. 自动化 FP3 知识库初始化
    # 如果索引不存在，则说明是首次运行，注入种子爆款基因
    if not FP3_INDEX_PATH.exists():
        logger.warning(f"📍 未检测到知识库索引 ({FP3_INDEX_PATH.name})，正在执行初始化注入...")
        try:
            run_seeding()
            logger.success("✨ FP3 种子数据注入成功！")
        except Exception as seeding_error:
            logger.error(f"❌ 种子注入失败: {seeding_error}")
            return
    else:
        logger.info("✅ 检测到既有知识库索引，跳过初始化阶段。")

    # 4. 实例化 Drama 工作流管线
    # 此时 DramaPipeline 内部会实例化 FP3Retriever 和 PromptInjector
    try:
        pipeline = DramaPipeline()
    except Exception as init_error:
        logger.error(f"❌ 工作流初始化失败: {init_error}")
        return

    # 5. 设定今日任务主题：硬核跨界爽点
    target_topic = "程序员穿越到修仙界，发现灵气其实是某种高维代码，他通过重构底层逻辑实现 root 权限"
    logger.info(f"🚀 正在为主题生成爆款剧本: {target_topic}")

    # 6. 执行全自动生成流程 (RAG 增强)
    try:
        # execute_workflow 会自动调用 FP3 进行基因检索，并注入 Prompt
        script = await pipeline.execute_workflow(target_topic)
        
        # 7. 打印最终成果 (用于 Phase 2 渲染引擎的 JSON 数据结构)
        print("\n" + "🚀" + "="*60)
        print(f"🎬 剧本标题: {script.title}")
        print(f"📝 爆款梗概: {script.summary}")
        print("-" * 62)
        
        for i, scene in enumerate(script.scenes):
            print(f"【镜头 {i+1}】| {scene.time}")
            print(f"👁️ 视觉画面: {scene.visual[:60]}...")
            print(f"🎵 音频旁白: {scene.audio[:60]}...")
            print("-" * 30)
            
        print("="*60 + "🏁\n")
        
        logger.success("🏁 FlowBeast Phase 1 MVP 流程全链路跑通！")

    except Exception as e:
        logger.exception(f"❌ 工作流运行异常，请检查 LLM API 或 Prompt 模板: {e}")

if __name__ == "__main__":
    # 使用 asyncio 运行异步主函数
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 用户手动停止系统。")
