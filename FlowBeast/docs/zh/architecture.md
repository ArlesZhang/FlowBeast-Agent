# 架构

FlowBeast 由两个核心引擎协同工作：

## IP2 — 剧本生成层 (`flowbeast/drama/`)

通过 LLM 调用生成病毒式短视频剧本。

## FP3 — 病毒基因知识库 (`flowbeast/fp3/`)

RAG 层，通过检索到的病毒模式来增强 prompt。

## LLM 路由 (`flowbeast/core/config.py`)

| 供应商 | 模型 | API Key |
|--------|------|---------|
| Gemini | gemini-1.5-flash | `GOOGLE_API_KEY` |
| Qwen | qwen-plus | `DASHSCOPE_API_KEY` |
| OpenAI | gpt-4o | `OPENAI_API_KEY` |

## 关键数据结构

```python
# drama/schema.py
Script: title, genre, core_hook, scenes: List[Scene]
Scene: id, hook, conflict, emotion_curve, dialogue: List[Dialogue]

# fp3/schema.py
ViralUnit: hook: str, pattern: str, emotion: List[str]
```
