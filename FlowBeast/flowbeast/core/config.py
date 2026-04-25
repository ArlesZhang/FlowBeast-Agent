import os
from pathlib import Path
from pydantic_settings import BaseSettings
from loguru import logger
from dotenv import load_dotenv

# ====================== 项目路径与 .env 加载 ======================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

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
    # 目录配置
    # ======================
    FLOWBEAST_OUTPUT_DIR: str = str(
        os.getenv("FLOWBEAST_OUTPUT_DIR", BASE_DIR / "flowbeast/data/outputs")
    )
    FLOWBEAST_MARKET_DIR: str = str(
        os.getenv("FLOWBEAST_MARKET_DIR", BASE_DIR / "flowbeast/market_material/raw_data")
    )
    FLOWBEAST_VECTOR_DIR: str = str(
        os.getenv("FLOWBEAST_VECTOR_DIR", BASE_DIR / "flowbeast/data/vector_store")
    )

    # ======================
    # FP3 专用路径（新增字段，解决 Pydantic 报错）
    # ======================
    
    # 这里先定义占位符，由 sanitize 进行动态对齐
    FP3_INDEX_PATH: Path = Path(FLOWBEAST_OUTPUT_DIR) / "vector_store" / "fp3/fp3.index"
    FP3_META_PATH: Path = Path(FLOWBEAST_OUTPUT_DIR) / "vector_store" / "fp3/fp3_meta.json"
    
    model_config = {
        "env_file": ENV_FILE,
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "case_sensitive": False,
    }

    @classmethod
    def sanitize(cls):
        """清理 + 创建目录 + 初始化 FP3 路径"""
        # 清理代理环境变量
        proxies = ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"]
        removed = [p for p in proxies if os.environ.pop(p, None)]
        if removed:
            logger.warning(f"🛡️ Cleared proxy envs: {removed}")

        instance = cls()

        output_base = Path(instance.FLOWBEAST_OUTPUT_DIR)


        # 创建基础目录
        for path_str in [
            instance.FLOWBEAST_OUTPUT_DIR,
            instance.FLOWBEAST_MARKET_DIR,
            instance.FLOWBEAST_VECTOR_DIR,
        ]:
            try:
                Path(path_str).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.warning(f"⚠️ 创建目录失败: {path_str} | {e}")

        # ====================== FP3 路径 ======================
        fp3_root = BASE_DIR / "flowbeast/data/vector_store"
        fp3_root.mkdir(parents=True, exist_ok=True)

        # 赋值给 Pydantic 字段
        instance.FP3_INDEX_PATH = fp3_root / "fp3.index"
        instance.FP3_META_PATH = fp3_root / "fp3_meta.json"

        return instance


# ====================== 全局实例 ======================
settings = Settings.sanitize()

# ====================== 导出变量（兼容旧代码） ======================
OPENAI_API_KEY = settings.OPENAI_API_KEY
QWEN_API_KEY = settings.QWEN_API_KEY

OUTPUTS_DIR = settings.FLOWBEAST_OUTPUT_DIR
VECTOR_STORE_PATH = settings.FLOWBEAST_VECTOR_DIR

# 明确导出 FP3 变量
FP3_INDEX_PATH = settings.FP3_INDEX_PATH
FP3_META_PATH = settings.FP3_META_PATH

logger.info(f"🚀 FlowBeast 配置加载成功 | Provider: {settings.MODEL_PROVIDER}")