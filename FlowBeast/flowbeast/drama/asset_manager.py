# flowbeast/drama/asset_manager.py

"""
Asset Manager: character, scene, and Style Lock asset management.

Core principle: assets are REUSED + RECOMPOSED, not regenerated per shot.
Style Lock prevents AI style drift across the entire episode.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from loguru import logger

from flowbeast.drama.shot_director import Shot, get_shot_suffix


# ====================== Style Lock ======================

@dataclass
class StyleLock:
    """
    Visual style lock — prevents AI drift across all shots in one episode.

    Positive style suffix goes at END of visual_prompt (Transformer attention).
    Negative prompt goes to API field separately (not mixed in positive).
    """
    visual_style_suffix: str       # "Chinese dark fantasy anime, cinematic composition, semi-realistic painterly texture"
    negative_prompt: str           # "chibi, cartoon, 3D render, cgi, western comic..."
    aspect_ratio: str              # "9:16 aspect ratio"
    color_palette: dict = None     # {"primary": "#1a2a3a", "accent": "#c4956a", ...}
    render_rules: dict = None      # {"mode": "2D", "shadow_intensity": 0.7, "grain": 0.1}

    def __post_init__(self):
        if self.color_palette is None:
            self.color_palette = {}
        if self.render_rules is None:
            self.render_rules = {}


# Default Style Lock for Chinese drama anime (国漫黑暗奇幻)
DEFAULT_STYLE = StyleLock(
    visual_style_suffix="Chinese dark fantasy anime, cinematic composition, semi-realistic painterly texture, high contrast dramatic rim lighting, volumetric fog, desaturated blues and warm amber accents",
    negative_prompt="chibi, cartoon, 3D render, cgi, western comic style, flat color, watercolor, pastel, cute, kawaii, manga style, low quality, blurry, deformed face, extra fingers, poorly drawn hands",
    aspect_ratio="9:16 aspect ratio",
    color_palette={
        "primary": "#1a2a3a",
        "accent": "#c4956a",
        "shadow": "#0a0f14",
        "highlight": "#e8d5b5",
    },
    render_rules={
        "mode": "2D+3D hybrid",
        "shadow_intensity": 0.7,
        "grain": 0.1,
        "line_weight": "medium-thin",
    },
)


# ====================== Asset Loading ======================

def get_character_prompt(name: str, asset_dir: Path) -> str:
    """Load character prompt template from asset directory."""
    char_path = asset_dir / name / "prompt_template.txt"
    if char_path.exists():
        return char_path.read_text(encoding="utf-8").strip()

    logger.warning(f"Character asset not found: {char_path}, using name as prompt")
    return name


def get_character_metadata(name: str, asset_dir: Path) -> dict:
    """Load character metadata (voice_tag, height, etc.)."""
    meta_path = asset_dir / name / "metadata.json"
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return {"name": name}


def get_scene_prompt(scene_name: str, asset_dir: Path) -> str:
    """Load scene prompt template from asset directory."""
    scene_path = asset_dir / scene_name / "prompt_template.txt"
    if scene_path.exists():
        return scene_path.read_text(encoding="utf-8").strip()

    logger.warning(f"Scene asset not found: {scene_path}, using scene_name")
    return scene_name


def save_character_assets(character: dict, asset_dir: Path) -> Path:
    """
    Save character assets to directory.

    character dict should have: name, prompt_template, metadata, reference_images
    """
    name = character["name"]
    char_dir = asset_dir / name
    char_dir.mkdir(parents=True, exist_ok=True)

    # Save prompt template
    prompt_path = char_dir / "prompt_template.txt"
    prompt_path.write_text(character.get("prompt_template", name), encoding="utf-8")

    # Save metadata
    meta_path = char_dir / "metadata.json"
    meta_path.write_text(
        json.dumps(character.get("metadata", {}), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    logger.info(f"Character assets saved: {char_dir}")
    return char_dir


def save_scene_assets(scene: dict, asset_dir: Path) -> Path:
    """Save scene assets to directory."""
    name = scene["name"]
    scene_dir = asset_dir / name
    scene_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = scene_dir / "prompt_template.txt"
    prompt_path.write_text(scene.get("prompt_template", name), encoding="utf-8")

    meta_path = scene_dir / "metadata.json"
    meta_path.write_text(
        json.dumps(scene.get("metadata", {}), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    logger.info(f"Scene assets saved: {scene_dir}")
    return scene_dir


# ====================== Style Lock I/O ======================

def load_style_lock(style_dir: Path) -> StyleLock:
    """
    Load Style Lock from assets/style/ directory.

    Reads:
    - visual_style.md → visual_style_suffix
    - negative_prompt.txt → negative_prompt
    - color_palette.json → color_palette
    - render_rules.json → render_rules
    """
    visual_style = ""
    negative_prompt = ""
    color_palette = {}
    render_rules = {}

    visual_md = style_dir / "visual_style.md"
    if visual_md.exists():
        content = visual_md.read_text(encoding="utf-8")
        # Strip markdown headers and list markers, extract only style descriptors
        parts = []
        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Strip "- 风格：" / "- 渲染：" etc. — keep only the English descriptor
            if "：" in line:
                parts.append(line.split("：", 1)[1])
            elif ":" in line:
                parts.append(line.split(":", 1)[1])
            else:
                parts.append(line)
        visual_style = ", ".join(p.strip().lstrip("- ") for p in parts if p.strip())

    neg_txt = style_dir / "negative_prompt.txt"
    if neg_txt.exists():
        negative_prompt = neg_txt.read_text(encoding="utf-8").strip()

    color_json = style_dir / "color_palette.json"
    if color_json.exists():
        color_palette = json.loads(color_json.read_text(encoding="utf-8"))

    rules_json = style_dir / "render_rules.json"
    if rules_json.exists():
        render_rules = json.loads(rules_json.read_text(encoding="utf-8"))

    if not visual_style:
        logger.warning("No visual_style.md found, using default Style Lock")
        return DEFAULT_STYLE

    return StyleLock(
        visual_style_suffix=visual_style,
        negative_prompt=negative_prompt or DEFAULT_STYLE.negative_prompt,
        aspect_ratio="9:16 aspect ratio",
        color_palette=color_palette,
        render_rules=render_rules,
    )


def create_default_style_lock(style_dir: Path) -> StyleLock:
    """Create default Style Lock files in directory."""
    style_dir.mkdir(parents=True, exist_ok=True)

    style_dir.joinpath("visual_style.md").write_text(
        """# 视觉风格：黑暗奇幻国漫
- 风格：Chinese dark fantasy anime, cinematic composition
- 渲染：Semi-realistic, painterly texture, no cartoon flat shading
- 光影：High contrast, dramatic rim lighting, volumetric fog
- 色彩：Desaturated blues and warm amber accents
- 禁止：No chibi, no western comic style, no 3D CGI, no watercolor
""",
        encoding="utf-8",
    )

    style_dir.joinpath("negative_prompt.txt").write_text(
        "chibi, cartoon, 3D render, cgi, western comic style, "
        "flat color, watercolor, pastel, cute, kawaii, manga style, "
        "low quality, blurry, deformed face, extra fingers, poorly drawn hands",
        encoding="utf-8",
    )

    style_dir.joinpath("color_palette.json").write_text(
        json.dumps(DEFAULT_STYLE.color_palette, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    style_dir.joinpath("render_rules.json").write_text(
        json.dumps(DEFAULT_STYLE.render_rules, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    logger.info(f"Default Style Lock created: {style_dir}")
    return DEFAULT_STYLE


# ====================== Core: Visual Prompt Assembly ======================

def build_visual_prompt(
    shot: Shot,
    style_lock: StyleLock,
    character_assets: dict,
    scene_assets: Optional[dict] = None,
) -> tuple[str, str]:
    """
    Assemble (positive_prompt, negative_prompt) for a single Shot.

    Rules:
    1. Character prompt (main + secondary_characters)
    2. Scene + shot description
    3. Style Lock suffix forced to END (Transformer attention)
    4. Negative prompt returned separately (goes to API field)

    character_assets: {character_name: prompt_string}
    scene_assets: {scene_name: prompt_string}  (optional, uses shot.environment if missing)
    """
    # 1. Main character
    char_prompt = character_assets.get(shot.speaker, shot.speaker)

    # 1b. Secondary characters (multi-character shot face_ref routing)
    for sc_name in shot.secondary_characters:
        sc_prompt = character_assets.get(sc_name, sc_name)
        char_prompt += f", {sc_prompt}"

    # 2. Scene + shot description
    scene_shot = (
        f"{shot.environment}, {shot.lighting} lighting, "
        f"{shot.facial_expression}, {shot.character_action}, "
        f"{get_shot_suffix(shot.shot_type)}"
    )

    # 3. Positive: character + scene + Style Lock forced to END
    positive = (
        f"{char_prompt}, {scene_shot}, "
        f"{style_lock.visual_style_suffix}, {style_lock.aspect_ratio}"
    )

    # 4. Negative: API field only, never mixed in positive
    negative = style_lock.negative_prompt

    return positive, negative


def inject_visual_prompts(
    shots: list[Shot],
    style_lock: StyleLock,
    character_assets: dict,
    scene_assets: Optional[dict] = None,
) -> list[Shot]:
    """
    Batch-inject visual_prompt and negative_prompt into all Shots.

    Modifies shots in place, returns same list for chaining.
    """
    for shot in shots:
        positive, negative = build_visual_prompt(
            shot, style_lock, character_assets, scene_assets
        )
        shot.visual_prompt = positive
        shot.negative_prompt = negative

    logger.info(f"Visual prompts injected for {len(shots)} shots")
    return shots


# ====================== Asset Discovery ======================

def discover_characters(asset_dir: Path) -> list[str]:
    """List all character names that have prompt_template.txt in asset_dir."""
    if not asset_dir.exists():
        return []
    return [
        d.name
        for d in asset_dir.iterdir()
        if d.is_dir() and (d / "prompt_template.txt").exists()
    ]


def discover_scenes(asset_dir: Path) -> list[str]:
    """List all scene names that have prompt_template.txt in asset_dir."""
    if not asset_dir.exists():
        return []
    return [
        d.name
        for d in asset_dir.iterdir()
        if d.is_dir() and (d / "prompt_template.txt").exists()
    ]


def load_all_character_assets(character_dir: Path) -> dict:
    """Load all character prompt templates into {name: prompt} dict."""
    assets = {}
    for char_name in discover_characters(character_dir):
        assets[char_name] = get_character_prompt(char_name, character_dir)
    return assets


def load_all_scene_assets(scene_dir: Path) -> dict:
    """Load all scene prompt templates into {name: prompt} dict."""
    assets = {}
    for scene_name in discover_scenes(scene_dir):
        assets[scene_name] = get_scene_prompt(scene_name, scene_dir)
    return assets
