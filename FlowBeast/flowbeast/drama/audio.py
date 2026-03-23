# drama/audio.py

import os
import asyncio
import edge_tts
from pathlib import Path
from elevenlabs.client import ElevenLabs

# --- 配置区 ---
# Edge-TTS 默认音色
EDGE_VOICE = "zh-CN-YunxiNeural" 
# ElevenLabs 默认音色 ID
ELEVEN_VOICE = "pNInz6obpgDQGcFmaJgB" 

# 初始化 ElevenLabs (仅当需要时使用)
def get_el_client():
    api_key = os.getenv("sk_c5dc1efcb036079d66aafc7062dfa2d4513e2c161c61454a")
    return ElevenLabs(api_key=api_key) if api_key else None

async def _edge_generate(text, file_path):
    communicate = edge_tts.Communicate(text, EDGE_VOICE)
    await communicate.save(file_path)

def _eleven_generate(text, file_path):
    client = get_el_client()
    if not client:
        raise ValueError("未检测到 ELEVENLABS_API_KEY")
    
    audio_stream = client.generate(
        text=text,
        voice=ELEVEN_VOICE,
        model="eleven_multilingual_v2"
    )
    with open(file_path, "wb") as f:
        for chunk in audio_stream:
            if chunk: f.write(chunk)

def generate_audio(text, scene_id, line_id, speaker, provider="edge"):
    """
    统一音频生成接口
    provider: "edge" (免费) 或 "elevenlabs" (付费)
    """
    print(f"🎙️ [{provider.upper()}] 正在配音 [S{scene_id}-L{line_id}] {speaker}...")
    
    output_dir = Path("flowbeast/data/outputs/audio")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"s{scene_id}_l{line_id}_{speaker}.mp3"

    if provider == "edge":
        asyncio.run(_edge_generate(text, file_path))
    elif provider == "elevenlabs":
        _eleven_generate(text, file_path)
    
    return str(file_path)
