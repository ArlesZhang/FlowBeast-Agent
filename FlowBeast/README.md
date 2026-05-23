## Text_scripts


## FlowBeast Flamwork for Agent-Centric

```mermaid
flowchart TB

%% ========================================
%% 0️⃣ FOUNDATION - 能源与基础设施 (融合 Git/CI/CD)
%% ========================================

subgraph Foundation["00 基础底座 | Infrastructure"]
    direction LR
    F1["Linux / Shell<br/><sub>自动化与生产环境</sub>"]
    F2["SQL / DuckDB / NoSQL<br/><sub>数据存储与多维分析</sub>"]
    F3["Git / Docker / CI/CD<br/><sub>版本控制与可部署基座</sub>"]
end

classDef DataNode fill:#d4edda,stroke:#28a745,color:#000
class F1,F2,F3 DataNode

%% ========================================
%% 1️⃣ FEATURE PIPELINE (F层 - 感知与计算)
%% ========================================

subgraph Feature ["01Feature Pipeline "]
    direction TB
    FP2["Python AI Stack<br/><sub>Pandas / NumPy / PyTorch<br/>数据清洗与特征工程</sub>"]
    FP3[("Vector DB / Embeddings<br/><sub>LlamaIndex / Qdrant<br/>长期知识与特征储备</sub>")]
    FP2 --> FP3
end

classDef FoundationNode fill:#cce5ff,stroke:#3399ff,color:#000
class FP2,FP3 FoundationNode

%% ========================================
%% 2️⃣ TRAINING PIPELINE (T层 - 认知与精炼)
%% ========================================

subgraph Training ["02Training Pipeline (认知层)"]
    direction TB
    TP1["FuelGenius<br/><sub>训练数据精炼飞轮<br/>数据自动筛选与合成&去重<br/><sub>(预留“人工审核”接口:防合成数据带毒)</sub>"]

end

classDef OrchestrationNode fill:#ffe5b4,stroke:#ff9900,color:#000
class TP1 OrchestrationNode

%% ========================================
%% 3️⃣ INFERENCE PIPELINE (I层 - 执行与优化)
%% ========================================

subgraph Inference ["03 Inference Pipeline (执行层)"]
    direction TB
    IP1["Reasoning Engine<br/><sub>RAG | Memory<br/>IP1-Retrieval & Reasoning</sub>"]
    IP2["Agent Workflow Engine<br/><sub>LangGraph / MCP<br/>IP2-Muit-Agent & Tool Use<br/><sub>(Images（Flux/Midj）& Vedios（Luma/Runway）API )</sub>"]
    IP3["Inference Engineering<br/><sub>KV&Context Cache / FinOps<br/>Performance Optimization & Token Cost Monitoring</sub>"]
    IP1 --> IP2
    IP2 --> IP1
    IP3 --> IP1
end

classDef InferenceNode fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px,color:#4A148C
class IP1,IP2,IP3 InferenceNode

%% ========================================
%% 4️⃣ PRODUCT LAYER (流量引擎)
%% ========================================

subgraph Product ["04 FlowBeast System"]
    direction TB
    APP["FlowBeast Agent<br/><sub>内容生成 -> (数据监控 + 优化策略)<br/>全自动流量增长引擎<br/><sub>(防毒:人工点击发布)</sub>"]
end

classDef app fill:#FCE4EC,stroke:#F06292,stroke-width:2px,color:#880E4F
class APP app


%% ========================================
%% 5️⃣ OBSERVABILITY (全局反馈中枢)
%% ========================================

subgraph Observe ["05 观测与反馈中枢 | Obser"]
    direction TB
    OBS0[数据分布监控<br/><sub>01层实时抓取的数据逻辑变动]
    OBS1["RAG Evaluation<br/><sub>Ragas / TruLens / Recall<br/>召回评估与质量基准:01 & 02</sub>"]
    OBS2["LLMOps & Monitoring<br/><sub>LangSmith / Phoenix / Opik<br/>链路追踪与全成本监控:03</sub>"]
    OBS1 --> OBS2
end

classDef OrchestrationNode fill:#ffe5b4,stroke:#ff9900,color:#000
class OBS0,OBS1,OBS2 OrchestrationNode

%% ========================================
%% 🎯 STRATEGIC GOAL
%% ========================================

Goal(("AI Engineering Expert<br/>数据飞轮架构师 / 流量系统构建者"))

%% ========================================
%% 🔗 核心主干管道 (Vertical Pipeline)
%% ========================================

Foundation -.->|互联网原始数据| FP2
FP2 -.->|高质量训练数据供给| Training
Training -.->|精炼后存储| FP3
FP3 -.->|RAG 语义检索增强| IP1
IP2 -.-> Product

%% ========================================
%% 🔄 飞轮反馈 (Closed Loop)
%% ========================================

Product --> |用户行为数据回流| Observe
Observe -.-> |Failure / Success| FP2
Observe --> |精炼强化信号| Training

%% ========================================
%% 🚀 收敛
%% ========================================

Product --> Goal

%% ========================================
%% 🎨 样式设置 (高对比度明亮色系)
%% ========================================

classDef foundation fill:#F8F9FA,stroke:#DEE2E6,stroke-width:2px,color:#212529
classDef feature fill:#E3F2FD,stroke:#2196F3,stroke-width:2px,color:#0D47A1
classDef training fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#E65100
classDef inference fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px,color:#4A148C
classDef product fill:#FCE4EC,stroke:#F06292,stroke-width:2px,color:#880E4F
classDef observe fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px,color:#4A148C
classDef goal fill:#FFFDE7,stroke:#FBC02D,stroke-width:3px,color:#000

class Foundation foundation
class Feature feature
class Training training
class Inference inference
class Product product
class Observe observe
class Goal goal
```


### Drama Pipeline Structure

**flowbeast/drama** 目录下的逻辑流：

> **总览**：一条「选题 →（prompt + fp3）→ 剧本 JSON → 落盘 → 配音 → 报告」流水线。`fp3` 只在 **generator** 内参与：在调用 LLM 之前把检索到的基因拼进 prompt。

```mermaid
flowchart LR
  topic[topic 字符串]
  prompt[prompt.py: build_prompt]
  subgraph FP3[fp3]
    RET[retriever.retrieve]
    INJ[injector.inject_prompt]
    RET --> INJ
  end
  gen[generator.py: generate_script]
  disk[(script.json 等)]
  aud[audio.py: generate_audio]
  rep[(production_report.json)]

  topic --> prompt
  topic --> RET
  prompt --> INJ
  INJ --> gen
  gen --> disk
  gen --> aud
  aud --> rep
```

### FP3 子系统（与上图中 `FP3` 框一致）

```mermaid
flowchart LR
  subgraph WRITE["① 建库（离线）"]
    direction TB
    SCH[schema: ViralUnit + ViralScript]
    BLD[builder + embed_unit]
    SEED[seed_data / reverse_engineered]
    REV[reverse_engineer CLI]
    STW[store.add → save]
    SCH -.-> BLD
    REV --> BLD
    SEED --> STW
    BLD --> STW
  end

  subgraph READ["② 在线检索（generator 内）"]
    direction LR
    EMB[embedding.embed_text]
    SRH[store.search]
    EMB --> SRH
  end

  subgraph CAL["③ QualityGate 校准"]
    direction LR
    CLB[calibrator]
    RAS[ReferenceAnchoredScorer]
    CLB --> RAS
  end

  WRITE -.->|索引与 meta 文件| READ
  WRITE -.->|参考集| CAL
```

**drama 与 fp3 的结合点**（唯一）：`flowbeast/drama/generator.py` → `generate_script`：先 `build_prompt(topic)`，再 `FP3Retriever.retrieve(topic)`（内部 **embedding → store.search**），再 `inject_prompt(base_prompt, examples)`，最后 `llm_call`。

`core/config` 的 `settings` 在 pipeline、generator、audio、fp3 的 `store` 路径上提供目录、模型、Key 等。

### 数据飞轮（1→0 逆向拆解引擎）

```
人工筛选市场爆款 → reverse_engineer CLI → ViralScript 解剖档案
                                                  │
                                        ┌─────────┘
                                        ▼
                              QualityGate 校准器（参考集分布对比）
                                        │
                                        ▼
                              脚本生成（FP3 RAG 增强）
                                        │
                                        ▼
                              高质量输出 → 回流 FP3
```

- **阶段A (1→0)：** 人工筛选 → 逆向拆解 → 系统注入（含正负样本）
- **阶段B (0→1)：** 质量校准 → 生成质量提升
- **阶段C (自转)：** 生成内容回流 → 知识库增长 → 生成更好

使用 `uv run python -m flowbeast.tools.reverse_engineer` 将真实漫剧转为 ViralScript 档案。

一流项目:用 pytest + 清晰目录/标记 + pyproject 约定 + CI 分档 + 文档 解决「又全又快」和「脚本 vs 测」的边界；很少靠「一个统一入口文件」。