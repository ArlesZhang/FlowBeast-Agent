# 0002 - 统一 Embedding 接口设计

Date: 2026-04-29

## Status

Proposed

## 上下文

当前 embedding 实现有供应商特定代码重复。

## 决策

创建统一的 `EmbeddingClient` 接口。

## 后果

- 单一职责
- 易于测试
- 更好的扩展性
