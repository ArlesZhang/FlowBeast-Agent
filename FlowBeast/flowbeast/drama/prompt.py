"""
Drama Prompt: LLM prompt template for hook-driven short-drama storytelling.

Role: Provides the structured prompt template that guides the LLM to generate
viral drama scripts. Includes narrative structure rotation, emotion curve
requirements, and output JSON schema enforcement.

The base prompt is enriched by injector.py with FP3 RAG examples before
being sent to the LLM.
"""

import random
from typing import Optional


# ====================== 叙事结构轮换池 ======================
NARRATIVE_STRUCTURES = [
    {
        "name": "classic_reversal",
        "pattern": "压制 → 身份揭露 → 反杀 → 爽",
        "description": "经典逆袭反转，但每个转折点必须有观众想不到的细节",
    },
    {
        "name": "mystery_reveal",
        "pattern": "谜团 → 线索 → 假真相 → 真反转",
        "description": "以悬念驱动，观众以为猜到了，但真相是另一个方向",
    },
    {
        "name": "double_identity",
        "pattern": "平凡表象 → 危机触发 → 能力泄露 → 层层揭露",
        "description": "主角隐藏身份，在危机中不断泄露能力，每一层都比上一层更惊人",
    },
    {
        "name": "deal_with_devil",
        "pattern": "绝境 → 禁忌契约 → 能力觉醒 → 代价浮现",
        "description": "主角获得力量但必须付出代价，代价的揭示是最高潮",
    },
    {
        "name": "inherited_secret",
        "pattern": "普通人生 → 遗产/秘密发现 → 追杀 → 真相大白",
        "description": "一个意外的发现改变了主角的命运，真相比想象中更大",
    },
    {
        "name": "parallel_perspective",
        "pattern": "同一事件 → 角色A视角 → 角色B视角 → 真相颠覆",
        "description": "从不同角色的视角看同一个事件，最后的视角颠覆前面的所有认知",
    },
]


def build_prompt(
    topic: str,
    trend_context: Optional[str] = None,
    narrative_style: Optional[str] = None,
    fp3_injected: str = "",
) -> str:
    # 随机选叙事结构（除非指定）
    if narrative_style is None:
        chosen = random.choice(NARRATIVE_STRUCTURES)
    else:
        chosen = next(
            (s for s in NARRATIVE_STRUCTURES if s["name"] == narrative_style),
            random.choice(NARRATIVE_STRUCTURES),
        )

    prompt = f"""
你是一个"短视频爆款生成系统"，而不是普通编剧。

你的任务不是写故事，而是：
👉 生成一个【可用于流量生产系统】的结构化爽剧数据

主题：
【{topic}】

==============================
🎭 本次叙事结构（随机选择）
==============================

结构名称：{chosen['name']}
模式：{chosen['pattern']}
描述：{chosen['description']}

你必须以这个结构为核心来组织故事，但允许自由发挥其中的细节和转折。

==============================
🎯 爆款生成规则（必须严格遵守）
==============================

【1】黄金3秒（Hook）
- 第一幕必须是：羞辱 / 背叛 / 极端冲突
- 必须让用户"停下来"

【2】冲突驱动（Conflict）
- 每一幕都必须有冲突升级
- 常见类型：羞辱 / 打脸 / 逆袭 / 权力反转 / 金钱碾压

【3】情绪曲线（Emotion Curve）
- 必须设计完整情绪路径，例如：
  压抑 → 屈辱 → 震惊 → 爆发 → 爽

【4】强反转（Twist）
- 第3或4幕必须出现身份揭露/反杀/权力翻转

【5】节奏（Pacing）
- 全剧控制在5-6个场景，节奏快

==============================
🚫 反套路指令（必须遵守）
==============================

1. 禁止使用"开除→跪求→逆袭"的标准逆袭蓝本
2. 至少一处情节必须是"观众意想不到的走向"
3. 禁止"所有人都在嘲笑主角"的套路化铺垫
4. 反派必须有合理动机，禁止脸谱化
5. 结局必须有情感余韵，禁止简单的大团圆

==============================
🧬 空想家创作核心（嫁接 / 篡改 / 愚弄 / 寄生 / 偷盗）
==============================

本系统的哲学根基是"凡空想的，必具现"。你必须在以下技法中选择至少一种使用：

【嫁接】将两个看似无关的设定嫁接在一起：
  例：修仙+AI伦理 → 灵气是某种高维代码
  例：霸道总裁+时间循环 → 每次循环死在不同人手里

【篡改】篡改一个经典设定的核心要素：
  例：战神归来 → 但主角发现才是当年阴谋的策划者
  例：重生复仇 → 但仇人重生得更早

【寄生】寄生在真实热点上，用熟悉的语境制造新鲜感：
  让故事的 hook 跟真实社会话题发生关联

【愚弄】在观众以为自己猜对时夺走他们的确信：
  群众以为他是穷小子 → 其实他是富二代 → 其实身份是借的 → 其实...

【偷盗】偷一个经典故事的骨架，套上完全不同的外壳：
  例：基督山伯爵的骨架 + 现代娱乐圈外壳

请明确标注你使用了哪种技法，以及如何使用。

==============================
📊 数据结构要求
==============================

必须包含：hook, conflict, emotion_curve, tags, summary

==============================
🎬 视觉生成要求
==============================

- 每个角色必须有 stable visual_desc（英文）
- 每个 scene 必须包含 visual_prompt（英文，用于MJ/SD）和 shot_type

==============================
📦 严格 JSON 输出格式
==============================

{{
  "title": "{topic}",
  "genre": "类型（如：逆袭 / 战神 / 校园 / AI讽刺）",
  "target_audience": "受众（如下沉市场 / 女性向）",
  "core_hook": "整个故事最强钩子（标题党）",
  "tags": ["标签1", "标签2"],
  "emotion_curve_global": ["情绪1", "情绪2"],
  "characters": [
    {{
      "name": "角色名",
      "visual_desc": "英文外貌描述",
      "voice_tag": "语音ID"
    }}
  ],
  "scenes": [
    {{
      "id": 1,
      "hook": "本幕钩子",
      "conflict": "冲突类型",
      "summary": "一句话描述",
      "emotion_curve": ["情绪变化"],
      "shot_type": "Close-up / Wide shot / High-angle",
      "visual_prompt": "英文提示词（角色+动作+环境）",
      "pace": "fast / medium / slow",
      "climax": true,
      "dialogue": [
        {{
          "speaker": "角色名",
          "text": "短促有力台词",
          "emotion": "情绪",
          "intensity": 9
        }}
      ]
    }}
  ]
}}

==============================
❗ 绝对禁止
==============================

- 不要解释
- 不要Markdown
- 不要多余文本
- 只输出 JSON
"""

    # --- 实时热点注入 ---
    if trend_context:
        prompt += f"""

==============================
🔥 实时热点基础素材（用于嫁接/篡改/寄生创作）
==============================

以下是当前真实的热搜话题，你必须以此为创意基础，将故事的 hook 或冲突与这些话题发生关联：

{trend_context}

利用这些真实话题进行"嫁接"或"寄生"创作，让作品有现实锚点和观众共鸣。
"""

    # --- FP3 爆款基因注入 ---
    if fp3_injected:
        prompt += f"""

==============================
📚 爆款基因参考（FP3 RAG 增强）
==============================

以下是从爆款知识库中检索到的成功模式，参考它们的情绪张力和结构设计：

{fp3_injected}
"""

    return prompt
