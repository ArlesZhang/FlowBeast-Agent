"""
API: FastAPI server for FlowBeast.

Role: Web interface for topic-to-prompt-package generation.
Currently serves health check only; generation endpoint pending.

Workflow: POST /v1/generate {topic} → generate_script() → prompt_package.json
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# ==================== 初始化 ====================
app = FastAPI(title="FlowBeast", version="0.4.1")

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
