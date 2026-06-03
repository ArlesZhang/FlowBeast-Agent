"""
FP3 Injector: enriches LLM prompts with retrieved viral pattern examples.

Role: Takes a base prompt + RAG-retrieved ViralUnit/ViralScript examples,
appends structured reference cases. ViralScript examples show hook_type
and audience_question for deeper anatomy display.

This is the ONLY point where FP3 connects to the drama generation pipeline
(called inside flowbeast/drama/generator.py).
"""


def inject_prompt(base_prompt: str, viral_examples: list) -> str:
    if not viral_examples:
        return base_prompt

    context = "\n### 爆款基因参考 (RAG 增强):\n"
    for i, ex in enumerate(viral_examples):
        if "hook_structure" in ex:  # ViralScript (stored as dict with sub-structure)
            hs = ex["hook_structure"]
            context += (
                f"【案例{i+1}】Hook: {ex['hook']} | 模式: {ex['pattern']}\n"
                f"  类型: {hs.get('hook_type', '')} | 观众疑问: {hs.get('audience_question', '')}\n"
            )
        else:
            context += f"【案例{i+1}】Hook: {ex['hook']} | 模式: {ex['pattern']}\n"

    return f"{context}\n\n### 创作任务：\n{base_prompt}"
