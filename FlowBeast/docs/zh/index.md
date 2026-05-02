# FlowBeast

**AI 驱动的短视频内容生成引擎**

> **FlowBeast** 是一个 AI 驱动的短视频内容生成引擎。核心流程是：**选题 → 病毒剧本 (JSON) → 音频 → 视频成品**。

---

## 快速链接

- 📚 [快速开始](getting-started.md)
- 🏗️ [架构](architecture.md)

## 功能

- 🎬 **Drama Generation**: AI驱动的短剧脚本生成
- 🧬 **FP3 Knowledge Base**: RAG赋能的病毒模式注入
- 🎙️ **Audio Generation**: TTS语音合成
- 🎥 **Video Pipeline**: 端到端视频生成

## 项目结构

```
FlowBeast/
├── flowbeast/          # 核心包
├── docs/              # MkDocs 文档
├── scripts/           # 工具脚本
└── tests/             # 测试套件
```

## 命令

```bash
# 安装依赖
uv sync

# 运行剧本生成流程
python main.py

# 运行 FastAPI 服务器
uvicorn flowbeast.api.main:app --reload --port 8000

# 初始化 FP3 向量知识库
python -m scripts.init_fp3

# 运行测试
uv run pytest tests/ -q
```

## 资源

- 📖 [文档](getting-started.md)
- 💬 [讨论](https://github.com/FlowBeast/FlowBeast/discussions)
- 🐛 [问题](https://github.com/FlowBeast/FlowBeast/issues)

---

**版本**: 0.3.2 (FP3 质量控制)
