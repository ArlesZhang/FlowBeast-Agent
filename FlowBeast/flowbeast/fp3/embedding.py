from flowbeast.core.config import settings

# TODO(arles,Stub #1): 1.Support asynchronous batch embedding  + 2.这里的 embedding 暂时用 0 向量占位，等接入 Qwen 后替换
def embed_text(text: str):
    """延迟导入，确保不发生循环引用"""
    from flowbeast.drama.generator import get_client
    client = get_client()
    
    provider = settings.MODEL_PROVIDER.lower()
    if provider == "gemini":
        # 使用你 v0.2.0 已有的 client 配置
        result = client.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']
    
    # 兜底：如果配置还没好，返回 Mock
    return [0.0] * 1536

def embed_unit(unit):
    """将 ViralUnit 转化为可嵌入的文本"""
    text = f"hook: {unit.hook} pattern: {unit.pattern} emotion: {' '.join(unit.emotion)}"
    return embed_text(text)
