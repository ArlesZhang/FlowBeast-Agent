<div align="center">

# FlowBeast

**给一个话题，交付一集短剧。**

从话题到成片所需的全套素材 —— 剧本 · 分镜 · 配音 · `prompt_package.json`

[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/managed%20by-uv-DE5FE9)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-34%20passing-brightgreen)](#测试)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](#贡献)

[快速开始](#快速开始) · [你会得到什么](#你会得到什么) · [架构](#架构) · [核心概念](#核心概念) · [配置](#配置) · [HTTP API](#http-api)

</div>

---

## 这是什么

FlowBeast 是一套 **AI 短剧生产引擎**：把**已经爆过的内容结构**变成可检索、可复用的记忆，再重组到新话题上，产出一集短剧从剧本到渲染所需的全部素材。

```
传统做法    话题 ──► LLM ──► 一段文本                    结构随机 · 不可复用 · 无校验
FlowBeast   话题 ──► 爆款记忆检索 ──► 质量门禁 ──► 生产包   结构来自已验证的爆款
                     (FP3 ViralUnit)    (QualityGate)
```

`prompt_package.json` 是**交接点，不是终点** —— 渲染那一步交给 Seedance / 可灵 / HeyGen 这类现成工具，FlowBeast 负责把前面所有环节变成一个可交付的整体。

**它不是**：又一个「调 GPT 写文案」的壳，也不是视频生成模型、发布平台或多智能体框架。

---

## 核心特性

| | 特性 | 说明 |
|---|---|---|
| 🧬 | **爆款记忆（FP3）** | 把爆款拆成可组合的叙事原子（钩子 / 结构 / 情绪），FAISS 向量检索后注入生成提示词 —— 让输出携带**已验证有效的结构**，而不是随机创意 |
| 🎬 | **节拍驱动的分镜** | 镜头由**情绪节拍**（`beat_type`）驱动，而不是景别。每个镜头带运镜、时长、光照、负面提示词 |
| 🔒 | **画风锁定** | 全局 `style_lock` + 角色/场景资产注入，抑制跨镜头风格漂移 |
| ✅ | **质量门禁** | 9 维启发式评分 + 向量去重，拒绝结构崩坏的输出 |
| 🔊 | **配音即验证** | 逐句 TTS 后拼接整集音频 —— 用耳朵比用眼睛更快发现节奏和台词问题，不必先渲染视频 |
| 🔌 | **多厂商可插拔** | 8 家 LLM 厂商 + 4 家 embedding 厂商，切换只改 `.env` 一行 |
| 📦 | **一份包，三个入口** | CLI / HTTP API / 图形界面，产物完全一致 |

---

## 快速开始

### 前置要求

| 依赖 | 版本 | 用途 | 必需 |
|------|------|------|:---:|
| [Python](https://www.python.org/) | ≥ 3.12 | 运行时 | ✅ |
| [uv](https://docs.astral.sh/uv/) | 最新 | 包管理（本项目**不用 pip**） | ✅ |
| 任一 LLM API Key | — | DeepSeek / Qwen / OpenAI / Claude / Gemini … | ✅ |
| [Ollama](https://ollama.com/) | 最新 | 本地 embedding（`nomic-embed-text`） | ✅ † |
| Docker | — | 容器化运行 | ⬜ |

> † Embedding 默认走本地 Ollama —— **不花钱、不需要 Key**，因为主流 LLM 厂商大多不提供 embedding 接口。
> 若改用 OpenAI / Gemini / Qwen 的 embedding，可跳过 Ollama。

### 三步跑通

```bash
# 1. 克隆
git clone https://github.com/ArlesZhang/FlowBeast-Agent.git
cd FlowBeast-Agent

# 2. 配置（只需填一个 Key）
cp .env.example .env
#    编辑 .env → 设置 ACTIVE_VENDOR=deepseek 和 DEEPSEEK_API_KEY=sk-xxxxx

# 3. 一键启动（装依赖 → 拉 embedding 模型 → 建索引 → 起 API + UI）
./quickstart.sh
```

打开 **http://localhost:8501**，输入话题，点 **🚀 Generate**。

> `quickstart.sh` 会做启动前预检：缺 `uv`、缺 Key、Ollama 没跑、端口被占 —— 都会在启动前给出明确提示，而不是跑到一半崩掉。

### 或者，只跑一次 CLI

不需要起服务，不需要界面：

```bash
uv sync
uv run python main.py --topic "AI Agent 取代白领"
```

产物落在 `flowbeast/data/outputs/<时间戳>/`。

---

## 你会得到什么

每次运行产出 6 类文件，全部落在 `flowbeast/data/outputs/<时间戳>/`：

```
20261014_175540/
├── script.json              # 结构化剧本：场景 / 台词 / 情绪曲线 / 冲突升级
├── shot_list.json           # 逐镜头分镜表：景别 / 运镜 / 时长 / 光照 / SFX
├── prompt_package.json      # ⭐ 最终产物 —— 直接投喂 AI 视频工具
├── production_report.json   # 生产报告：质量分 / 耗时 / 失败项
├── episode_audio.mp3        # 拼接后的整集配音
└── audio/                   # 逐句 TTS 音频
    ├── s1_l0_HR.mp3
    └── s1_l1_林薇.mp3
```

`prompt_package.json` 的结构：

```jsonc
{
  "title": "...",
  "genre": "...",
  "core_hook": "...",
  "tags": ["..."],
  "emotion_curve_global": ["..."],
  "style_lock": { "...": "..." },   // 全局画风锁定，防止跨镜头漂移
  "shots": [
    {
      "shot_id": "S01_SH001",
      "beat_type": "tension",        // 情绪节拍 —— 驱动镜头，而非景别
      "shot_type": "close_up",
      "camera_motion": "slow_push_in",
      "duration_sec": 4,
      "motion_intensity": 3,         // close-up 强制限速，防五官崩坏
      "lighting": "harsh_fluorescent",
      "visual_prompt": "...",
      "negative_prompt": "..."
    }
  ]
}
```

> **为什么 `motion_intensity` 要限速？** 可灵 2.0 图生视频中，面部特写只要运动强度超过 4，五官就会像橡皮泥一样融化。
> [`shot_director.py`](flowbeast/drama/shot_director.py) 对 `close_up` 做了硬性 clamp —— 这条规则来自实际生成失败，不是拍脑袋。

---

## 使用方式

### 入口点一览

日常只需要记住前两个。

| # | 入口 | 命令 | 作用 | 端口 |
|---|------|------|------|:---:|
| 1 | **图形界面** | `uv run streamlit run flowbeast/demo/app.py` | 全流程可视化演示（需先启动 #2） | `8501` |
| 2 | **HTTP API** | `uvicorn flowbeast.api.main:app --reload --port 8000` | 异步任务 API | `8000` |
| 3 | **CLI 全流程** | `uv run python main.py --topic "话题"` | 不开服务，直接跑完 script → shots → audio | — |
| 4 | **反馈回流** | `uv run python -m flowbeast.fp3.feedback_ingest --report <报告> --views N --likes N` | 用真实播放数据调整原子权重 | — |
| 5 | **种子数据** | `uv run python -m flowbeast.fp3.seed_data` | 初始化 FP3 向量库（首次运行自动触发） | — |

### HTTP API

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/health` | 健康检查 |
| `POST` | `/api/v1/generate` | 提交生成任务，立即返回 `task_id` |
| `GET` | `/api/v1/tasks/{task_id}` | 轮询任务状态与进度 |
| `GET` | `/api/v1/download/{file_type}/{run_id}` | 下载产物（`prompt_package` · `script` · `report` · `episode_audio`） |

交互式文档：启动后访问 **http://localhost:8000/docs**。

```bash
# 不进界面，纯 API 跑一遍
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI Agent 取代白领"}'

curl http://localhost:8000/api/v1/tasks/<task_id>
```

---

## 架构

### 数据流

```
┌─ 记忆层 ───────────────────────────────────────────────────────┐
│  FP3 向量库 · 叙事原子（hook / pattern / emotion）· 质量门禁     │
└────────────────────────────┬───────────────────────────────────┘
                             ▼
┌─ 生成层 ───────────────────────────────────────────────────────┐
│  爆款结构注入 ──► 剧本生成 ──► Shot Director ──► TTS 配音       │
└────────────────────────────┬───────────────────────────────────┘
                             ▼
┌─ 交付层 ───────────────────────────────────────────────────────┐
│  prompt_package.json ──► 成片 ──► 播放数据 ──► 原子权重回流      │
└────────────────────────────────────────────────────────────────┘
```

### 代码模块

| 模块 | 职责 | 关键文件 |
|------|------|----------|
| [`flowbeast/fp3/`](flowbeast/fp3/) | **记忆层** —— 向量存储、检索、注入、反馈 | `store.py` · `retriever.py` · `injector.py` · `schema.py` |
| [`flowbeast/observe/quality/`](flowbeast/observe/quality/) | 质量门禁 —— 评分、去重、审计 | `scorer.py` · `gate.py` · `dedup.py` |
| [`flowbeast/drama/`](flowbeast/drama/) | 生产管线 —— 剧本、分镜、音频 | `pipeline.py` · `generator.py` · `shot_director.py` · `audio.py` |
| [`flowbeast/core/`](flowbeast/core/) | 配置 + 多厂商 LLM 适配 | `config.py` · `providers/` |
| [`flowbeast/api/`](flowbeast/api/) | FastAPI 服务 | `main.py` |
| [`flowbeast/demo/`](flowbeast/demo/) | Streamlit 界面 | `app.py` |

**分层原则：** 记忆层是核心资产；生产管线是**可替换的商品层** —— 任何一环出现更好的现成工具，直接换掉。

### 多厂商适配

[`flowbeast/core/providers/`](flowbeast/core/providers/) 用注册表模式统一了 8 家厂商：

```
openai_compatible.py     →  deepseek · qwen · openai · glm · openrouter · ollama
anthropic_compatible.py  →  anthropic（含 Token Plan 代理网关）
gemini_provider.py       →  gemini
embedding.py             →  ollama · openai · gemini · qwen
```

---

## 核心概念

### FP3 —— 可组合的叙事原子

FP3 存储**可组合的叙事原子**。`ViralUnit` 只有三个字段，刻意保持最小：

| 字段 | 含义 | 性质 |
|------|------|------|
| `hook` | 开场钩子（前 3 秒） | **可插拔** —— 独立替换 |
| `pattern` | 冲突 / 结构模式 | **可迁移** —— 跨语义域通用 |
| `emotion` | 情绪序列 | **可重映射** —— 同形状不同情绪 |

检索到的原子被注入生成提示词，让输出携带已验证有效的结构。

### Latent Grammar —— 隐式语法

FP3 本质是一套内容生成的隐式语法：

- **原子 = 词汇**（钩子类型、冲突模式、情绪曲线、视觉风格、镜头语言）
- **合法组合 = 语法**（哪些 hook × 哪些 conflict × 哪些 emotion × 哪些 shot = 爆款）
- **QualityGate = 类型检查**（拒绝违反隐式语法的组合）

### QualityGate —— 9 维评分

[`flowbeast/observe/quality/config.py`](flowbeast/observe/quality/config.py) 中定义，所有权重可用 `QUALITY_` 前缀的环境变量覆盖：

| 维度 | 权重 | | 维度 | 权重 |
|------|:---:|---|------|:---:|
| `hook_strength` | 0.20 | | `pacing` | 0.08 |
| `emotional_intensity` | 0.15 | | `engagement_density` | 0.08 |
| `retention_potential` | 0.15 | | `conflict_density` | 0.08 |
| `novelty` | 0.10 | | `replay_potential` | 0.06 |
| `virality_signals` | 0.10 | | | |

**阈值：** `≥ 0.60` 接受 · `≥ 0.40` 转人工复核 · `< 0.40` 拒绝。另有 `0.98` 相似度的向量去重。

> **已知局限（请勿当作结论）**：这些权重是拍的，不是标定的。9 个维度中有 4 个（合计 0.45 权重）只读 `unit.hook` 一个字段，且互相高度相关。
> 目前它**从未给出过 ACCEPT**。把它当**弱信号**用，别当裁判。

### Audio Validation —— 用耳朵做质量验证

TTS 配音是**质量验证层**，不是最终产物。听觉比视觉更快暴露节奏和台词问题 ——
不用等渲染视频，就能判断这一集剧本是否成立。

---

## 配置

所有配置集中在 `.env`（从 [`.env.example`](.env.example) 复制）。核心项：

```bash
# ---- LLM ----
ACTIVE_VENDOR=deepseek          # deepseek | qwen | openai | anthropic | gemini | glm | openrouter | ollama
ACTIVE_MODEL=deepseek-chat      # 留空则用厂商默认模型
DEEPSEEK_API_KEY=sk-xxxxxxxx    # 只填你选的那家

# ---- Embedding ----
EMBED_VENDOR=ollama             # ollama | openai | gemini | qwen
OLLAMA_BASE_URL=http://localhost:11434   # 裸机用 localhost；Docker 用 host.docker.internal
```

### ⚠️ 三个必知的配置陷阱

1. **改完 `.env` 必须重启后端。** `config.py` 在 **import 时**加载配置 —— 运行中的 uvicorn 进程不会感知你的修改，
   表现为「Key 明明填了却报未配置」。

2. **`.env` 里的空值会覆盖 shell 环境变量。** `config.py` 使用 `load_dotenv(override=True)`，
   所以 `OPENAI_API_KEY=`（空）会抹掉你 `~/.bashrc` 里已 export 的同名变量。
   **用不到的厂商，请整行注释掉，而不是留空。**

3. **`EMBED_MODEL=` 留空会覆盖代码默认值**，把 `nomic-embed-text` 抹成空字符串。
   只在需要覆盖时才显式写模型名。

### 两个厂商相关的坑

- **`qwen` 这个 vendor 实际读的是 `DASHSCOPE_API_KEY`**，不是 `QWEN_API_KEY`（尽管 `.env.example` 两个都列了）。
- **DeepSeek 不提供 embedding 接口**，把 `EMBED_VENDOR` 设成 `deepseek` 会直接抛 `Unsupported embedding provider`。

---

## 部署

### Docker

```bash
docker-compose up --build
```

> ⚠️ **当前镜像未安装 ffmpeg 和字体**，容器内音频拼接会失败。本地裸机运行不受影响。

### 其他

| 文件 | 用途 |
|------|------|
| [`quickstart.sh`](quickstart.sh) | 本地一键启动（预检 + 建索引 + 起服务） |
| [`start_dev.sh`](start_dev.sh) | 云平台启动（读 `$PORT`，适配 Railway） |
| [`start.sh`](start.sh) | 容器内启动包装 |
| [`railpack.json`](railpack.json) | Railway 构建配置 |

---

## 故障排查

| 症状 | 原因 | 解决 |
|------|------|------|
| `API key not configured for vendor 'xxx'` | `.env` 缺失，或改完没重启服务 | 检查 `.env`；重启 uvicorn |
| 界面显示 `❌ API server not running` | FastAPI 没起，或端口不是 8000 | 先启动入口点 #2 |
| 调 Ollama 时 `404 page not found` | `OLLAMA_BASE_URL` 少了 `/v1` 后缀 | 用 `http://localhost:11434/v1` |
| 音频全部失败 / HTTP 403 | `edge-tts` 版本过旧，被微软网关拒绝 | `uv add "edge-tts>=7.3.1"`（**勿降级**） |
| `Unsupported embedding provider` | `EMBED_VENDOR` 设成了不提供 embedding 的厂商 | 改回 `ollama` |
| 换话题后结果高度雷同 | FP3 目前只有种子数据 | 见 [Roadmap](#roadmap) |
| 端口被占用 | 上次进程没退干净 | `fuser -k 8501/tcp` |

---

## 项目结构

```
FlowBeast-p1/
├── main.py                    # CLI 全流程入口
├── quickstart.sh              # 一键启动（预检 + 建索引 + 起服务）
├── pyproject.toml             # 依赖声明（uv 管理）
├── Dockerfile                 # 两阶段构建：development / production
├── docker-compose.yml
│
├── flowbeast/
│   ├── fp3/                   # ⭐ 记忆层：向量存储 / 检索 / 注入 / 反馈
│   ├── observe/quality/       # 质量门禁：评分 / 去重 / 审计
│   ├── drama/                 # 生产管线：剧本 / 分镜 / 音频
│   ├── core/                  # 配置 + 多厂商 LLM 适配
│   ├── api/                   # FastAPI 服务
│   ├── demo/                  # Streamlit 界面
│   └── data/                  # 运行产物（输出 / 向量库）
│
├── assets/style/              # 视觉风格资产：调色板 / 渲染规则 / 负面提示词
└── tests/                     # 34 个 pytest 用例
```

---

## 测试

```bash
uv run pytest tests/ -q                      # 全部（34 个用例）
uv run pytest tests/test_fp3_quality.py -q   # 只跑质量门禁
uv run pytest -k "fp3" -v                    # 按关键字筛选
```

用例只覆盖**能抓到真实回归**的路径：LLM 输出解析（JSON 提取 + 结构校验）、
提示词组装分支、FP3 反馈提取、质量门禁评分与审计落盘。

> 不为常量形状、源码文本、环境路径写测试 —— 那类断言抓不到 bug，只增加维护成本。

---

## Roadmap

**主线：从「生产包」走到「成片」。**

- [x] 端到端管线跑通：话题 → 剧本 → 分镜 → 配音 → 生产包
- [x] 多厂商 LLM 适配（8 家）+ 本地 embedding
- [x] FastAPI 异步任务服务 + Streamlit 界面
- [x] 质量门禁：9 维评分 + 向量去重 + 审计
- [ ] **渲染适配层** —— 把 `prompt_package.json` 接到现成视频生成 API，产出可交付的成片
- [ ] **扩充 FP3 真实爆款语料** —— 当前仅种子数据，是输出多样性的主要瓶颈
- [ ] **标定 QualityGate 权重** —— 现有权重未经数据拟合
- [ ] Docker 镜像补齐 ffmpeg 与字体

---

## 贡献

欢迎 Issue 和 PR。开始之前：

1. 阅读 [`CLAUDE.md`](CLAUDE.md)（项目约定）与 [`.cursor/rules/`](.cursor/rules/)（开发规范）
2. **先搜再写** —— 这个项目需要的绝大多数能力，市场上已有成熟方案。优先集成，而非自研
3. 提交前跑一遍 `uv run pytest tests/ -q`

---

## 许可

[Apache License 2.0](LICENSE)

<div align="center">
<sub>FlowBeast · 把爆款拆成原子，再编译成新的爆款</sub>
</div>
