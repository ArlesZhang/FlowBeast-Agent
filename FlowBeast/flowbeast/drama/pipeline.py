import json
import os
from datetime import datetime
from flowbeast.drama.generator import generate_script
from flowbeast.drama.audio import generate_audio

# --- 全局配置：在这里一键切换配音引擎 ---
# "edge" 为免费微软音色，"elevenlabs" 为高质付费音色
AUDIO_PROVIDER = "edge" 

def run_full_pipeline(topic: str):
    print(f"\n🚀 === FlowBeast 启动：【{topic}】 ===")

    # 1. 大脑生成：从 LLM 获取结构化剧本
    try:
        script = generate_script(topic)
    except Exception as e:
        print(f"❌ 剧本生成失败: {e}")
        return

    # 2. 剧本持久化：存入 data/outputs 以备后续人工查阅或剪辑参考
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 确保输出目录存在
    os.makedirs("flowbeast/data/outputs", exist_ok=True)
    
    script_filename = f"flowbeast/data/outputs/script_{timestamp}.json"
    with open(script_filename, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)
    print(f"✅ 剧本已存: {script_filename}")

    # 3. 产能闭环：自动化批量配音
    print(f"🎬 正在使用 [{AUDIO_PROVIDER.upper()}] 引擎进行配音任务...")
    
    for scene in script.get("scenes", []):
        scene_id = scene.get("id", 0)
        for line_id, line in enumerate(scene.get("dialogue", [])):
            try:
                # 注意：这里的参数名必须与你的 audio.py 定义严格对应
                path = generate_audio(
                    text=line["text"],
                    scene_id=scene_id,
                    line_id=line_id,
                    speaker=line["speaker"],
                    provider=AUDIO_PROVIDER
                )
                print(f"   -> 已生成: {os.path.basename(path)}")
            except Exception as e:
                print(f"   ❌ [S{scene_id}-L{line_id}] 配音失败: {e}")

    print(f"✨ 闭环完成！主题【{topic}】所有资产已就绪。")

if __name__ == "__main__":
    # 批量测试：收集“直觉数据”，验证爽感逻辑
    test_topics = [
        "逆袭：被开除后的百亿首富",
        "校园：穷小子获得神豪系统",
        "战神：归来发现女儿住狗窝"
    ]

    for topic in test_topics:
        run_full_pipeline(topic)
