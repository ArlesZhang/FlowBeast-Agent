"""
Feedback extraction: convert generated script JSON into FP3-compatible units.

Role: Extracts ViralUnit/ViralScript from generator output so engagement
feedback can be mapped back to the atoms that produced it.

Workflow: generator produces script.json → extract_unit() → feedback_ingest maps engagement
"""

from flowbeast.fp3.schema import ViralUnit
from loguru import logger


def extract_unit_from_script(script_data: dict) -> ViralUnit:
    """
    Extract a ViralUnit from a generated script JSON.
    Used by feedback_ingest to map engagement data back to FP3 atoms.
    """
    script_body = script_data.get("script", {})

    hook = script_body.get("core_hook") or script_body.get("title", "unnamed")
    genre = script_body.get("genre", "generic")
    pattern = f"{genre} | {script_body.get('tags', ['unknown'])[0]}"
    emotion = script_body.get("emotion_curve_global", ["neutral"])

    return ViralUnit(hook=hook, pattern=pattern, emotion=emotion)


def extract_viral_script_from_script(script_data: dict):
    """
    Extract full ViralScript anatomy from generated script JSON.
    Delegates to reverse_engineer.analyze_generated_script.
    """
    from flowbeast.reverse.reverse_engineer import analyze_generated_script

    script_body = script_data.get("script", script_data)
    return analyze_generated_script(script_body)
