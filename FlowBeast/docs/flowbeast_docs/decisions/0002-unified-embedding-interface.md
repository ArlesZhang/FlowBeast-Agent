# 0002 - Embedding 统一接口设计

Date: 2026-04-29

## Status

Proposed

## 上下文 (Context)

当前 `flowbeast/fp3/embedding.py` 中，不同 LLM 供应商的 embedding 实现方式不一致：

- **Gemini**: 使用 `client.embed_content()` (v0.2.0 已有)
- **Qwen/DashScope**: 待接入，返回零向量占位
- **OpenAI**: 待接入

**问题**：
1. 代码重复，每个供应商需要单独的客户端配置
2. 维护成本高，新增供应商需修改 core 逻辑
3. 测试困难，无法 mock 统一接口

## 决策 (Decision)

创建统一的 `EmbeddingClient` 接口，抽象不同供应商的 embedding API。

### 设计草案

```python
# flowbeast/core/embedding.py

from abc import ABC, abstractmethod
from typing import List

class EmbeddingClient(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass

# 供应商具体实现
class GeminiEmbeddingClient(EmbeddingClient):
    def __init__(self, api_key: str):
        self.client = build_gemini_client(api_key)
    
    def embed_text(self, text: str) -> List[float]:
        result = self.client.embed_content(...)
        return result['embedding']

class QwenEmbeddingClient(EmbeddingClient):
    # ... 实现
```

### 使用方式

```python
# flowbeast/fp3/embedding.py

from flowbeast.core.config import settings
from flowbeast.core.embedding import get_embedding_client

client = get_embedding_client(settings.MODEL_PROVIDER)
vector = client.embed_text("测试文本")
```

## 后果 (Consequences)

### 正面
- **单一职责**: `embedding.py` 只负责文本到向量的转换
- **易于测试**: 可 mock `EmbeddingClient` 接口
- **扩展性**: 新增供应商只需实现接口，无需修改 core 逻辑

### 负面
- **开发成本**: 需要重构现有代码
- **抽象开销**: 多一层间接调用

### 权衡
- 选择接口抽象而非条件分支: 随着供应商增加，条件分支会变得难以维护
- 拒绝 LiteLLM: LiteLLM 主要针对 completion API，embedding 支持有限

## 考虑的备选方案

### 备选方案 1: 继续使用条件分支

```python
# 当前方式
if provider == "gemini":
    # ...
elif provider == "qwen":
    # ...
```

**为什么拒绝**: 随着供应商增加，`embedding.py` 会变成难以维护的巨型函数。

### 备选方案 2: 使用 LiteLLM

**为什么拒绝**: LiteLLM 的 embedding API 支持不如 completion API 完善，且增加了一个外部依赖。

## 引用 (References)

- [相关代码](../01-tech-debt.md#fb-002--多供应商-embedding-占位)
- [RFC 讨论](https://github.com/orgs/FlowBeast/discussions/42)
