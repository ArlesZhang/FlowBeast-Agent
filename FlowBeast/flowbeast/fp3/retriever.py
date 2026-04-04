from typing import List
from flowbeast.fp3.schema import RetrievalResult

def inject_prompt(base_prompt: str, viral_examples: List[RetrievalResult]) -> str:
    """
    对接已经闭环的 generator.py 调用的函数名
    """
    if not viral_examples:
        return base_prompt

    context = "\n### 参考爆款案例：\n"
    for res in viral_examples:
        m = res.material
        context += f"- 结构参考: {m.content[:100]}... (匹配分: {res.score:.2f})\n"
    
    return f"{context}\n\n### 原始任务：\n{base_prompt}"
