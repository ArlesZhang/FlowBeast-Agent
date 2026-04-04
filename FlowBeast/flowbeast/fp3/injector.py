def inject_prompt(base_prompt: str, viral_examples: list) -> str:
    if not viral_examples:
        return base_prompt

    context = "\n### 爆款基因参考 (RAG 增强):\n"
    for i, ex in enumerate(viral_examples):
        context += f"【案例{i+1}】Hook: {ex['hook']} | 模式: {ex['pattern']}\n"
    
    return f"{context}\n\n### 创作任务：\n{base_prompt}"
