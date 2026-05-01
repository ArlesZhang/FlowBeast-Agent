# 0002 - Embedding 统一接口设计

Date: 2026-04-29

## Status

Proposed

## 上下文

当前 `flowbeast/fp3/embedding.py` 中，不同 LLM 供应商的 embedding 实现方式不一致。

**问题**：
1. 代码重复，每个供应商需要单独的客户端配置
2. 维护成本高，新增供应商需修改 core 逻辑
3. 测试困难，无法 mock 统一接口

## 决策

创建统一的 `EmbeddingClient` 接口，抽象不同供应商的 embedding API。

### 设计草案

```python
from abc import ABC, abstractmethod

class EmbeddingClient(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

class GeminiEmbeddingClient(EmbeddingClient):
    def embed_text(self, text: str) -> List[float]:
        result = self.client.embed_content(...)
        return result['embedding']
```

## 后果

### 正面
- **单一职责**: `embedding.py` 只负责文本到向量的转换
- **易于测试**: 可 mock `EmbeddingClient` 接口
- **扩展性**: 新增供应商只需实现接口

### 负面
- **开发成本**: 需要重构现有代码
- **抽象开销**: 多一层间接调用
