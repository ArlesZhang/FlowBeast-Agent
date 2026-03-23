def build_prompt(topic: str) -> str:
    return f"""
你是一位短视频爽剧导演，精通心理博弈和极致反转。
请根据主题【{topic}】创作一个 60 秒（约 5-6 镜）的爆款剧本。

### 核心约束：
1. 黄金3秒：第一镜必须是极端的身份冲突或言语羞辱。
2. 极致反转：第三或第四镜必须揭露隐藏身份或反向打脸。
3. 视觉一致性：必须为每个角色提供稳定的外貌描述。

### 严格 JSON 格式输出：
{{
  "title": "{topic}",
  "characters": [
    {{
      "name": "主角名字",
      "visual_desc": "详细的英文外貌描述，用于 AI 绘图，如：A sharp-dressed young billionaire, short black hair, cold eyes, wearing a grey Armani suit",
      "voice_tag": "zh-CN-YunxiNeural"
    }}
  ],
  "scenes": [
    {{
      "id": 1,
      "hook": "本镜冲突点",
      "shot_type": "Close-up / Wide shot / High-angle",
      "visual_prompt": "给绘图模型的英文提示词，必须包含角色名和动作场景描述",
      "emotion_weight": 0.9,
      "dialogue": [
        {{"speaker": "角色名", "text": "台词（简短有力）"}}
      ]
    }}
  ]
}}

不要任何开头和结尾的废话，只输出 JSON。
"""
