# flowbeast/drama/audio.py

import asyncio
from pathlib import Path
from typing import Optional

import edge_tts
from loguru import logger
from elevenlabs.client import ElevenLabs

from flowbeast.core.config import settings


# ====================== 默认配置 ======================
EDGE_VOICE = "zh-CN-YunxiNeural"
ELEVEN_VOICE = "pNInz6obpgDQGcFmaJgB"

EDGE_TTS_MAX_RETRIES = 2
EDGE_TTS_BACKOFF = 1  # seconds, exponential base


# ====================== ElevenLabs ======================
def get_eleven_client():
    api_key = getattr(settings, "ELEVENLABS_API_KEY", "")
    if not api_key:
        return None
    return ElevenLabs(api_key=api_key)


# ====================== 情绪控制（核心升级）======================
def build_voice_params(emotion: Optional[str], intensity: Optional[int]):
    """
    将情绪映射为语音参数
    """
    rate = "+0%"
    pitch = "+0Hz"
    volume = "+0%"

    if not emotion:
        return rate, pitch, volume

    intensity = intensity or 5

    if emotion in ["愤怒", "爆发"]:
        rate = f"+{intensity * 5}%"
        pitch = f"+{intensity * 5}Hz"

    elif emotion in ["悲伤", "压抑"]:
        rate = f"-{intensity * 3}%"
        pitch = f"-{intensity * 5}Hz"

    elif emotion in ["震惊"]:
        rate = f"+{intensity * 3}%"
        pitch = f"+{intensity * 8}Hz"

    return rate, pitch, volume


# ====================== Edge TTS ======================
async def _edge_generate(text, file_path, emotion=None, intensity=None):
    rate, pitch, volume = build_voice_params(emotion, intensity)

    communicate = edge_tts.Communicate(
        text=text,
        voice=EDGE_VOICE,
        rate=rate,
        pitch=pitch,
        volume=volume
    )

    await communicate.save(str(file_path))


async def _edge_generate_with_retry(text, file_path, emotion=None, intensity=None, max_retries=EDGE_TTS_MAX_RETRIES):
    """Edge TTS wrapper with retry + exponential backoff（处理国内网络不稳定）。"""
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            await _edge_generate(text, file_path, emotion=emotion, intensity=intensity)
            return
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                delay = EDGE_TTS_BACKOFF ** attempt
                logger.warning(f"⚠️ Edge TTS 失败 (第 {attempt}/{max_retries} 次)，{delay}s 后重试: {e}")
                await asyncio.sleep(delay)
    raise last_error


# ====================== ElevenLabs ======================
def _eleven_generate(text, file_path):
    client = get_eleven_client()
    if not client:
        raise ValueError("❌ 未配置 ELEVENLABS_API_KEY")

    audio_stream = client.generate(
        text=text,
        voice=ELEVEN_VOICE,
        model="eleven_multilingual_v2"
    )

    with open(file_path, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)


# ====================== 主接口 ======================
def generate_audio(
    text: str,
    scene_id: int,
    speaker: str,
    provider: str = "edge",
    output_dir: str = None,
    line_id: int = 0,
    emotion: Optional[str] = None,
    intensity: Optional[int] = None,
):
    """
    FlowBeast 音频生成统一入口（Audio Engine）

    支持：
    - 多 provider（edge / elevenlabs）
    - 情绪语音控制
    - 自定义输出目录
    """

    logger.info(f"🎙️ [{provider.upper()}] S{scene_id}-L{line_id} | {speaker}")

    # ====================== 输出路径 ======================
    if output_dir:
        base_path = Path(output_dir)
    else:
        base_path = Path(settings.FLOWBEAST_OUTPUT_DIR) / "audio"

    base_path.mkdir(parents=True, exist_ok=True)

    safe_speaker = "".join(c for c in speaker if c.isalnum() or c in "_- ")
    file_path = base_path / f"s{scene_id}_l{line_id}_{safe_speaker}.mp3"

    # ====================== 执行生成 ======================
    try:
        if provider == "edge":
            asyncio.run(
                asyncio.wait_for(
                    _edge_generate_with_retry(
                        text,
                        file_path,
                        emotion=emotion,
                        intensity=intensity,
                    ),
                    timeout=30,
                )
            )

        elif provider == "elevenlabs":
            _eleven_generate(text, file_path)

        else:
            raise ValueError(f"❌ 不支持的 provider: {provider}")

        logger.success(f"✅ 音频生成完成: {file_path.name}")

    except asyncio.TimeoutError:
        logger.warning(f"⚠️ S{scene_id}-L{line_id} 超时，跳过")
        raise TimeoutError(f"Audio generation timeout for S{scene_id}-L{line_id}")
    except Exception as e:
        logger.error(f"❌ 音频生成失败: {e}")
        raise

    return str(file_path)
