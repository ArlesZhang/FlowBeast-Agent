# FlowBeast-Agent  
>**The Data Workflow Compiler for LLMops**

---

## Overview
**FlowBeast Agent** is an intelligent agent that automates and optimizes data workflows — from raw data ingestion to transformation and deployment — acting like a **compiler** for data engineering tasks.It converts high-level workflow descriptions into executable, efficient pipelines.

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

subgraph Feature ["01Feature Pipeline (感知层)"]
    direction TB
    FP1["Real-time Pipeline<br/><sub>Kafka / Flink / Spark<br/>实时与批处理链路</sub><br/><sub>(警惕架构过载:巨量工程)</sub>"]
    FP2["Python AI Stack<br/><sub>Pandas / NumPy / PyTorch<br/>数据清洗与特征工程</sub>"]
    FP3[("Vector DB / Embeddings<br/><sub>Milvus / Qdrant / Hybrid Search<br/>长期知识与特征储备</sub>")]
    FP1 --> FP2 --> FP3
end

classDef FoundationNode fill:#cce5ff,stroke:#3399ff,color:#000
class FP1,FP2,FP3 FoundationNode

%% ========================================
%% 2️⃣ TRAINING PIPELINE (T层 - 认知与精炼)
%% ========================================

subgraph Training ["02Training Pipeline (认知层)"]
    direction TB
    TP1["FuelGenius<br/><sub>训练数据精炼飞轮<br/>数据自动筛选与合成<br/><sub>(预留“人工审核”接口:防合成数据带毒)</sub>"]
    TP2["Model Fine-tuning<br/><sub>SFT / DPO / Unsloth<br/>模型指令微调与强化</sub>"]
    TP3{{"Model Registry<br/><sub>Weights / Adaptors<br/>私有模型权重管理仓库</sub>"}}
    TP1 --> TP2 --> TP3
end

%% ========================================
%% 3️⃣ INFERENCE PIPELINE (I层 - 执行与优化)
%% ========================================

subgraph Inference ["03 Inference Pipeline (执行层)"]
    direction TB
    IP1["Agent Workflow Engine<br/><sub>LangGraph / MCP<br/>多Agent编排与工具调用</sub>"]
    IP2["Reasoning Engine<br/><sub>RAG / Tool Use<br/>上下文感知与推理决策</sub>"]
    IP3["Inference Engineering<br/><sub>KV Cache / Batching / FinOps<br/>性能优化与Token成本建模</sub>"]
    IP1 --> IP2
    IP3 --> IP1
end

classDef InferenceNode fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px,color:#4A148C
class IP1,IP2,IP3 InferenceNode

%% ========================================
%% 4️⃣ PRODUCT LAYER (流量引擎)
%% ========================================

subgraph Product ["04 FlowBeast System"]
    direction TB
    APP["FlowBeast Agent<br/><sub>内容生成 -> (数据监控 + 优化策略)<br/>全自动流量增长引擎</sub>"]
end

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
class OBS1,OBS2 OrchestrationNode

%% ========================================
%% 🎯 STRATEGIC GOAL
%% ========================================

Goal(("AI Engineering Expert<br/>数据飞轮架构师 / 流量系统构建者"))

%% ========================================
%% 🔗 核心主干管道 (Vertical Pipeline)
%% ========================================

Foundation --> Feature
Feature -->|高质量训练数据供给| Training
Training -->|分发私有模型权重| Inference
Feature -.->|RAG 语义检索增强| IP2
Inference --> Product

%% ========================================
%% 🔄 飞轮反馈 (Closed Loop)
%% ========================================

Product -->|用户行为数据回流| Observe
Observe -->|失败样本 / 高分样本| Feature
Observe -->|精炼强化信号| Training

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
classDef inference fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#1B5E20
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

---

## Core Features
- **Workflow Compiler** — Translates data flow definitions into optimized DAGs (Directed Acyclic Graphs).  
- **AI-assisted Optimization** — Uses AI heuristics to suggest pipeline improvements.  
- **Multi-backend Support** — Integrates with Spark, Airflow, and DVC pipelines.  
- **Reproducible Builds** — Every data transformation is versioned and trackable.  
- **Declarative DSL** — Describe what you want, not how to run it.

## Tech stack

* **Core Languages:** Python, LLMOps
* **Agent Frameworks:** LangChain / LlamaIndex
* **Backend Services:** FastAPI, Uvicorn
* **Deployment/Containerization:** Docker
* **Frontend Interaction:** VS Code Extension API
* **Target Ecosystem:** dbt-core, Apache Airflow / Dagster

---

## Project Structure
```bash
.
├── create_project_structure.py
├── FlowBeast
│   ├── deployments
│   │   ├── docker
│   │   ├── k8s
│   │   └── terraform
│   ├── Dockerfile
│   ├── docs
│   │   ├── DEVELOPMENT.md
│   │   └── README.md
│   ├── flowbeast
│   │   ├── agent
│   │   ├── api
│   │   ├── codegen
│   │   ├── commercial
│   │   ├── compiler
│   │   ├── data
│   │   ├── execution
│   │   ├── __init__.py
│   │   ├── ir
│   │   └── __pycache__
│   ├── generated_workflow.py
│   ├── __init__.py
│   ├── main.py
│   ├── market_material
│   │   ├── case_studies
│   │   ├── docs
│   │   └── pricing
│   ├── pyproject.toml
│   ├── README.md
│   ├── requirements.txt
│   ├── run.py
│   ├── start_dev.sh
│   ├── start_production.sh
│   ├── test_data
│   │   └── input.csv
│   ├── tests
│   │   ├── conftest.py
│   │   ├── __init__.py
│   │   ├── test_codegen.py
│   │   └── test_compiler.py
│   ├── ultimate_verify.py
│   ├── uv.lock
│   ├── verify_cody.py
│   ├── verify.py
│   └── vs_code_extension
│       ├── media
│       ├── package.json
│       ├── src
│       ├── test
│       └── tsconfig.json
├── logs
│   ├── dev
│   └── prod
│       ├── flowdeastr_v2-bash_history_2025-11-08_1819.log
│       ├── flowdeast_v2-bash_history_2025-11-08_0958.log
│       └── flowdeast_v2-bash_history_2025-11-25_1501.log
└── start.sh

30 directories, 29 files
````

## Quick Start (To Be Completed)

1. **Environment:** Clone the repository and create a Python virtual environment.
2. **API Key:** Configure LLM API Key in the `.env` file.
3. **Run Backend:** `docker-compose up` (to be implemented) or `uvicorn src.main:app --reload`
4. **Install Extension:** Build `vsc_extension` and install it into local VS Code.
5. **Enjoy!** (to be implemented)

---

## Installation

```bash
git clone https://github.com/ArlesZhang/FlowBeast.git
cd FlowBeast-p1/FlowBeast
pip install -r requirements.txt
```

---

## ▶️ Run Example

```bash
python src/main.py --config examples/sample_workflow.yaml
```

---

## Roadmap

* [ ] Define DSL for workflow description
* [ ] Implement core compiler engine
* [ ] Integrate AI optimization agent
* [ ] Add Airflow backend
* [ ] Release v0.1.0

---

## Author

**Arles Zhang**

> Building AI-powered compiler systems for data engineers.
> GitHub: [@arleszhang](https://github.com/arleszhang)

---

### **requirements.txt**

```txt
# Core dependencies By GPT5 
fastapi==0.115.0
uvicorn==0.30.0

# Data workflow & orchestration
pandas==2.2.3
pydantic==2.9.0
networkx==3.3

# ML & optimization
scikit-learn==1.5.2

# Version control & reproducibility
dvc==3.50.0

# Testing & linting
pytest==8.3.3
black==24.10.0
````

```txt
# DataCody Agent Backend Dependencies By Gemini

# Web Framework and Server
fastapi==0.110.0
uvicorn[standard]==0.27.1

# LLM & Agent Framework
langchain==0.1.13  # 或者 llama-index，选择其一
pydantic==2.6.4    # 用于结构化输出 (JSON Schema)

# LLM Provider (假设使用 OpenAI)
openai==1.14.3
# 如果使用其他模型，例如 Claude:
# anthropic==0.23.1

# Data Engineering Tooling (用于解析 dbt 相关文件)
pyyaml==6.0.1
dbt-core==1.7.0  # 用于理解 dbt 的依赖结构和解析器

# 环境和调试
python-dotenv==1.0.1

# ------------------------------
# 可选依赖 (后续迭代时加入)
# ------------------------------
# 数据库/向量库 (用于 RAG 记忆)
# chromadb==0.4.24
# duckdb==0.10.1

# 分布式计算 (Spark集成)
# pyspark==3.5.0

# 文件操作/AST解析
# typed-ast==1.5.5

