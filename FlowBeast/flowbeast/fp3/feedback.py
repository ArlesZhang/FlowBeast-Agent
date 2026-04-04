# 核心逻辑层:这个文件负责把 generator.py 产出的复杂 script.json 降维打击，提取成 ViralUnit 格式

import json
from pathlib import Path
from loguru import logger
from .schema import ViralUnit
from .builder import build_fp3

class FP3Feedback:
    @staticmethod
    def extract_unit_from_script(script_data: dict) -> ViralUnit:
        """
        从生成的剧本 JSON 中提取爆款基因
        """
        # 提取逻辑：对齐 generator 输出的字段
        script_body = script_data.get("script", {})

        # 1. 提取 Hook
        hook = script_body.get("core_hook") or script_body.get("title", "未命名基因")

        # 2. 提取 Pattern (从第一个场景的 conflict 结合整个 genre)
        genre = script_body.get("genre", "通用")
        pattern = f"{genre} | {script_body.get('tags', ['未知模式'])[0]}"

        # 3. 提取 Emotion
        emotion = script_body.get("emotion_curve_global", ["neutral"])

        return ViralUnit(
            hook=hook,
            pattern=pattern,
            emotion=emotion
        )

    def process_file(self, file_path: Path, auto_confirm: bool = False):
        """
        处理单个剧本文件并回流
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 校验是否是有效的生成结果
            if "script" not in data:
                logger.warning(f"跳过无效文件: {file_path.name}")
                return

            unit = self.extract_unit_from_script(data)

            logger.info(f"🧬 提取到新基因: [Hook: {unit.hook[:20]}...]")

            if not auto_confirm:
                confirm = input("是否确认将此基因回流至 FP3 知识库? (y/n): ")
                if confirm.lower() != 'y':
                    logger.info("已取消回流")
                    return

            # 执行回流（调用我们已经跑通的 builder）
            build_fp3([unit])
            logger.success(f"✨ 进化成功！基因已写入 FP3 索引。")

        except Exception as e:
            logger.error(f"回流处理失败: {e}")
