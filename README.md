<div align="center">

# 🌊 FlowBeast

**给小团队的 AI 短剧交付系统 —— 一个话题进去，一集成片（剧本 + 分镜 + 配音 + 提示词包）出来。**

`topic → FP3 爆款记忆检索 → 剧本 → 分镜 → 配音 → prompt_package.json`

[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/managed%20by-uv-DE5FE9)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-34%20passing-brightgreen)](#测试)

</div>

---

## ⚠️ 先读这一段

> 市场反馈表明，静态语料壁垒、低价抽取服务、特定品牌命名以及提示词包等四条早期创业路径已被证伪。
> AI 2.0 时代轻资产模式已难以为继，从业者需要转向更深层的系统级工作流集成与业务结果交付。

**FlowBeast 不卖编译器，也不卖提示词包。** 它的产品形态是 **「陪跑式」AI 短剧制作服务** —— 面向中国小型短剧团队，
**按交付成片集数收费**，是服务而不是 SaaS。免费的公开评分器是获客入口，不是产品本身。

**唯一验收标准：有真实付费证据。**
在客户为一集成片付过钱之前，任何功能、重构、文档都不算数。

**优化目标：可用 · 能落地 · 可集成 · 可交付 · 能赚钱。**
不追求完整，不追求优雅，不追求架构纯洁。**能跑通的集成，胜过更聪明的自研。**

完整论证与 30 天计划见 [`.ai/current/commercialization_playbook.zh.md`](.ai/current/commercialization_playbook.zh.md)。

---

## 规则 0 —— 绝不重复造轮子

**默认假设：这件事市场上已经有人做过，而且做得比我们好。**

框架、包、模块、开源项目、Claude Skills、MCP、插件、SaaS API —— 这个项目需要的东西，
绝大多数已经存在，由别人维护，比我们一天写出来的更成熟。

稀缺资源**不是代码**，而是**集成 + 调度 + 商业交付**。自己重写一个已有的轮子，
花掉的正是唯一拿不回来的资源。

### 默认顺序

1. **先搜**（GitHub / PyPI / MCP registry / Skills 生态），并说明找到了什么
2. **集成** —— 当作依赖直接用（最好结果：我们自己零行代码）
3. **借鉴** —— 移植成熟的设计或算法，注明出处并核对 License
4. **自研** —— 只有在 1–3 确实失败后，并且必须说明**为什么失败**

### 硬性约束

- **库里有的，绝不手写。** 不手搓分词、重试逻辑、TTS 对齐、字幕排版、鉴权、队列、调度、向量检索。
- **优先选平庸、流行、有人维护的方案**，哪怕自己调的版本略好一点 —— 维护成本活得比调优收益久。
- **采用前核对 License。** MIT / Apache-2.0 / BSD 可用；商用链路里的 GPL/AGPL 必须先上报。
- **复制进仓库的代码会腐烂。** 优先真依赖，而不是把文件拷进 repo。
- **工具差一点点时，扩展它**（插件 / 配置 / 包装 / 提 PR），而不是fork 出一套自己的平行实现。

### 落地检查

- 加依赖前先 `uv pip list` 看是否已装
- 写脚本前先看机器上是不是已有 CLI 能干这件事
- 造 sub-agent 前先看现有 Claude Skill / MCP server 是否覆盖
- 设计子系统前先看 [`capability_map.md`](.ai/current/capability_map.md)（已把能力对上现成工具）
- **把集成选择说出来**（"用 X，因为 Y；不写 Z，因为 X 已覆盖"），让决策可被 review

### 我们只自研什么

只有真正的业务本身：把工具串成一份可交付物的**工作流胶水**，以及通用工具不可能知道的**领域逻辑**
（短剧结构、中文短剧节奏、按集交付的打包方式）。底下的基础设施、管线、格式、协议 —— 都是别人的活，且已经干完了。

---

## 这是什么

FlowBeast 把**已经爆过的内容结构**变成可复用、可检索的记忆，再重组到新话题上。

你给它一个话题（比如「AI Agent 取代白领」），它产出：

- **结构化剧本** —— 场景 / 台词 / 情绪曲线 / 冲突升级
- **逐镜头分镜表** —— 景别 / 运镜 / 时长 / 光照 / 负面提示词
- **整集配音** —— Edge TTS 逐句生成后拼接
- **`prompt_package.json`** —— 可直接投喂 Seedance / 可灵 / HeyGen 的最终产物

```
传统做法:  话题 ──► LLM ──► 一段文本              (结构随机，不可复用，无质量校验)
FlowBeast: 话题 ──► FP3 爆款记忆检索 ──► 质量门禁 ──► prompt_package.json
                    (ViralUnit 原子)     (QualityGate)
```

**它不是**：又一个「调 GPT 写文案」的壳，也不是视频生成器、发布平台或多智能体框架。
我们停在 `prompt_package.json` 和交付的成片。

---

## 为什么需要它

大模型会越来越强，视频工具会越来越便宜。**但「什么样的内容结构容易爆」这件事，不会随模型升级自动出现。**

FlowBeast 押注的不是生产管线（script → audio → video，那是可替换的商品层），而是：

> **爆款内容的可组合结构 —— 一套「隐式语法」（Latent Grammar）**

它编译的不是代码，而是：**情绪 · 冲突 · 镜头 · 节奏 · 爽点 · 人设 · 视觉风格 · 音频情绪**。

---

## 快速开始

### 前置要求

| 依赖 | 版本 | 用途 | 是否必需 |
|------|------|------|----------|
| **Python** | ≥ 3.12 | 运行时 | ✅ 必需 |
| **[uv](https://docs.astral.sh/uv/)** | 最新 | 包管理（本项目不用 pip） | ✅ 必需 |
| **LLM API Key** | — | DeepSeek / OpenAI / Qwen 任选其一 | ✅ 必需 |
| **[Ollama](https://ollama.com/)** | 最新 | 本地 embedding（`nomic-embed-text`） | ✅ 必需¹ |
| Docker | — | 容器化运行 | ⬜ 可选 |

> ¹ Embedding 走本地 Ollama，**不需要 API Key、不产生费用**。这是因为 DeepSeek 等主流厂商不提供 embedding 接口。若你改用 OpenAI / Gemini 的 embedding，可跳过 Ollama。

### 三步跑通

```bash
# 1. 克隆
git clone <repo-url>
cd FlowBeast-p1

# 2. 配置（只需填一个 API Key）
cp .env.example .env
#    编辑 .env，设置 ACTIVE_VENDOR=deepseek 和 DEEPSEEK_API_KEY=sk-xxxxx

# 3. 一条命令启动（自动装依赖 → 拉取 embedding 模型 → 建索引 → 起 API + UI）
./quickstart.sh
```

启动后打开 **http://localhost:8501**，输入话题，点 **🚀 Generate**。

> 💡 `quickstart.sh` 会做预检：缺 `uv`、缺 Key、Ollama 没跑、端口被占 —— 都会在启动前给出明确提示，而不是跑到一半崩掉。

### 只想跑一次 CLI？

不需要起服务，不需要 UI：

```bash
uv sync
uv run python main.py --topic "AI Agent 取代白领"
```

产物落在 `flowbeast/data/outputs/<时间戳>/`。

### Docker 方式

```bash
docker-compose up --build
```

> ⚠️ 当前 Docker 镜像**未装 ffmpeg 和字体**，音频拼接那一步在容器内会失败。定型前暂不修（维护成本 > 收益），
> 本地跑或裸机跑不受影响。

---

## 入口点与命令

日常只需要记住前两个。

| # | 入口 | 命令 | 作用 | 端口 |
|---|------|------|------|------|
| 1 | **Streamlit UI** | `uv run streamlit run flowbeast/demo/app.py` | 图形化全流程演示（**依赖 #2 先启动**） | `8501` |
| 2 | **FastAPI 服务** | `uvicorn flowbeast.api.main:app --reload --port 8000` | 异步任务 API，4 个端点 | `8000` |
| 3 | **CLI 全流程** | `uv run python main.py --topic "话题"` | 不开服务，直接跑完 script→shots→audio | — |
| 4 | **反馈回流** | `uv run python -m flowbeast.fp3.feedback_ingest --report <报告> --views N --likes N` | 把真实播放数据回写 FP3，调整原子权重 | — |
| 5 | **种子数据** | `uv run python -m flowbeast.fp3.seed_data` | 初始化 FP3 向量库（首次运行自动触发） | — |

### FastAPI 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/health` | 健康检查 |
| `POST` | `/api/v1/generate` | 提交生成任务，立即返回 `task_id` |
| `GET` | `/api/v1/tasks/{task_id}` | 轮询任务状态与进度 |
| `GET` | `/api/v1/download/{file_type}/{run_id}` | 下载产物（`prompt_package` / `script` / `report` / `episode_audio`） |

```bash
# 示例：不进 UI，纯 API 跑一遍
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI Agent 取代白领"}'

curl http://localhost:8000/api/v1/tasks/<task_id>
```

---

## 你会得到什么

每次运行产出 5 类文件，全部落在 `flowbeast/data/outputs/<时间戳>/`：

```
20261014_175540/
├── script.json              # 结构化剧本（场景/台词/情绪/冲突）
├── shot_list.json           # 逐镜头分镜表（景别/运镜/时长/光照/SFX）
├── prompt_package.json      # ⭐ 最终产物 —— 喂给 AI 视频工具
├── production_report.json   # 生产报告（质量分/耗时/失败项）
├── episode_audio.mp3        # 拼接后的整集配音
└── audio/                   # 逐句 TTS 音频
    ├── s1_l0_林薇.mp3
    └── ...
```

`prompt_package.json` 的结构：

```jsonc
{
  "title": "...",
  "genre": "...",
  "core_hook": "...",
  "tags": [...],
  "emotion_curve_global": [...],
  "style_lock": { ... },     // 全局画风锁定，防止跨镜头风格漂移
  "shots": [                 // 逐镜头指令，直接映射到视频工具的 API 字段
    {
      "shot_id": "S01_SH001",
      "beat_type": "tension",        // 情绪节拍（驱动镜头，而非景别）
      "shot_type": "close_up",
      "camera_motion": "slow_push_in",
      "duration_sec": 4,
      "motion_intensity": 3,         // close-up 强制限速 ≤3，防五官崩坏
      "lighting": "harsh_fluorescent",
      "visual_prompt": "...",
      "negative_prompt": "..."
    }
  ]
}
```

> **关于 `motion_intensity` 限速**：可灵 2.0 图生视频中，面部特写只要运动强度 > 4，五官就会像橡皮泥一样融化。
> `shot_director.py` 里对 `close_up` 做了硬性 clamp —— 这是从实际生成失败中总结出的规则，不是拍脑袋。

---

## 架构

### 数据流

```
┌─ FP3 Viral Memory（护城河）───────────────────────────────────┐
│  FAISS 向量库 + 叙事原子（hook / pattern / emotion）+ QualityGate │
└───────────────────────────┬───────────────────────────────────┘
                            ▼
┌─ 生成 ────────────────────────────────────────────────────────┐
│  爆款结构注入 ──► 剧本生成 ──► Shot Director ──► TTS 音频      │
└───────────────────────────┬───────────────────────────────────┘
                            ▼
┌─ 交付 + 回流 ─────────────────────────────────────────────────┐
│  prompt_package.json ──► 成片交付 ──► views/likes ──► 原子权重 │
└───────────────────────────────────────────────────────────────┘
```

### 代码模块

| 模块 | 职责 | 关键文件 |
|------|------|----------|
| `flowbeast/fp3/` | **护城河** — 向量存储、检索、注入、反馈 | `store.py` `retriever.py` `injector.py` `schema.py` |
| `flowbeast/observe/quality/` | QualityGate — 9 维评分 + 去重 + 审计 | `scorer.py` `gate.py` |
| `flowbeast/drama/` | 生产管线（可替换的商品层） | `pipeline.py` `shot_director.py` `audio.py` |
| `flowbeast/core/` | 配置 + 多厂商 LLM 适配 | `config.py` `providers/` |
| `flowbeast/api/` | FastAPI 服务 | `main.py` |
| `flowbeast/demo/` | Streamlit 演示 UI | `app.py` |

### 多厂商适配

`flowbeast/core/providers/` 用注册表模式统一了 7 家厂商，切换只需改 `.env` 里的一行：

```
openai_compatible.py    →  deepseek / qwen / openai / glm / openrouter / ollama
anthropic_compatible.py →  anthropic（含 Token Plan 代理网关）
gemini_provider.py      →  gemini
embedding.py            →  ollama / openai / gemini
```

---

## 核心概念

### FP3 — 可组合的叙事原子

FP3 存储**可组合的叙事原子**。`ViralUnit` 只有三个字段，刻意保持最小：

| 字段 | 含义 | 性质 |
|------|------|------|
| `hook` | 开场钩子（前 3 秒） | 可插拔 —— 独立替换 |
| `pattern` | 冲突 / 结构模式 | 可迁移 —— 跨语义域通用 |
| `emotion` | 情绪序列 | 可重映射 —— 同形状不同情绪 |

检索到的原子被注入生成 prompt，让输出携带**已验证有效的结构**，而不是随机创意。

### Latent Grammar — 隐式语法

FP3 本质是一套内容生成的隐式语法：

- **原子 = 词汇**（hook 类型、冲突模式、情绪曲线、视觉风格、镜头语言）
- **合法组合 = 语法**（哪些 hook + 哪些 conflict + 哪些 emotion + 哪些 shot = 爆款）
- **QualityGate = 类型检查**（拒绝违反隐式语法的组合）

### QualityGate — 9 维评分

`flowbeast/observe/quality/config.py` 中定义，所有权重可通过 `QUALITY_` 前缀的环境变量覆盖：

| 维度 | 权重 | 维度 | 权重 |
|------|------|------|------|
| `hook_strength` | 0.20 | `pacing` | 0.08 |
| `emotional_intensity` | 0.15 | `engagement_density` | 0.08 |
| `retention_potential` | 0.15 | `conflict_density` | 0.08 |
| `novelty` | 0.10 | `replay_potential` | 0.06 |
| `virality_signals` | 0.10 | | |

**阈值**：`≥ 0.60` 接受 · `≥ 0.40` 转人工复核 · `< 0.40` 拒绝。另有 `0.98` 相似度的向量去重。

> ⚠️ **这些权重是拍的，不是标定的。** 9 个维度里有 4 个（合计 0.45 权重）只读 `unit.hook` 一个字段，
> 且互相高度相关。目前它**从来没给出过 ACCEPT**。别把它的分数当结论 —— 详见
> [commercialization_playbook.zh.md](.ai/current/commercialization_playbook.zh.md) Part 0。

### Audio Validation — 用耳朵做质量验证

Edge TTS 生成音频是**质量验证层**，不是最终产物。听觉比视觉更快暴露节奏和对话问题 —— 不用渲染视频，就能判断剧本是否成立。

---

## 技术栈

| 层 | 选型 |
|----|------|
| **语言 / 包管理** | Python 3.12+ · [uv](https://docs.astral.sh/uv/) |
| **数据校验** | Pydantic v2 · pydantic-settings |
| **向量检索** | FAISS（本地索引） |
| **LLM 接入** | OpenAI SDK · Anthropic SDK · Google GenAI（统一注册表封装） |
| **后端** | FastAPI · Uvicorn · BackgroundTasks |
| **前端** | Streamlit |
| **语音合成** | edge-tts（默认，免费） |
| **可观测性** | Loguru |
| **测试** | pytest（34 个用例） |
| **部署** | Docker · docker-compose · Railway（railpack） |

---

## 配置

所有配置集中在 `.env`（从 `.env.example` 复制）。核心项：

```bash
# ---- LLM ----
ACTIVE_VENDOR=deepseek              # deepseek | qwen | openai | anthropic | gemini | glm | openrouter | ollama
ACTIVE_MODEL=deepseek-chat          # 留空则用厂商默认模型
DEEPSEEK_API_KEY=sk-xxxxxxxx        # 只填你选的那家

# ---- Embedding（必须走本地 Ollama）----
EMBED_VENDOR=ollama
OLLAMA_BASE_URL=http://localhost:11434   # 裸机用 localhost；Docker 用 host.docker.internal
```

### ⚠️ 三个必须知道的配置陷阱

1. **改了 `.env` 必须重启后端服务。** `config.py` 在 **import 时**加载配置 —— 正在运行的 uvicorn 进程不会感知你的修改，表现是「Key 明明填了却报未配置」。

2. **`.env` 里的空值会覆盖 shell 环境变量。** `config.py` 用 `load_dotenv(override=True)`，所以 `OPENAI_API_KEY=`（空）会抹掉你 `~/.bashrc` 里已 export 的同名变量。**用不到的厂商，请整行注释掉，而不是留空。**

3. **`EMBED_MODEL=` 留空会覆盖代码默认值。** 同理会把 `nomic-embed-text` 抹成空字符串，导致 embedding 调用失败。需要覆盖时才显式写模型名。

另外两个厂商相关的坑：
- **`qwen` 这个 vendor 实际读的是 `DASHSCOPE_API_KEY`**，不是 `QWEN_API_KEY`（尽管 `.env.example` 两个都列了）。
- **DeepSeek 不提供 embedding 接口**，`EMBED_VENDOR` 改成 `deepseek` 会直接抛 `Unsupported embedding provider`。

---

## 测试

```bash
uv run pytest tests/ -q                      # 全部（34 个用例）
uv run pytest tests/test_fp3_quality.py -q   # QualityGate
uv run pytest -k "fp3" -v                    # 按关键字筛选
```

只保留能抓到**真实回归**的用例，覆盖：LLM 输出解析（`_extract_json` + 结构校验）、
prompt 组装分支、FP3 反馈提取、QualityGate 评分与审计落盘。

> 不为常量形状、源码文本、环境路径写测试 —— 那类断言不会抓到 bug，只会增加维护成本。

---

## 项目状态

**当前版本：`v0.5.0-mvp`（Demo 可用）**

管线端到端能跑通：**话题 → 剧本 → 分镜 → 配音 → 交付包**，本地 34 个测试通过。

**但下面这些必须知道：**

| 事项 | 状态 |
|------|------|
| 端到端管线（本地） | ✅ 跑得通 |
| Docker 内音频拼接 | 🔴 缺 ffmpeg/字体 —— 暂不修 |
| FP3 语料 | 🟡 约 20 条手写演示数据，0 部真实逆向脚本 |
| QualityGate | 🔴 从未给出过 ACCEPT，权重未标定 |
| 真实付费客户 | 🔴 **0** —— 这才是唯一重要的数字 |

> **旧方向（静态语料壁垒 / 逆向工程 / VTO 算子）已被证伪并移除。**
> `flowbeast/vto/`、`flowbeast/reverse/`、`flowbeast/hooks/`、QualityGate 的校准器已从代码库删除。
> 现在只保留：**FP3 爆款记忆 + 生成管线 + 质量门禁 + 交付包**。

---

## 故障排查

| 症状 | 原因 | 解决 |
|------|------|------|
| `API key not configured for vendor 'xxx'` | `.env` 缺失，或改完没重启服务 | 检查 `.env`；重启 uvicorn |
| UI 显示 `❌ API server not running` | FastAPI 没起，或端口不是 8000 | 先启动入口点 #2 |
| `404 page not found`（调 Ollama 时） | `OLLAMA_BASE_URL` 少了 `/v1` 后缀 | 用 `http://localhost:11434/v1` |
| 音频全部生成失败 / HTTP 403 | `edge-tts` 版本过旧，被微软网关拒绝 | `uv add "edge-tts>=7.3.1"`（**勿降级**） |
| `Unsupported embedding provider` | `EMBED_VENDOR` 设成了不提供 embedding 的厂商 | 改回 `ollama` |
| 换话题后结果高度雷同 | FP3 语料只有演示数据 | 见 [项目状态](#项目状态) |
| 端口被占用 | 上次进程没退干净 | `fuser -k 8501/tcp` |

---

## 目录结构

```
FlowBeast-p1/
├── main.py                    # 入口点 #3 —— CLI 全流程
├── quickstart.sh              # 一键启动（预检 + 建索引 + 起服务）
├── start_dev.sh               # 云部署启动脚本（Railway，读 $PORT）
├── start.sh                   # 容器内启动包装
├── dev.sh                     # devcontainer 内激活环境并开一个 shell
├── Dockerfile                 # 两阶段：development / production
├── docker-compose.yml         # 本地容器编排
├── pyproject.toml             # 依赖声明（uv 管理）
│
├── flowbeast/
│   ├── fp3/                   # ⭐ 护城河：向量存储 / 检索 / 注入 / 反馈
│   ├── observe/quality/       # QualityGate：评分 / 去重 / 审计
│   ├── drama/                 # 生产管线：剧本 / 分镜 / 音频
│   ├── core/                  # 配置 + 多厂商 LLM 适配
│   ├── api/                   # FastAPI 服务
│   ├── demo/                  # Streamlit UI
│   └── data/                  # 运行产物（输出 / 向量库）
│
├── assets/
│   └── style/                 # 视觉风格资产（调色板 / 渲染规则 / 负面提示词）
├── tests/                     # 34 个 pytest 用例
├── .ai/current/               # 定位 / 目标 / 状态 / 商业化手册
├── .cursor/rules/             # 开发规范
└── CLAUDE.md                  # AI 协作说明（含规则 0）
```

---

## 相关文档

| 文档 | 内容 |
|------|------|
| [`commercialization_playbook.zh.md`](.ai/current/commercialization_playbook.zh.md) | **商业化手册（中文，先读这份）** |
| [`decisions/001_project_positioning.md`](.ai/current/decisions/001_project_positioning.md) | 项目定位决策记录 |
| [`decisions/002_what_we_do_not_do.md`](.ai/current/decisions/002_what_we_do_not_do.md) | 「我们不做什么」 |
| [`goal.md`](.ai/current/goal.md) | 当前阶段目标 |
| [`status.md`](.ai/current/status.md) | 已接通 vs 桩代码清单 |
| [`capability_map.md`](.ai/current/capability_map.md) | 能力 → 现成工具对照表（规则 0 用） |
| [`CLAUDE.md`](CLAUDE.md) | 项目约定、规则 0、开发规范 |

---

## 许可

[Apache License 2.0](LICENSE)

<div align="center">
<sub>FlowBeast · 把爆款拆成原子，再编译成新的爆款</sub>
</div>
