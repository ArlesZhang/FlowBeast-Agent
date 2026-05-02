# 快速开始

欢迎使用 FlowBeast！本指南将帮助您快速上手。

## 前置要求

- Python 3.10+
- `uv` 包管理器
- 所选 LLM 供应商的 API 密钥

## 安装

```bash
git clone https://github.com/FlowBeast/FlowBeast.git
cd FlowBeast
uv sync
```

## 配置

在项目根目录创建 `.env` 文件：

```bash
ACTIVE_VENDOR=gemini
GOOGLE_API_KEY=your_google_api_key
FLOWBEAST_OUTPUT_DIR=./flowbeast/data/outputs
FLOWBEAST_VECTOR_DIR=./flowbeast/data/vectors
```

## 首次运行

```bash
python -m scripts.init_fp3
python main.py --topic "一个关于人工智能的短剧"
```

## 下一步

- 📖 阅读 [架构](architecture.md) 文档
- 🔧 查看 [技术债](tech-debt.md) 了解已知问题
- 📚 探索 [ADRs](adrs/index.md) 了解架构决策
