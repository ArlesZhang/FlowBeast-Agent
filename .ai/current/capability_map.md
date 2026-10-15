# FlowBeast 能力映射表 (Capability Map)

> **⚠️ 商业化定位（2026-10-15）。** 见 [commercialization_playbook.zh.md](commercialization_playbook.zh.md)。
> 静态语料壁垒 / 低价抽取服务 / 品牌命名 / 提示词包四条路径已证伪；方向是**系统级工作流集成 + 业务结果交付**。
> **唯一验收标准：有真实付费证据。**
> VTO 算子、逆向工程、语料库流水线、QualityGate 校准器**已从代码库删除** —— 下表中指向它们的锚点已同步清理。

> **这份文档解决什么问题:** FlowBeast 目前离商业化还很远。但在把它继续做下去的过程中,
> 我要顺带练出六项能力 —— 多 Agent 协同、部署与 workflow 搭建、流程编排、Prompt 调优、
> Agent 调试与效果评估、训练效果量化。这份文档把**每一项能力锚定到项目里具体的模块和文件**,
> 并指定**可以直接拿来用的行业标杆**,避免重复造轮子。
>
> **核心原则:基础设施抄,领域知识自己造。**
> 追踪、评估、编排、调优的**管道**一律用成熟开源项目;只有 **FP3 原子**和 **QualityGate 的评分维度**
> 是领域资产,才考虑自己写 —— 而且能集成就不写。

创建于 2026-10-14。最后更新:2026-10-15。

---

## 0. 总览

| # | 能力 | 项目里的锚点 | 现状 | 直接采用 | 优先级 |
|---|------|--------------|------|----------|--------|
| 1 | 多 Agent 协同 | `drama/pipeline.py` 的线性调用链 | 🔴 无线程,但 `langgraph` 已装未用 | **LangGraph** | 中 |
| 2 | 部署与 workflow 搭建 | `Dockerfile` / `start_dev.sh` / `railpack.json` | 🟡 本地能跑通,**云端跑不起来、零 CI** | **GitHub Actions** + Railway/HF Spaces | 中 |
| 3 | Workflow 流程编排 | `run_full_pipeline()` 五阶段同步阻塞 | 🔴 手写重试循环 | **Prefect** | 中 |
| 4 | Prompt 指令调优 | `drama/prompt.py` | 🔴 全部靠肉眼调 | **DSPy** | 🔥 **高** |
| 5 | Agent 调试与效果评估 | `observe/quality/` 手搓评估器 | 🟡 有评估,**无追踪** | **Langfuse** + **RAGAS** | 🔥 **高** |
| 6 | 训练效果量化 | `fp3/feedback*` | 🟡 无实验追踪 | **RAGAS** + **W&B/MLflow** | 中 |

**建议顺序:5 → 4 → 1 → 3 → 6 → 2。**
先能看见(5),再能改进(4);有了评估基线,多 Agent 和编排才有意义。
部署放最后 —— 现在部署出去,只是把一个质量分不可信的系统暴露给用户,没有收益。
**但在拿到第一个付费客户之前,以上全部让位给 Phase A/B。**

---

## 1. 多 Agent 协同处理任务

### 锚点

| 位置 | 现状 |
|------|------|
| [flowbeast/drama/pipeline.py](../../flowbeast/drama/pipeline.py) | `run_full_pipeline(topic)` —— **一条同步直线**:生成剧本 → 质量门禁 → 分镜 → 逐句 TTS → 拼接。不是 Agent,是函数调用链 |
| 同上,重试逻辑 | `max 2 retries` 的 `for` 循环 —— 这是**手写的、退化版的** LangGraph 条件边 |
| [flowbeast/observe/quality/scorer.py](../../flowbeast/observe/quality/scorer.py) | 9 维评分器 —— 它**已经是一个 evaluator 角色**,只是没人这么用它 |
| `langgraph` | **已在 `pyproject.toml` 依赖里,全项目零引用** |

### 缺口

`langgraph` 装了不用,是这份文档里最明显的"免费午餐"。当前管线有三个天然的 Agent 化切点:

1. **evaluator-optimizer 循环** —— QualityGate 打分 → 不达标则带反馈重写。现在是一个粗暴的 `retry`,没有把**失败原因**回传给生成器。
2. **orchestrator-workers 并行** —— 分镜、音频、资产三条支线互不依赖,现在串行跑。
3. **逆向拆解的多轮反思** —— 提取出的 ViralScript 应该被另一个 Agent 质疑("这个 hook_type 判对了吗?"),现在是一次成型。

### 直接采用(不要自己造)

| 项目 | 说明 |
|------|------|
| **[LangGraph](https://github.com/langchain-ai/langgraph)** | 已装。`StateGraph` + 条件边 + checkpointer 直接替掉手写重试循环。checkpointer 还顺带解决"任务中断后无法恢复" |
| **[Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** | 先读这篇,再决定要不要上框架。它明确反对过早引入多 Agent —— 很多场景一个带工具的循环就够 |
| **[OpenAI Agents SDK](https://github.com/openai/openai-agents-python)** | 轻量替代方案,handoff 原语干净。若不想被 LangChain 生态绑定,选它 |
| **[CrewAI](https://github.com/crewAIInc/crewAI)** | 角色扮演式多 Agent,上手最快但可控性最差。**适合快速原型,不适合长期架构** |

### 第一个可执行动作

把 `run_full_pipeline` 里的 `for attempt in range(3)` 重写成 LangGraph 图:
`generate → gate → (条件边: score ≥ 0.65 ? END : critique → generate)`,
其中 `critique` 节点把 QualityGate 的**分维度得分**转成自然语言反馈塞回 prompt。
这一步不动任何业务逻辑,只换编排层 —— 风险最低,收益是立刻能看见"为什么这次没过"。

---

## 2. 部署与 workflow 搭建

### 锚点

| 位置 | 现状 |
|------|------|
| [Dockerfile](../../Dockerfile) | 两阶段(development / production),写得不错 |
| [docker-compose.yml](../../docker-compose.yml) | 本地编排,含 `extra_hosts` 让容器访问宿主 Ollama |
| [start_dev.sh](../../start_dev.sh) | **Railway 部署入口** —— 读 `$PORT` 环境变量起 uvicorn。这是你之前云部署留下的 |
| [railpack.json](../../railpack.json) | Railway 的构建声明(用 uv 装依赖) |
| [quickstart.sh](../../quickstart.sh) | 本地一键启动(2026-10-14 新增) |
| `.github/` | **不存在 —— 没有任何 CI** |

### 你之前那次云部署是什么

`start_dev.sh` + `railpack.json` 的组合说明:你当时把 FastAPI 服务部署到了 **Railway**。
Railway 注入 `$PORT`,脚本据此绑定端口;Railpack 负责构建。**它只部署了 API,没有部署 Streamlit UI** ——
所以即使当时跑通了,别人也看不到界面,只能调 API。这大概是你"忘了它的意义"的原因:它不完整。

### 为什么它现在仍然跑不起来(2026-10-15 核查)

上面那条"没有 UI"只是表象。真正堵死的是**依赖链**:

1. **Ollama 在 Railway 上不存在。**
   [`flowbeast/fp3/retriever.py:21`](../../flowbeast/fp3/retriever.py#L21) 的 `retrieve()` 第一行就是
   `embed_text(query)` → [`core/providers/embedding.py`](../../flowbeast/core/providers/embedding.py)
   的 ollama 分支 → HTTP 打到 `OLLAMA_BASE_URL`(本地 `localhost:11434`)。
   云上没有这个进程 → 连接被拒 → **检索直接抛异常,整条生成链路死掉** —— 也就是护城河死掉。

2. **不能靠改一行 `.env` 换成 API embedding。**
   各家维度不同:ollama `nomic-embed-text` **768** 维、qwen `text-embedding-v3` **1024** 维、
   openai / gemini **1536** 维。而 `fp3.index` 是**按 768 维建好的**。
   换 `EMBED_PROVIDER` 而不重建索引 → FAISS 维度不匹配直接报错。

3. **索引本身在临时磁盘上。** `flowbeast/data/outputs/vector_store/fp3/fp3.index` 是本地文件。
   多数 PaaS 容器重启即清空 → 每次部署都得重建索引(而重建又要先解决第 1 条)。

**结论:让 Railway 真跑起来是一个小项目,不是一次配置调整。**
顺序是:换成托管 embedding 厂商 → 按新维度重建索引 → 把索引做成构建期产物或挂载卷 →
启动命令里加上 Streamlit → 加限流与花费上限。

**所以现在怎么办:文件留着(一共不到 5 行,零成本),但别再把它当成"部署方案"。**
它真正的价值是能力 #2 的**实物教材** —— 你亲手踩过 `$PORT`、构建声明、临时磁盘这几课。
要给别人体验,走**静态展示页**(预生成产物 + 截图/录屏),那条路一次性绕开
Ollama、临时磁盘、成本裸露、2-4 分钟延迟这四个问题。

### 缺口

- **零 CI**:67 个测试没有自动跑过。改一行代码不知道有没有破坏别的东西。
- **状态是文件**:`api/main.py` 的任务注册表落在 `flowbeast/data/runtime/tasks_state.json`,单进程内存态。多 worker 或多实例直接错乱;容器重启即丢失。
- **成本裸露**:任何人访问都能触发一次真实的 LLM 调用。公开 Demo 必须先加限流与花费上限。
- **产物在本地磁盘**:`flowbeast/data/outputs/` 写容器本地盘。多数 PaaS 的磁盘是临时的,重启即清空。

### 直接采用

| 项目 | 说明 |
|------|------|
| **[GitHub Actions](https://github.com/features/actions)** | 先加一个 `pytest` 的 workflow(约 20 行 YAML)。这是投入产出比最高的一步 |
| **[Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-sdks-docker)** | 免费 Docker 托管,**对 Streamlit 有原生支持**。做 Demo 展示的最优解 |
| **[Railway](https://railway.app/)** / **[Render](https://render.com/)** / **[Fly.io](https://fly.io/)** | 完整应用托管。Railway 你已用过;Fly.io 的 volume + 多区域更专业 |
| **[Modal](https://modal.com/)** | 无服务器 GPU。**将来真要接视频生成(Seedance/Kling)时用这个**,不要自己管 GPU 机器 |

### 第一个可执行动作

加 `.github/workflows/test.yml`,跑 `uv run pytest tests/ -q`。
在"部署到公网"之前先有"每次提交都验证" —— 后者是所有部署的地基。

---

## 3. Workflow 流程编排

### 锚点

| 位置 | 现状 |
|------|------|
| `run_full_pipeline()` | 五个阶段同步阻塞串行:剧本 → 门禁 → 分镜 → 音频(逐句) → 拼接 |
| [flowbeast/api/main.py](../../flowbeast/api/main.py) | FastAPI `BackgroundTasks` + 内存态 + JSON 落盘。**没有队列、没有重试、没有超时、没有断点续跑** |
| [flowbeast/drama/audio.py](../../flowbeast/drama/audio.py) | 42 句台词逐个调 edge-tts。**任何一句失败,整条链没有独立重试** |
| 产物落盘 | 每阶段各自写 `flowbeast/data/outputs/<ts>/`,无事务、无原子性 |

### 缺口

这是最典型的"应该用引擎却手写"的地方。当前管线缺三样:

1. **持久化执行** —— 进程挂了,已生成的 17 个音频文件白做。
2. **细粒度重试** —— TTS 第 23 句 403,应该只重试第 23 句,而不是整个管线。
3. **可观测的执行历史** —— 现在只能翻 `/tmp/flowbeast_api.log`。

### 直接采用

| 项目 | 说明 |
|------|------|
| **[Prefect](https://github.com/PrefectHQ/prefect)** | **首选**。`@flow` / `@task` 装饰器改造量最小,自带重试、缓存、UI、失败续跑。Python 原生,和现有代码风格冲突最小 |
| **[Dagster](https://github.com/dagster-io/dagster)** | 资产(asset)导向,适合"产物是文件"的场景 —— FlowBeast 完全符合。比 Prefect 重,但数据血缘更强 |
| **[Temporal](https://github.com/temporalio/temporal)** | 工业级持久化工作流,最强也最重。需要单独跑服务,**不建议现在上** |
| **[Dify](https://github.com/langgenius/dify)** / **[n8n](https://github.com/n8n-io/n8n)** | 低代码 LLM 编排。**学概念很好,别用来做核心** —— 你的护城河会被框在别人的抽象里 |

### 第一个可执行动作

只把**音频生成阶段**改成 Prefect task 列表(`audio.py` 里逐句 TTS 的那个循环)。
这是收益最直接的一段:17~42 个独立单元,天然可并行、可重试、可缓存。
改造完你会立刻拿到一张"哪句话失败了、重试了几次"的执行图。

---

## 4. Prompt 指令调优 🔥

### 锚点

| 位置 | 现状 |
|------|------|
| [flowbeast/drama/prompt.py](../../flowbeast/drama/prompt.py) `build_prompt()` + `NARRATIVE_STRUCTURES` | 剧本生成的主 prompt,**纯手写字符串** |
| [flowbeast/observe/quality/scorer.py](../../flowbeast/observe/quality/scorer.py) | **现成的评估指标** —— 9 维打分 |

### 缺口

**FlowBeast 的产品本质就是 Prompt 编译,但它的 Prompt 却全靠肉眼调。** 这是最讽刺、也最该先补的一环。

好消息是:你已经有了优化的前提条件 —— **一个自动化的、可复现的评分函数**(QualityGate)。
Prompt 调优最难的部分就是"怎么知道改得更好",而这部分你已经有了。

### 直接采用

| 项目 | 说明 |
|------|------|
| **[DSPy](https://github.com/stanfordnlp/dspy)** | **核心推荐**。把 prompt 当**可编译产物**而非手写文本:`Signature` 定义输入输出,`MIPROv2` 优化器自动搜索指令与示例。3.x 已是生产可用状态 |
| **GEPA**(DSPy 内置,ICLR 2026) | 无梯度优化器,用自然语言反思改进 prompt。据 Dropbox 生产案例:相关性判断的 NMSE 降低 45%,模型适配周期从 1–2 周压到 1–2 天 |
| **[Promptfoo](https://github.com/promptfoo/promptfoo)** | Prompt 的**单元测试框架**。声明式 YAML 定义用例与断言,CI 里跑。比 DSPy 轻,适合先建立回归防线 |
| [Anthropic Prompt Engineering 文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) | 手工调优的底层原理。**先读这个再上 DSPy** —— 否则你不知道优化器在改什么 |

### 注意事项

- DSPy 的 `MIPROv2` 一次优化运行**要花钱**(约 $20–100/次),且可能过拟合你的评分指标。
- 官方经验:**20–100 个样本的效果常常优于 500 个**(样本太多会导致 prompt 膨胀)。
- 一旦换模型(比如 DeepSeek 升版),prompt 需要**重新编译** —— 这正是"prompt 即代码"的价值,也正是你必须做版本管理的原因。

### 第一个可执行动作

用 **Promptfoo**(不是 DSPy)给 `build_prompt` 建 5–10 条回归用例:
输入话题 → 断言输出的 `core_hook` 非空、`scenes` 数量 ≥ 3、`emotion_curve_global` 长度 ≥ 3。
这一步不优化任何东西,只是**给现在的手写 prompt 装上安全网**。有了网,后面才敢动。

---

## 5. Agent 调试与效果评估 🔥

### 锚点

| 位置 | 现状 |
|------|------|
| [flowbeast/observe/quality/](../../flowbeast/observe/quality/) | `scorer.py`(9 维)/ `gate.py`(门禁)/ `dedup.py`(去重)—— **一套手搓的评估体系** |
| `pyproject.toml` | `# "ragas"` **被注释掉了** —— 你当时已经想到了,只是没做 |
| `flowbeast/data/quality_audit/` | 审计目录,已有落盘习惯 |
| 全项目 | **无任何 tracing** —— 不知道哪次 LLM 调用产生了哪个输出 |

### 缺口

你**已经在做评估**(QualityGate),但**看不见执行**。具体缺:

- 没有 span 级视图:一次生成里,检索花了多久?prompt 多长?LLM 返回了几次才解析成功?
- 没有跨运行对比:本周的 5 次运行和上周的 5 次,质量分布变了吗?
- FP3 检索本身是一个 **RAG 系统**,但**从未用 RAG 指标衡量过** —— 检索回来的原子到底相不相关?

### 直接采用

| 项目 | 说明 |
|------|------|
| **[Langfuse](https://github.com/langfuse/langfuse)** | **首选**。MIT/Apache 核心,免费 Docker 自托管,框架无关,原生吃 OpenTelemetry。免费云档 50K units/月。2026-01 被 ClickHouse 收购,开源与自托管承诺保留 |
| **[Opik (Comet)](https://github.com/comet-ml/opik)** | Apache 2.0,功能覆盖最接近 Braintrust 的开源替代。追踪 + LLM-as-judge + 数据集 + 实验,一个项目全包 |
| **[Arize Phoenix](https://github.com/Arize-ai/phoenix)** | Elastic License 2.0,单进程、极轻量。**本地调试首选**,起一个进程就有 UI |
| **[RAGAS](https://github.com/explodinggradients/ragas)** | 你的 `pyproject.toml` 里已经写了。专门评估 RAG:context precision/recall、faithfulness、answer relevancy —— **直接对应 FP3 检索质量** |
| **[DeepEval](https://github.com/confident-ai/deepeval)** | Pytest 风格写 LLM 断言。你已经用 pytest,迁移成本几乎为零 |
| **[OpenTelemetry GenAI 语义约定](https://opentelemetry.io/docs/specs/semconv/gen-ai/)** | 底层标准。按它埋点,上面这些后端可以随时换,不用重新插桩 |

### 第一个可执行动作

把 `# "ragas"` 那行的注释取消,给 FP3 检索写一个测试:
给定一个话题,检索回来的 top-k 原子与话题的相关度是多少。
**这直接回答了一个你现在答不上来的问题:语料只有 20 条演示数据时,检索质量到底有多差?**
这个数字会是 Phase 0 语料建设最有力的论据。

---

## 6. 训练效果量化

### 锚点

| 位置 | 现状 |
|------|------|
| [flowbeast/fp3/feedback.py](../../flowbeast/fp3/feedback.py) | `extract_unit_from_script` —— 把生成脚本映射回 FP3 原子 |
| `flowbeast/fp3/feedback_ingest.py` | CLI:摄入 views/likes 回流 FP3 |
| `flowbeast/data/quality_audit/` | 每次门禁决策落盘 —— **这就是可量化的原始数据** |

### 重要澄清

**"训练效果量化"在当前阶段 ≠ 微调模型。** 项目里没有任何需要微调的东西:
你在调的是 prompt、原子权重、检索策略。这些属于**评估驱动的优化**,不是训练。

过早跳到 LoRA/微调是这条路上最常见的陷阱 —— 你还没有干净的评估集,
微调出来的东西根本无法判断好坏。**先把第 5 项做扎实。**

真正需要"训练"的时刻会在:你有 300+ 条真实语料、有稳定的评分体系、
且发现**无论怎么调 prompt 都撞到天花板**的时候。那时再说。

### 直接采用

| 项目 | 说明 |
|------|------|
| **[Weights & Biases](https://github.com/wandb/wandb)** / **[MLflow](https://github.com/mlflow/mlflow)** | 实验追踪。每次改 prompt / 改权重跑一次,记录指标曲线。**"效果量化"的载体就是它** |
| **[Evidently](https://github.com/evidentlyai/evidently)** | 数据漂移与分布对比 —— 生成分布 vs 交付后真实反馈分布 |
| **[scipy.stats](https://docs.scipy.org/doc/scipy/reference/stats.html)** | 显著性检验(t-test / Mann-Whitney / 二项检验)直接用 scipy,别自己写 |
| **将来再说:** [PEFT/LoRA](https://github.com/huggingface/peft) · [TRL](https://github.com/huggingface/trl) · [Unsloth](https://github.com/unslothai/unsloth) | 微调工具链。**现在不要碰** |

### 第一个可执行动作

把 `flowbeast/data/quality_audit/` 里已有的评分记录读出来,用 `scipy.stats` 算一件事:
**9 个维度和总分之间的相关性是多少?**
如果某个维度和总分的相关性接近 1,说明它没有独立信息 —— 它只是在给别的维度加权。
这一步不改任何代码,只回答一个问题:**我现在这套 9 维评分,到底有几个维度是真在起作用的?**

---

## 7. 重复造轮子黑名单

以下东西**已经有人做好了,不要自己写**:

| ❌ 不要自己写 | ✅ 用这个 | 状态 |
|--------------|----------|------|
| LLM 调用追踪 / Span | Langfuse / Opik / Phoenix | 未接入 |
| RAG 评估指标 | RAGAS | 依赖已注释 |
| Prompt 版本管理与回归测试 | Promptfoo / DSPy | 未接入 |
| 工作流引擎 / 重试 / 断点续跑 | Prefect / LangGraph | 手写中 |
| 多 Agent 编排 | LangGraph(已装) | 未使用 |
| 向量数据库 | FAISS(已用)/ Qdrant(已声明) | ✅ 已在用 |
| LLM 厂商适配 | 自研 `providers/` 注册表 | ✅ **这个写得对**,7 家厂商统一抽象 |
| 结构化输出解析 | Pydantic(已用) | ⚠️ 但 LLM 返回仍是脏 JSON,见下 |
| 实验追踪 / 指标曲线 | W&B / MLflow | 未接入 |
| 显著性检验 | scipy.stats | 手写中 |
| TTS | edge-tts(已用)/ ElevenLabs(已声明) | ✅ 已在用 |
| CI/CD | GitHub Actions | **完全没有** |

### ⚠️ 一条具体的债

`shot_director.py` 里的 `int(scene.get("id", 0))` 加 try/except 回退 ——
这是**手工修补 LLM 输出类型不稳定**的典型症状。
正确做法是用 **structured output**(OpenAI/DeepSeek 的 `response_format` /
Instructor / Pydantic AI)在源头约束,而不是在每个消费点防御。
这类手写防御代码会随着项目增长不断扩散。

---

## 8. 哪些必须自己造(护城河)

抄基础设施的前提是:**清楚哪些不能抄**。

| ✅ 必须自己写 | 为什么 |
|--------------|--------|
| **FP3 原子 schema**([fp3/schema.py](../../flowbeast/fp3/schema.py)) | Hook / Pattern / Emotion —— 这是领域知识,没有现成库 |
| **交付流程本身** | 「话题 → 成片」这条链路的编排,以及按集交付的打包方式 —— 这是生意,不是代码 |
| **QualityGate 的维度与权重**([quality/config.py](../../flowbeast/observe/quality/config.py)) | 9 个维度、`hook_strength=0.20` 这些数字 —— 是判断力,不是代码。**但承载它的管道应该换成库** |
| **Latent Grammar** | "哪些原子组合合法"—— 核心假设 |
| ~~VTO 算子语义~~ | ❌ 已证伪,代码已删 |
| ~~静态语料库~~ | ❌ 已证伪 —— 能被轻易复制的东西撑不起定价 |

**判据:** 如果一段代码换掉之后,FlowBeast 就不再是 FlowBeast 了,那它是护城河,自己写。
如果换掉之后只是"用了另一家的工具",那就该换。

---

## 9. 可扩展性:项目应该长成什么样

要让将来的接入是"插上"而不是"重写",现在就该留的口子:

| 扩展点 | 现状 | 应该变成 |
|--------|------|----------|
| **QualityGate 维度** | 9 个维度在 `scorer.py` 里硬编码 | 插件式:每个维度一个类,可增删、可重组权重,可被外部工具(RAGAS)替换 |
| **LLM 厂商** | ✅ `core/providers/` 注册表,7 家厂商 | **保持,这是范本** |
| **执行层** | `run_full_pipeline()` 写死五阶段 | 定义 stage 接口,允许 Prefect/LangGraph 接管编排 |
| **产物输出** | 写本地磁盘 | 抽象成 sink(本地 / S3 / OSS),部署到 PaaS 的必要前提 |
| **外部集成面** | FastAPI 4 个端点 | 这就是对外接口。将来 webhook / MCP server 都从这里长出来 |

**一句话:凡是"将来会有第二个实现"的地方,现在就用注册表/接口包一层。**

---

## 10. 参考资源

**方法论**
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)

**实践案例**
- [Dropbox — Optimizing Dash's relevance judge with DSPy](https://dropbox.tech/machine-learning/optimizing-dropbox-dash-relevance-judge-with-dspy)(真实生产数据:DSPy 相对手调 prompt 降低 NMSE 45%)
- [Decagon — Optimizing GEPA for production](https://decagon.ai/blog/optimizing-gepa-for-production)(20–100 样本优于 500 样本的实证)

**工具文档**
- [DSPy](https://dspy.ai/) · [LangGraph](https://langchain-ai.github.io/langgraph/) · [Prefect](https://docs.prefect.io/) · [Langfuse](https://langfuse.com/docs) · [RAGAS](https://docs.ragas.io/) · [Promptfoo](https://www.promptfoo.dev/docs/)

---

## 11. 检查清单:每完成一项就打勾

- [ ] **CI 存在** —— `.github/workflows/test.yml` 跑通 34 个测试
- [ ] **能看见执行** —— Langfuse(或 Phoenix)里能看到一次完整生成的 span 树
- [ ] **检索质量有数字** —— RAGAS 给出 FP3 top-k 检索的相关度基线
- [ ] **Prompt 有回归测试** —— Promptfoo 覆盖 `drama/prompt.py:build_prompt`
- [ ] **重试不再是手写的** —— `run_full_pipeline` 用 LangGraph 图或 Prefect flow 表达
- [ ] **Prompt 可编译** —— DSPy 用 QualityGate 指标优化过至少一个 prompt
- [ ] **指标可对比** —— W&B/MLflow 里有跨版本的指标曲线
- [ ] **换模型不用改代码** —— 改 `.env` 一行即可切换,且 prompt 有重新编译流程

---

*相关文档:[goal.md](goal.md) · [status.md](status.md) · [roadmap.md](roadmap.md) · [decisions/](decisions/)*
