# flowbeast/config.py
import os
from loguru import logger

class Config:
    # --- 模型治理 ---
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")  # openai / deepseek / anthropic
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
    
    # --- 环境治理 (解决握手报错) ---
    @staticmethod
    def sanitize_env():
        """清理干扰变量，确保 API 调用链路最优"""
        for key in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"]:
            os.environ.pop(key, None)
            os.environ.pop(key.lower(), None)
        logger.info("Environment sanitized: Proxy disabled for stable LLM handshake.")

# 初始化运行
Config.sanitize_env()
