# 核心逻辑层:这个文件负责把 generator.py 产出的复杂 script.json 降维打击，提取成 ViralUnit/ViralScript 格式

import asyncio
import json
from pathlib import Path
from typing import Optional, Union
from loguru import logger
from .schema import ViralUnit, ViralScript
from .builder import build_fp3


class FP3Feedback:
    @staticmethod
    def extract_unit_from_script(script_data: dict) -> ViralUnit:
        """
        从生成的剧本 JSON 中提取爆款基因（保留旧接口，向后兼容）
        """
        script_body = script_data.get("script", {})

        hook = script_body.get("core_hook") or script_body.get("title", "未命名基因")
        genre = script_body.get("genre", "通用")
        pattern = f"{genre} | {script_body.get('tags', ['未知模式'])[0]}"
        emotion = script_body.get("emotion_curve_global", ["neutral"])

        return ViralUnit(hook=hook, pattern=pattern, emotion=emotion)

    @staticmethod
    def extract_viral_script_from_script(script_data: dict) -> ViralScript:
        """
        从生成的剧本 JSON 中提取完整 ViralScript 解剖信息。
        委托给 reverse_engineer.analyze_generated_script。
        """
        from flowbeast.tools.reverse_engineer import analyze_generated_script

        script_body = script_data.get("script", script_data)
        return analyze_generated_script(script_body)

    def process_file(self, file_path: Path, auto_confirm: bool = False):
        """
        处理单个剧本文件并回流（同步兼容接口）
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

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

            build_fp3([unit])
            logger.success(f"✨ 进化成功！基因已写入 FP3 索引。")

        except Exception as e:
            logger.error(f"回流处理失败: {e}")

    async def process_file_async(self, file_path: Path, auto_confirm: bool = False, use_viral_script: bool = True) -> Optional["GateDecision"]:
        """
        处理单个剧本文件，通过 QualityGate 评估后回流。
        返回 GateDecision 或 None（如果文件无效或被取消）。

        Args:
            use_viral_script: If True, extract full ViralScript (enriched).
                              If False, use legacy ViralUnit.
        """
        from .quality import create_quality_gate, GateAction, GateDecision

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "script" not in data:
                logger.warning(f"跳过无效文件: {file_path.name}")
                return None

            if use_viral_script:
                unit = self.extract_viral_script_from_script(data)
            else:
                unit = self.extract_unit_from_script(data)

            hook_preview = unit.hook[:20]
            logger.info(f"🧬 提取到新基因: [Hook: {hook_preview}...]")

            if not auto_confirm:
                confirm = input("是否确认将此基因提交至 QualityGate? (y/n): ")
                if confirm.lower() != 'y':
                    logger.info("已取消回流")
                    return None

            gate = create_quality_gate(calibrated=True)
            decision = await gate.evaluate_and_store(unit)

            if decision.action == GateAction.ACCEPT:
                logger.success(
                    f"✅ 基因通过 QualityGate (score={decision.score_result.weighted_total:.3f})"
                )
            elif decision.action == GateAction.REVIEW:
                logger.warning(
                    f"⏳ 基因标记 REVIEW (score={decision.score_result.weighted_total:.3f}): {decision.reason}"
                )
            else:
                logger.warning(
                    f"❌ 基因被 QualityGate 拒绝 (score={decision.score_result.weighted_total:.3f}): {decision.reason}"
                )

            return decision

        except Exception as e:
            logger.error(f"QualityGate 处理失败: {e}")
            return None
