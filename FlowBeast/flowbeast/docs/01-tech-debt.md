# Tech Debt & Roadmap

> **原则**：MVP 速度可以妥协，但必须「显性化」——让代码、债单、决策形成可追溯闭环。

## 状态定义

| 状态 | 含义 | 处理优先级 |
|------|------|-----------|
| `Stub` | 占位实现，功能可运行但未真实实现 | P1~P2（看阻塞程度） |
| `Debt` | 已知缺陷/代码妥协，需修复 | P0~P1 |
| `Risk` | 潜在风险，可能爆雷 | P0~P1 |
| `Idea` | 未承诺的灵感，不进主 Roadmap | 按需跟进 |

## 与代码的关联方式

**在代码中**：`# FB-xxx: 简短说明`
**在债单中**：`- **位置**: `path/to/file.py:123``

---

## Core Pipeline

### FB-001 — 统一配置导入路径

- **类型**: `Debt`
- **位置**: `flowbeast/api/main.py:5`, `flowbeast/core/config.py`
- **现状**: 部分模块尝试从 `flowbeast.config` 导入，导致 `ImportError`
- **目标**: 全部收敛至 `from flowbeast.core.config import settings`
- **阻塞**: 代码重构，无外部依赖
- **优先级**: `P0` (阻塞型)
- **记录日期**: 2026-04-29
- **状态**: Open

### FB-002 — 多供应商 Embedding 占位

- **类型**: `Stub`
- **位置**: `flowbeast/fp3/embedding.py:4`
- **现状**: 非 Gemini 供应商返回 `[0.0] * 1536` 零向量
- **目标**: 接入 `LiteLLM` 的 embedding 统一接口
- **阻塞**: Qwen API 接入完成
- **优先级**: `P1`
- **记录日期**: 2026-04-29
- **状态**: Open

---

## FP3 RAG Layer

### FB-003 — 数据契约不一致风险

- **类型**: `Risk`
- **位置**: `flowbeast/fp3/injector.py`
- **现象**: 检索结果若缺失 `hook`/`pattern` 等键，注入失败
- **现状**: 临时使用 `get(key, "N/A")` 规避
- **目标**: 在 `schema.py` 中添加严格的类型校验
- **阻塞**: FP3 schema 设计定型
- **优先级**: `P1`
- **记录日期**: 2026-04-29
- **状态**: Open

### FB-004 — 自动化回流闭环

- **类型**: `Idea`
- **位置**: `scripts/feedback_loop.py`
- **想法**: 筛选高质量 `script.json`（反馈分 > 0.8），自动转 `ViralUnit` 并入库
- **依赖**: FP3 基础稳定 + feedback_loop 健壮
- **备注**: 属于「自进化」特性，不紧急
- **优先级**: `P2`
- **记录日期**: 2026-04-29
- **状态**: Parked

---

## Environment & Tooling

### FB-005 — Docker 卷权限问题

- **类型**: `Debt`
- **位置**: `docker-compose.yml`, `Dockerfile`
- **现象**: `FLOWBEAST_VECTOR_DIR` 在容器内创建时偶发 Root 权限冲突
- **目标**: Dockerfile 中指定 `USER arleszhang`
- **阻塞**: 需确认非 root 运行是否影响其他服务
- **优先级**: `P1`
- **记录日期**: 2026-04-29
- **状态**: Open

---

## Worklog

| Date | Action | FB-xxx |
|------|--------|--------|
| 2026-04-29 | 创建初始债单 | FB-001 ~ FB-005 |
