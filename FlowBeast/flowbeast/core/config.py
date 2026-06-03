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

# ====================== 模型路由映射 ======================

# .env 里定义 ACTIVE_VENDOR 和 ACTIVE_MODEL 作为一键切换入口，
# config.py 负责把它们解析为代码层使用的 MODEL_PROVIDER / MODEL_NAME。
def _resolve_active_vendor() -> str:
    """从 ACTIVE_VENDOR 解析当前使用的 provider。"""
    vendor = os.getenv("ACTIVE_VENDOR", "").lower().strip()
    if vendor:
        return vendor
    # 兼容旧变量名
    old = os.getenv("MODEL_PROVIDER", "").lower().strip()
    return old or "qwen"


def _resolve_active_model(vendor: str) -> str:
    """根据 vendor 解析对应的模型名。优先级：ACTIVE_MODEL > {VENDOR}_MODEL > 硬编码默认。"""
    active = os.getenv("ACTIVE_MODEL", "").strip()
    if active:
        return active

    vendor_upper = vendor.upper()
    env_key = f"{vendor_upper}_MODEL"
    vendor_model = os.getenv(env_key, "").strip()
    if vendor_model:
        return vendor_model

    defaults = {
        "qwen": "qwen-turbo",
        "openai": "gpt-4o-mini",
        "gemini": "gemini-1.5-flash",
        "deepseek": "deepseek-chat",
        "ollama": "llama3",
        "glm": "glm-4",
        "openrouter": "anthropic/claude-sonnet-4-20250514",
        "anthropic": "qwen3.6-plus",
    }
    return defaults.get(vendor, "qwen-turbo")


_active_vendor = _resolve_active_vendor()
_active_model = _resolve_active_model(_active_vendor)


def _resolve_embed_vendor() -> str:
    """解析 embedding provider。默认 ollama（本地离线无 API key），可设 EMBED_VENDOR 覆盖。"""
    vendor = os.getenv("EMBED_VENDOR", "").lower().strip()
    if vendor:
        return vendor
    return "ollama"


def _resolve_embed_model(vendor: str) -> str:
    active = os.getenv("EMBED_MODEL", "").strip()
    if active:
        return active
    defaults = {
        "gemini": "models/embedding-001",
        "openai": "text-embedding-3-small",
        "qwen": "text-embedding-v3",
        "ollama": "nomic-embed-text",
    }
    return defaults.get(vendor, "nomic-embed-text")


_active_embed_vendor = _resolve_embed_vendor()
_active_embed_model = _resolve_embed_model(_active_embed_vendor)


# ====================== 配置类 ======================
class Settings(BaseSettings):
    # ======================
    # 🧠 基础配置
    # ======================
    APP_NAME: str = "FlowBeast-Agent"
    APP_ENV: str = "development"

    # ======================
    # 🤖 LLM 模型配置（由 ACTIVE_VENDOR / ACTIVE_MODEL 驱动）
    # ======================
    MODEL_PROVIDER: str = _active_vendor
    MODEL_NAME: str = _active_model

    # ======================
    # 🧬 Embedding 配置（独立于 LLM，默认 gemini embedding-001）
    # ======================
    EMBED_PROVIDER: str = _active_embed_vendor
    EMBED_MODEL: str = _active_embed_model

    # ======================
    # 🔑 API Keys
    # ======================
    OPENAI_API_KEY: str = ""
    QWEN_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    DASHSCOPE_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    GLM_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # ======================
    # 🔌 本地模型
    # ======================
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    DASHSCOPE_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    ANTHROPIC_BASE_URL: str = ""

    # ======================
    # 目录配置
    # ======================
    FLOWBEAST_OUTPUT_DIR: str = str(
        os.getenv("FLOWBEAST_OUTPUT_DIR", BASE_DIR / "flowbeast/data/outputs")
    )
    FLOWBEAST_VECTOR_DIR: str = str(
        os.getenv("FLOWBEAST_VECTOR_DIR", BASE_DIR / "flowbeast/data/vector_store")
    )

    # ======================
    # FP3 专用路径
    # ======================
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
        proxies = ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"]
        removed = [p for p in proxies if os.environ.pop(p, None)]
        if removed:
            logger.warning(f"🛡️ Cleared proxy envs: {removed}")

        instance = cls()

        output_base = Path(instance.FLOWBEAST_OUTPUT_DIR)

        for path_str in [
            instance.FLOWBEAST_OUTPUT_DIR,
            instance.FLOWBEAST_VECTOR_DIR,
        ]:
            try:
                Path(path_str).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.warning(f"⚠️ 创建目录失败: {path_str} | {e}")

        fp3_root = output_base / "vector_store" / "fp3"
        fp3_root.mkdir(parents=True, exist_ok=True)

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

FP3_INDEX_PATH = settings.FP3_INDEX_PATH
FP3_META_PATH = settings.FP3_META_PATH

logger.info(
    f"🚀 FlowBeast 配置加载成功 | "
    f"LLM: {settings.MODEL_PROVIDER}/{settings.MODEL_NAME} | "
    f"Embed: {settings.EMBED_PROVIDER}/{settings.EMBED_MODEL}"
)
