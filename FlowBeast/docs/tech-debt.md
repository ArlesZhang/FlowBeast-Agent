# Tech Debt & Roadmap

> **原则**：MVP 速度可以妥协，但必须「显性化」——让代码、债单、决策形成可追溯闭环。

## 状态定义

| 状态 | 含义 | 处理优先级 |
|------|------|-----------|
| `Stub` | 占位实现，功能可运行但未真实实现 | P1~P2 |
| `Debt` | 已知缺陷/代码妥协，需修复 | P0~P1 |
| `Risk` | 潜在风险，可能爆雷 | P0~P1 |
| `Idea` | 未承诺的灵感，不进主 Roadmap | 按需跟进 |

## Core Pipeline

### FB-001 — 统一配置导入路径

- **类型**: `Debt`
- **位置**: `flowbeast/api/main.py`, `flowbeast/core/config.py`
- **现状**: 部分模块尝试从 `flowbeast.config` 导入
- **目标**: 收敛至 `from flowbeast.core.config import settings`
- **优先级**: `P0`
- **状态**: Open

### FB-002 — 多供应商 Embedding 占位

- **类型**: `Stub`
- **位置**: `flowbeast/fp3/embedding.py`
- **现状**: 非 Gemini 返回 `[0.0] * 1536`
- **目标**: 接入 `LiteLLM` 统一接口
- **优先级**: `P1`
- **状态**: Open

## FP3 RAG Layer

### FB-003 — 数据契约不一致风险

- **类型**: `Risk`
- **位置**: `flowbeast/fp3/injector.py`
- **现象**: 检索结果缺失键导致注入失败
- **目标**: 添加 `schema.py` 类型校验
- **优先级**: `P1`
- **状态**: Open

### FB-004 — 自动化回流闭环

- **类型**: `Idea`
- **位置**: `scripts/feedback_loop.py`
- **想法**: 筛选高质量 script.json 自动转 ViralUnit
- **优先级**: `P2`
- **状态**: Parked

## Environment & Tooling

### FB-005 — Docker 卷权限问题

- **类型**: `Debt`
- **位置**: `docker-compose.yml`, `Dockerfile`
- **现象**: 容器内创建目录时权限冲突
- **目标**: Dockerfile 指定 `USER arleszhang`
- **优先级**: `P1`
- **状态**: Open
