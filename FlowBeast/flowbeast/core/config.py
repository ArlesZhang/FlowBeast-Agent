import os
from pathlib import Path
from pydantic_settings import BaseSettings
from loguru import logger
from dotenv import load_dotenv

# 1. 确保在 Pydantic 加载前，.env 已经进入环境变量
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings(BaseSettings):
    # --- 基础配置 ---
    APP_NAME: str = os.getenv("APP_NAME", "FlowBeast-Agent")
    APP_ENV: str = os.getenv("APP_ENV", "development")

    # --- 模型治理 (融合了你之前的逻辑) ---
    # 优先读取 ACTIVE_VENDOR，如果没有则回退到 MODEL_PROVIDER
    MODEL_PROVIDER: str = os.getenv("ACTIVE_VENDOR", os.getenv("MODEL_PROVIDER", "gemini"))
    MODEL_NAME: str = os.getenv("ACTIVE_MODEL", os.getenv("MODEL_NAME", "gemini-1.5-flash"))

    # --- 算力地址与 API Keys ---
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # --- 路径管理 ---
    DATA_SAVE_PATH: str = os.getenv("DATA_SAVE_PATH", "/app/market_material/raw_data")

    # --- 环境治理 (保留你的核心逻辑) ---
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
