import os
from typing import List
from loguru import logger
from flowbeast.fp3.schema import RetrievalResult, ViralMaterial

class PromptInjector:
    @staticmethod
    def inject_viral_context(base_prompt: str, viral_examples: List[RetrievalResult]) -> str:
        """
        核心注入逻辑：将检索到的爆款基因（FP3）缝合进 Base Prompt
        """
        if not viral_examples:
            logger.warning("⚠️ 未检索到爆款案例，将使用基础 Prompt 生成")
            return base_prompt

        examples_text = ""
        for i, res in enumerate(viral_examples):
            # 从检索结果中提取素材对象
            v = res.material 
            # 兼容你之前的 hook/pattern/emotion 逻辑
            # 如果素材里没分这么细，我们直接输出 content
            examples_text += f"\n[爆款案例 {i+1} | 匹配度: {res.score:.2f}]\n"
            examples_text += f"结构参考: {v.content}\n"
            if v.hooks:
                examples_text += f"核心 Hooks: {', '.join(v.hooks)}\n"

        # 组合最终发送给 LLM 的增强 Prompt
        enhanced_prompt = f"""
你现在是一位顶级短视频编剧，你的任务是根据给定的主题创作爆款漫剧脚本。

### 必须参考的爆款结构与基因：
{examples_text}

### 创作硬性要求：
- 开头3秒必须有强 Hook（黄金3秒原则）
- 剧情必须包含核心冲突，不能平铺直叙
- 至少包含 1 次身份或剧情的反转
- 输出格式必须为 JSON (符合 DramaScript 模式)

### 待处理主题：
{base_prompt}
"""
        return enhanced_prompt

# ============= 工具函数：供 seed_data.py 调用 =============

def add_new_material(content: str, style: str, hooks: list):
    """
    将爆款基因特征向量化并持久化到本地向量库
    """
    from flowbeast.fp3.embedding import embedder
    from flowbeast.fp3.store import store
    
    # 1. 封装数据对象
    material = ViralMaterial(
        content=content, 
        style=style, 
        hooks=hooks,
        metadata={"source": "seed_injection"}
    )
    
    # 2. 调用模型生成 Embedding
    logger.debug(f"正在为素材生成向量... 内容摘要: {content[:20]}...")
    vector = embedder.get_embedding(content)
    
    # 3. 存入 Store 并持久化到磁盘 (config.py 指定的路径)
    store.add(vector, material)
    store.save()
    logger.success(f"✅ 素材入库成功: [{style}]")

# 实例化对象供 builder 调用
injector = PromptInjector()
