import os
from pathlib import Path

from pydantic_settings import BaseSettings
from loguru import logger
from dotenv import load_dotenv

# ====================== 项目路径与 .env 加载 ======================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

# 提前手动加载 .env（保证 os.getenv 和 pydantic 都能读到）
load_dotenv(dotenv_path=ENV_FILE, override=True)

if not ENV_FILE.exists():
    logger.warning(f"⚠️ .env 文件不存在！路径: {ENV_FILE}")

# ====================== 配置类 ======================
class Settings(BaseSettings):
    # --- 基础配置 ---
    APP_NAME: str = "FlowBeast-Agent"
    APP_ENV: str = "development"

    # --- 模型相关 ---
    MODEL_PROVIDER: str = "qwen"
    MODEL_NAME: str = "qwen-turbo"

    # --- API Keys ---
    OPENAI_API_KEY: str = ""
    QWEN_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    DASHSCOPE_API_KEY: str = ""

    # --- 其他配置 ---
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"

    # --- 路径配置（动态，推荐） ---
    DATA_SAVE_PATH: str = str(BASE_DIR / "flowbeast/data/outputs")

    # ====================== Pydantic v2 推荐写法 ======================
    model_config = {
        "env_file": ENV_FILE,
        "env_file_encoding": "utf-8",
        "extra": "ignore",           # 忽略 .env 中未声明的字段
        "case_sensitive": False,
    }

    @classmethod
    def sanitize(cls):
        """清理代理环境变量，防止干扰本地 LLM 调用"""
        proxies = ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                   "http_proxy", "https_proxy", "all_proxy"]
        removed = [p for p in proxies if os.environ.pop(p, None)]
        if removed:
            logger.warning(f"🛡️ Cleared proxy envs: {removed} to ensure local LLM handshake.")
        return cls()


# ====================== 全局实例 ======================
settings = Settings.sanitize()

# ====================== 导出常用变量（保持兼容） ======================
OPENAI_API_KEY = settings.OPENAI_API_KEY
QWEN_API_KEY = settings.QWEN_API_KEY
DATA_SAVE_PATH = settings.DATA_SAVE_PATH
