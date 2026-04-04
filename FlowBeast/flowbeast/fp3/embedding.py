from flowbeast.core.config import settings

def embed_text(text: str):
    # 延迟导入已经闭环的 generator 里的 get_client
    from flowbeast.drama.generator import get_client
    client = get_client()
    
    provider = settings.MODEL_PROVIDER.lower()
    if provider == "gemini":
        result = client.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']
    elif provider == "qwen":
        import dashscope # 假设你已安装
        resp = dashscope.TextEmbedding.call(
            model=dashscope.TextEmbedding.Models.text_embedding_v2,
            input=text
        )
        return resp.output['embeddings'][0]['embedding']
    return [0.0] * 1536
