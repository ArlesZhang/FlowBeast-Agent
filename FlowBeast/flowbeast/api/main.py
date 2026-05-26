from flowbeast.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# ==================== 初始化 ====================
app = FastAPI(title="FlowBeast", version="0.3.2")

# 跨域支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==================== 路由 ====================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "FlowBeast Engine",
    }


@app.get("/v1/user/info")
async def get_user_placeholder():
    return {"tier": "architect_preview", "status": "active"}
