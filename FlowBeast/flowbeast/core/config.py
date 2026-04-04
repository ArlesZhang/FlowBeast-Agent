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

# 定义 FP3 专用路径
FP3_DIR = Path(os.getenv("FLOWBEAST_OUTPUT_DIR", BASE_DIR / "flowbeast/data/outputs")) / "vector_store" / "fp3"
FP3_INDEX_PATH = FP3_DIR / "fp3.index"
FP3_META_PATH = FP3_DIR / "fp3_meta.json"

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

    # 兼容旧代码
    DATA_SAVE_PATH: str = ""

    # ======================
    # FP3 专用路径（新增字段，解决 Pydantic 报错）
    # ======================
    FP3_DIR: str = ""
    
    FP3_INDEX_PATH: Path = FP3_INDEX_PATH
    FP3_META_PATH: Path = FP3_META_PATH

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

        # 保证 DATA_SAVE_PATH 有值
        if not instance.DATA_SAVE_PATH:
            instance.DATA_SAVE_PATH = instance.FLOWBEAST_OUTPUT_DIR

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
        fp3_dir = Path(instance.DATA_SAVE_PATH) / "vector_store" / "fp3"
        fp3_dir.mkdir(parents=True, exist_ok=True)

        # 赋值给 Pydantic 字段
        instance.FP3_DIR = str(fp3_dir)
        instance.FP3_INDEX_PATH = str(fp3_dir / "fp3.index")
        instance.FP3_META_PATH = str(fp3_dir / "fp3_meta.json")

        logger.info(f"✅ FP3_DIR 已设置: {instance.FP3_DIR}")

        return instance


# ====================== 全局实例 ======================
settings = Settings.sanitize()

# ====================== 导出变量（兼容旧代码） ======================
OPENAI_API_KEY = settings.OPENAI_API_KEY
QWEN_API_KEY = settings.QWEN_API_KEY

DATA_SAVE_PATH = settings.DATA_SAVE_PATH
OUTPUTS_DIR = settings.FLOWBEAST_OUTPUT_DIR
VECTOR_STORE_PATH = settings.FLOWBEAST_VECTOR_DIR


logger.info(f"✅ 配置加载完成 | FP3_DIR = {FP3_DIR}")
