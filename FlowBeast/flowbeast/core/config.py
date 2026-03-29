import os
from pathlib import Path

from pydantic_settings import BaseSettings
from loguru import logger
from dotenv import load_dotenv

# ====================== 项目路径与 .env 加载 ======================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

# 提前加载 .env
load_dotenv(dotenv_path=ENV_FILE, override=True)

if not ENV_FILE.exists():
    logger.warning(f"⚠️ .env 文件不存在！路径: {ENV_FILE}")


# ====================== 配置类 ======================
class Settings(BaseSettings):
    # ======================
    # 🧠 基础配置
    # ======================
    APP_NAME: str = "FlowBeast-Agent"
    APP_ENV: str = "development"

    # ======================
    # 🤖 模型配置
    # ======================
    MODEL_PROVIDER: str = "qwen"
    MODEL_NAME: str = "qwen-turbo"

    # ======================
    # 🔑 API Keys
    # ======================
    OPENAI_API_KEY: str = ""
    QWEN_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    DASHSCOPE_API_KEY: str = ""

    # ======================
    # 🔌 本地模型
    # ======================
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"

    # ======================
    # 🎬 内容生产数据（核心输出）
    # ======================
    FLOWBEAST_OUTPUT_DIR: str = str(
        os.getenv(
            "FLOWBEAST_OUTPUT_DIR",
            BASE_DIR / "flowbeast/data/outputs"
        )
    )

    # ======================
    # 📊 商业素材数据（独立隔离）
    # ======================
    FLOWBEAST_MARKET_DIR: str = str(
        os.getenv(
            "FLOWBEAST_MARKET_DIR",
            BASE_DIR / "flowbeast/market_material/raw_data"
        )
    )

    # ======================
    # 🧠 向量库 / FP2（未来扩展）
    # ======================
    FLOWBEAST_VECTOR_DIR: str = str(
        os.getenv(
            "FLOWBEAST_VECTOR_DIR",
            BASE_DIR / "flowbeast/data/vector_store"
        )
    )

    # ======================
    # ⚠️ 兼容旧代码（关键！）
    # ======================
    DATA_SAVE_PATH: str = FLOWBEAST_OUTPUT_DIR

    # ======================
    # Pydantic v2 配置
    # ======================
    model_config = {
        "env_file": ENV_FILE,
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "case_sensitive": False,
    }

    # ======================
    # 初始化钩子
    # ======================
    @classmethod
    def sanitize(cls):
        """清理代理 + 初始化目录"""
        proxies = [
            "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
            "http_proxy", "https_proxy", "all_proxy"
        ]

        removed = [p for p in proxies if os.environ.pop(p, None)]
        if removed:
            logger.warning(
                f"🛡️ Cleared proxy envs: {removed} to ensure local LLM handshake."
            )

        instance = cls()

        # ======================
        # 📁 自动创建目录（关键）
        # ======================
        for path in [
            instance.FLOWBEAST_OUTPUT_DIR,
            instance.FLOWBEAST_MARKET_DIR,
            instance.FLOWBEAST_VECTOR_DIR,
        ]:
            try:
                Path(path).mkdir(parents=True, exist_ok=True)
            except PermissionError:
                logger.warning(f"⚠️ 无法创建目录（权限问题）: {path}")

        return instance


# ====================== 全局实例 ======================
settings = Settings.sanitize()

# ======================
# 🔥 导出常用变量（兼容旧代码）
# ======================
OPENAI_API_KEY = settings.OPENAI_API_KEY
QWEN_API_KEY = settings.QWEN_API_KEY

# 旧代码仍然能跑
DATA_SAVE_PATH = settings.DATA_SAVE_PATH

# 新架构推荐使用
OUTPUTS_DIR = settings.FLOWBEAST_OUTPUT_DIR
MARKET_DATA_PATH = settings.FLOWBEAST_MARKET_DIR
VECTOR_STORE_PATH = settings.FLOWBEAST_VECTOR_DIR
