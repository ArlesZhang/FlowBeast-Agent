import os
from pydantic_settings import BaseSettings
from loguru import logger

class Settings(BaseSettings):
    # --- 模型治理 ---
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "openai")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o")
    
    # --- 算力地址 ---
    # 增加这个配置，确保代码能找到 Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # --- 环境治理 ---
    @classmethod
    def sanitize(cls):
        """一次性清理，解决容器内外的代理冲突"""
        proxies = ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"]
        removed = [p for p in proxies if os.environ.pop(p, None)]
        if removed:
            logger.warning(f"Detected and cleared proxy envs: {removed} to ensure local LLM handshake.")
        return cls()

# 在容器启动时初始化
settings = Settings.sanitize()
