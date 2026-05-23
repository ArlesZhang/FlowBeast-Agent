# flowbeast/drama/shot_director.py

"""
Shot Director: converts script JSON into a full cinematic shot list.

Primary driver: beat_type (情绪节拍) — not shot_type.
Audience feels: 压迫 → 停顿 → 爆发 → 反转 → 爽点
Not: 远景 → 中景 → 特写
"""

from dataclasses import dataclass, field, asdict
from typing import Optional


# ====================== Beat Type Definitions ======================

BEAT_TYPE_MAP = {
    "setup": {
        "duration_range": (5, 6),
        "motion_intensity_range": (1, 3),
        "camera_motion": "slow_pan",
        "bgm_state": "soft_build",
        "description": "铺垫/建立",
    },
    "tension": {
        "duration_range": (4, 5),
        "motion_intensity_range": (2, 4),
        "camera_motion": "slow_push_in",
        "bgm_state": "tension_build",
        "description": "压迫/张力",
    },
    "reveal": {
        "duration_range": (3, 4),
        "motion_intensity_range": (2, 4),
        "camera_motion": "push_in",
        "bgm_state": "sudden_silence",
        "description": "身份揭露/转折",
    },
    "payoff": {
        "duration_range": (2, 3),
        "motion_intensity_range": (4, 6),
        "camera_motion": "quick_cut",
        "bgm_state": "explosion",
        "description": "爽点/打脸",
    },
    "reaction": {
        "duration_range": (2, 3),
        "motion_intensity_range": (1, 2),
        "camera_motion": "static",
        "bgm_state": "silent",
        "description": "角色反应",
    },
    "cliffhanger": {
        "duration_range": (1, 2),
        "motion_intensity_range": (1, 2),
        "camera_motion": "freeze_frame",
        "bgm_state": "abrupt_cut",
        "description": "悬念/钩子",
    },
    "emotional_pause": {
        "duration_range": (5, 7),
        "motion_intensity_range": (1, 2),
        "camera_motion": "slow_pull_out",
        "bgm_state": "gentle",
        "description": "情感余韵",
    },
}

# Conflict type → default beat_type
# Includes LLM-generated synonyms and compound variants.
CONFLICT_TO_BEAT = {
    "羞辱": "tension",
    "逆袭": "payoff",
    "打脸": "payoff",
    "背叛": "reveal",
    "对峙": "tension",
    "揭秘": "reveal",
    "反转": "reveal",
    "开场": "setup",
    "悬念": "cliffhanger",
    "余韵": "emotional_pause",
    # Expanded: LLM synonyms
    "追杀": "tension",
    "逃亡": "tension",
    "羞辱": "tension",
    "权力碾压": "tension",
    "生存剥夺": "tension",
    "权力监控": "tension",
    "身份揭露": "reveal",
    "认知颠覆": "reveal",
    "逻辑反杀": "payoff",
    "权力反转": "payoff",
    "权力翻转": "payoff",
    "理念交锋": "tension",
    "情感余韵": "emotional_pause",
    "代价承担": "emotional_pause",
    "混沌破局": "payoff",
    "虚假温情": "tension",
    "尊严剥夺": "tension",
    "追杀": "tension",
    "能力泄露": "reveal",
    "规则对抗": "tension",
}

# Emotion → shot_type mapping
EMOTION_TO_SHOT = {
    "愤怒": "close_up",
    "爆发": "close_up",
    "震惊": "medium",
    "压抑": "medium",
    "悲伤": "close_up",
    "绝望": "close_up",
    "冷静": "medium",
    "轻蔑": "close_up",
    "恐惧": "close_up",
    "紧张": "medium",
    "坚定": "medium",
    "冷漠": "wide",
}

# Conflict → environment lighting
CONFLICT_TO_LIGHTING = {
    "羞辱": "harsh_fluorescent",
    "逆袭": "dramatic_backlight",
    "打脸": "high_contrast",
    "背叛": "cold_blue",
    "对峙": "split_lighting",
    "揭秘": "low_key_shadow",
    "反转": "dramatic_rim",
    "开场": "establishing_natural",
    "悬念": "low_key_shadow",
    "余韵": "warm_golden",
    "追杀": "low_key_shadow",
    "逃亡": "cold_blue",
    "权力碾压": "harsh_fluorescent",
    "生存剥夺": "harsh_fluorescent",
    "身份揭露": "dramatic_rim",
    "认知颠覆": "low_key_shadow",
    "权力反转": "dramatic_backlight",
    "权力翻转": "dramatic_backlight",
    "逻辑反杀": "high_contrast",
    "理念交锋": "split_lighting",
    "情感余韵": "warm_golden",
    "代价承担": "warm_golden",
    "混沌破局": "dramatic_rim",
    "虚假温情": "warm_low_key",
    "尊严剥夺": "harsh_fluorescent",
    "能力泄露": "dramatic_rim",
    "规则对抗": "split_lighting",
}

# SFX presets per beat type
BEAT_TO_SFX = {
    "setup": ["ambient"],
    "tension": ["low_hum", "heartbeat"],
    "reveal": ["sudden_silence", "sharp_inhale"],
    "payoff": ["impact", "whoosh"],
    "reaction": ["breath"],
    "cliffhanger": ["abrupt_cut", "high_tone"],
    "emotional_pause": ["soft_ambient"],
}


# ====================== Close-up Motion Clamp ======================

def clamp_motion_intensity(shot_type: str, beat_type: str, base_intensity: int) -> int:
    """
    Close-up 强制限速：面部特写 motion_intensity 绝不超过 3。

    可灵 2.0 图生视频中，close-up 只要 motion_intensity > 4，
    角色五官就会像橡皮泥一样融化变型。武戏爆发只能留给
    全景/中景的特效粒子去表达。
    """
    if shot_type == "close_up":
        return min(base_intensity, 3)
    return base_intensity


# ====================== Shot Dataclass ======================

@dataclass
class Shot:
    shot_id: str                       # "S01_SH03"
    scene_id: int
    beat_type: str                     # setup, tension, reveal, payoff, reaction, cliffhanger, emotional_pause
    shot_type: str                     # close_up, medium, wide
    camera_motion: str                 # slow_push_in, pan_left, static, etc.
    duration_sec: int
    motion_intensity: int              # 1-10, auto-derived, clamped for close-up
    emotion: str
    character_action: str
    facial_expression: str
    environment: str
    lighting: str
    dialogue: str
    speaker: str
    secondary_characters: list[str] = field(default_factory=list)
    sfx: list[str] = field(default_factory=list)
    bgm_state: str = "soft_build"
    visual_prompt: str = ""            # filled by asset_manager with Style Lock
    negative_prompt: str = ""          # goes to API field, not in positive prompt
    transition_in: str = "cut"
    transition_out: str = "cut"

    def to_dict(self) -> dict:
        return asdict(self)


# ====================== Visual Prompt Suffixes ======================

SHOT_SUFFIX = {
    "close_up": "Close-up shot, dramatic low-angle lighting, 9:16 aspect ratio",
    "medium": "Medium shot, upper body cinematic portrait, 9:16 aspect ratio",
    "wide": "Wide-angle shot, establishing shot, epic scale, 9:16 aspect ratio",
    "extreme_close_up": "Extreme close-up on eyes, shallow depth of field, 9:16 aspect ratio",
    "over_shoulder": "Over-the-shoulder shot, two-person framing, 9:16 aspect ratio",
    "pov": "POV shot, first-person perspective, 9:16 aspect ratio",
}


def get_shot_suffix(shot_type: str) -> str:
    return SHOT_SUFFIX.get(shot_type, SHOT_SUFFIX["medium"])


# ====================== Beat Type Inference ======================

def _normalize_conflict(conflict: str) -> str:
    """
    Clean compound conflict strings like '生存剥夺 / 系统碾压' into known keys.
    LLMs often generate compound/dirty conflict types — this normalizes them.
    """
    # Strip whitespace, split on common separators
    conflict = conflict.strip()
    if " / " in conflict or "/" in conflict:
        parts = [p.strip() for p in conflict.replace(" / ", "/").split("/")]
        # Return first part that matches a known key
        for part in parts:
            if part in CONFLICT_TO_BEAT:
                return part
        # If no exact match, try substring matching
        for part in parts:
            for key in CONFLICT_TO_BEAT:
                if key in part or part in key:
                    return key
    elif conflict in CONFLICT_TO_BEAT:
        return conflict
    else:
        # Substring match for dirty strings like "权力碾压/尊严剥夺"
        for key in CONFLICT_TO_BEAT:
            if key in conflict:
                return key

    return conflict


def infer_beat_type(dialogue: dict, scene: dict, position: str) -> str:
    """
    Infer beat_type from dialogue content, scene conflict type, and position in scene.

    position: "first" | "middle" | "last"
    """
    emotion = dialogue.get("emotion", "")
    intensity = dialogue.get("intensity", 5) or 5
    conflict = _normalize_conflict(scene.get("conflict", ""))

    # First dialogue in scene → usually setup
    if position == "first":
        if conflict in ("开场",):
            return "setup"
        if conflict in ("羞辱", "对峙"):
            return "tension"
        if conflict in ("逆袭", "打脸"):
            return "payoff"

    # Last dialogue → cliffhanger or emotional_pause
    if position == "last":
        if scene.get("climax"):
            return "cliffhanger"
        if intensity <= 3:
            return "emotional_pause"
        return "cliffhanger"

    # Middle: driven by emotion + intensity
    if emotion in ("愤怒", "爆发") and intensity >= 7:
        return "payoff"
    if emotion in ("震惊",):
        return "reveal"
    if emotion in ("压抑", "紧张") and intensity >= 5:
        return "tension"
    if emotion in ("悲伤", "绝望") and intensity <= 4:
        return "reaction"
    if conflict in ("背叛", "揭秘", "反转"):
        return "reveal"

    # Default based on conflict
    return CONFLICT_TO_BEAT.get(conflict, "setup")


def infer_shot_type(emotion: str, beat_type: str) -> str:
    """Infer shot type from emotion and beat."""
    if beat_type == "payoff" and emotion in ("愤怒", "爆发"):
        return "close_up"
    if beat_type == "reaction":
        return "close_up"
    if beat_type == "cliffhanger":
        return "medium"
    if beat_type == "setup":
        return "wide"
    if beat_type == "emotional_pause":
        return "medium"

    return EMOTION_TO_SHOT.get(emotion, "medium")


def infer_facial_expression(emotion: str, beat_type: str) -> str:
    EXPRESSION_MAP = {
        "愤怒": "clenched jaw, intense glare",
        "爆发": "mouth open shouting, veins visible",
        "震惊": "wide eyes, mouth slightly open",
        "压抑": "tight lips, downward gaze",
        "悲伤": "teary eyes, trembling lips",
        "绝望": "empty stare, lifeless expression",
        "冷静": "cold, unreadable expression",
        "轻蔑": "sneering, raised eyebrow",
        "恐惧": "widened eyes, pale face",
        "紧张": "sweating, tense jaw",
        "坚定": "set jaw, focused eyes",
        "冷漠": "blank stare, detached",
    }

    if beat_type == "reaction":
        return "frozen expression, subtle micro-expression"
    if beat_type == "cliffhanger":
        return "frozen mid-expression, dramatic pause"

    return EXPRESSION_MAP.get(emotion, "neutral expression, subtle emotion")


def infer_character_action(beat_type: str, emotion: str, dialogue_text: str) -> str:
    """Generate simple character action description from beat context."""
    ACTIONS = {
        ("payoff", "愤怒"): "slams hand on table, stands up aggressively",
        ("payoff", "冷静"): "delivers final line with cold precision",
        ("tension", "压抑"): "grips chair arm, knuckles white",
        ("tension", "紧张"): "shifts weight, avoids eye contact",
        ("reveal", "震惊"): "steps back slowly, hand covering mouth",
        ("reveal", "冷静"): "reveals truth with steady gaze",
        ("reaction", "悲伤"): "looks down, single tear",
        ("reaction", "绝望"): "collapses onto chair, shoulders slumped",
        ("cliffhanger", "愤怒"): "points finger, cuts off mid-sentence",
        ("cliffhanger", "震惊"): "freezes mid-reaction, screen holds",
        ("emotional_pause", "悲伤"): "looks out window, rain reflection",
        ("setup", "冷静"): "enters scene, surveys surroundings",
    }

    key = (beat_type, emotion)
    if key in ACTIONS:
        return ACTIONS[key]

    # Generic fallbacks
    if beat_type == "payoff":
        return "delivers decisive line with authority"
    if beat_type == "tension":
        return "tense body language, restrained movement"
    if beat_type == "reveal":
        return "reveals information with dramatic weight"

    return "subtle movement, natural acting"


# ====================== Main Builder ======================

def build_shot_list(script: dict) -> list[Shot]:
    """
    Convert a Script dict into a full Shot Director list.

    Each dialogue line becomes one Shot, with beat_type, shot_type,
    motion_intensity, camera_motion, visual_prompt scaffolding.
    """
    shots = []
    global_shot_counter = 0

    for scene in script.get("scenes", []):
        scene_id = scene.get("id", 0)
        dialogue_list = scene.get("dialogue", [])
        conflict = scene.get("conflict", "")
        emotion_curve = scene.get("emotion_curve", [])
        environment = scene.get("summary", "indoor scene")
        lighting = CONFLICT_TO_LIGHTING.get(conflict, "natural")

        num_lines = len(dialogue_list)

        for idx, line in enumerate(dialogue_list):
            position = "first" if idx == 0 else ("last" if idx == num_lines - 1 else "middle")
            emotion = line.get("emotion", "冷静") or "冷静"
            intensity = line.get("intensity", 5) or 5

            # Infer beat type
            beat_type = infer_beat_type(line, scene, position)

            # Infer shot type
            shot_type = infer_shot_type(emotion, beat_type)

            # Beat params
            beat_params = BEAT_TYPE_MAP.get(beat_type, BEAT_TYPE_MAP["setup"])
            duration = beat_params["duration_range"][0]
            base_intensity = beat_params["motion_intensity_range"][1]

            # Override intensity from dialogue emotion
            if intensity >= 8:
                base_intensity = max(base_intensity, 5)
            elif intensity <= 3:
                base_intensity = min(base_intensity, 2)

            # Clamp for close-up (hard rule)
            motion_intensity = clamp_motion_intensity(shot_type, beat_type, base_intensity)

            camera_motion = beat_params["camera_motion"]
            bgm_state = beat_params["bgm_state"]
            sfx = list(BEAT_TO_SFX.get(beat_type, ["ambient"]))

            facial_expression = infer_facial_expression(emotion, beat_type)
            character_action = infer_character_action(beat_type, emotion, line.get("text", ""))

            global_shot_counter += 1
            shot_id = f"S{scene_id:02d}_SH{global_shot_counter:03d}"

            shot = Shot(
                shot_id=shot_id,
                scene_id=scene_id,
                beat_type=beat_type,
                shot_type=shot_type,
                camera_motion=camera_motion,
                duration_sec=duration,
                motion_intensity=motion_intensity,
                emotion=emotion,
                character_action=character_action,
                facial_expression=facial_expression,
                environment=environment,
                lighting=lighting,
                dialogue=line.get("text", ""),
                speaker=line.get("speaker", "Unknown"),
                sfx=sfx,
                bgm_state=bgm_state,
                transition_in="cut" if idx == 0 else "cut_on_action",
                transition_out="cut" if idx == num_lines - 1 else "cut_on_action",
            )

            shots.append(shot)

    logger = __import__("loguru").logger
    logger.info(f"Shot Director: built {len(shots)} shots from {len(script.get('scenes', []))} scenes")

    # Validation: close-up motion clamp audit
    violations = [s for s in shots if s.shot_type == "close_up" and s.motion_intensity > 3]
    if violations:
        for v in violations:
            logger.warning(f"VIOLATION: {v.shot_id} close_up motion_intensity={v.motion_intensity} (must be <= 3)")
    else:
        logger.success("Motion clamp check: all close_up shots within limit (<= 3)")

    return shots


def shots_to_json(shots: list[Shot]) -> list[dict]:
    """Convert Shot list to JSON-serializable dicts."""
    return [s.to_dict() for s in shots]


def load_shot_list_from_json(json_path: str) -> list[Shot]:
    """Load Shot list from a previously saved JSON file."""
    import json

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    shots = []
    for item in data:
        shot = Shot(
            shot_id=item["shot_id"],
            scene_id=item["scene_id"],
            beat_type=item["beat_type"],
            shot_type=item["shot_type"],
            camera_motion=item["camera_motion"],
            duration_sec=item["duration_sec"],
            motion_intensity=item["motion_intensity"],
            emotion=item["emotion"],
            character_action=item["character_action"],
            facial_expression=item["facial_expression"],
            environment=item["environment"],
            lighting=item["lighting"],
            dialogue=item["dialogue"],
            speaker=item["speaker"],
            secondary_characters=item.get("secondary_characters", []),
            sfx=item.get("sfx", []),
            bgm_state=item.get("bgm_state", "soft_build"),
            visual_prompt=item.get("visual_prompt", ""),
            negative_prompt=item.get("negative_prompt", ""),
            transition_in=item.get("transition_in", "cut"),
            transition_out=item.get("transition_out", "cut"),
        )
        shots.append(shot)

    return shots
