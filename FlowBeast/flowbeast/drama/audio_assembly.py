# flowbeast/drama/audio_assembly.py

"""
Audio Assembly: concatenates individual dialogue MP3s into one continuous episode file.

Uses ffmpeg directly (no pydub dependency).
"""

import subprocess
import tempfile
from pathlib import Path

from loguru import logger


DEFAULT_PAUSE_SEC = 0.5


def assemble_episode_audio(
    audio_dir: Path,
    script: dict,
    output_path: Path = None,
    pause_sec: float = DEFAULT_PAUSE_SEC,
) -> str:
    """
    Concatenate all dialogue MP3s from a single episode into one continuous file.

    Order: scenes in script order, dialogues within each scene in line order.
    Inserts pause_sec silence between each dialogue line.

    Returns path to assembled file.
    """
    audio_files = []
    for scene in script.get("scenes", []):
        scene_id = scene.get("id", 0)
        for line_id, line in enumerate(scene.get("dialogue", [])):
            safe_speaker = "".join(c for c in line["speaker"] if c.isalnum() or c in "_- ")
            mp3_path = audio_dir / f"s{scene_id}_l{line_id}_{safe_speaker}.mp3"
            if mp3_path.exists():
                audio_files.append(mp3_path)
            else:
                logger.warning(f"Missing audio file: {mp3_path}")

    if not audio_files:
        raise ValueError(f"No audio files found in {audio_dir}")

    if output_path is None:
        output_path = audio_dir.parent / "episode_audio.mp3"

    if len(audio_files) == 1:
        import shutil
        shutil.copy2(audio_files[0], output_path)
        logger.info(f"Single audio file, copied to {output_path}")
        return str(output_path)

    # Build a concat list file with silence segments interspersed
    concat_file = output_path.with_suffix(".concat_list.txt")
    with open(concat_file, "w") as f:
        for i, audio_file in enumerate(audio_files):
            f.write(f"file '{audio_file.resolve()}'\n")
            # Insert silence between lines (not after the last)
            if i < len(audio_files) - 1:
                silence_mp3 = _generate_silence(pause_sec, output_path.parent / f"_silence_{i}.mp3")
                f.write(f"file '{silence_mp3.resolve()}'\n")

    # Concatenate via ffmpeg concat demuxer
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:a", "libmp3lame", "-b:a", "128k",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg concat failed: {result.stderr[:500]}")

    # Cleanup concat file and silence files
    concat_file.unlink(missing_ok=True)
    for sil in output_path.parent.glob("_silence_*.mp3"):
        sil.unlink(missing_ok=True)

    logger.success(
        f"Episode audio assembled: {output_path.name} "
        f"({len(audio_files)} lines, {pause_sec}s pauses)"
    )
    return str(output_path)


def _generate_silence(duration_sec: float, output_path: Path) -> Path:
    """Generate a silent MP3 file of given duration."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100:d={duration_sec}",
        "-c:a", "libmp3lame", "-b:a", "128k",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg silence generation failed: {result.stderr[:300]}")
    return output_path
