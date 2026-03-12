from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from flowbeast.agent.compiler import compile_workflow  # 对应重构的编译器
from flowbeast.agent.codegen import generate_code      # 对应重构的生成器
from flowbeast.config import settings                    # 对应环境治理
from pydantic import BaseModel
from loguru import logger

# ==================== 初始化 ====================
app = FastAPI(title="FlowBeast Intelligent API", version="0.2.0")

# 保持竞争力：跨域支持
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# ==================== 模型定义 ====================
class TaskRequest(BaseModel):
    prompt: str
    stream: bool = False

# ==================== 核心路由 ====================

@app.post("/v1/execute")
async def execute_task(request: TaskRequest):
    """
    MVP 核心：接收自然语言，返回 IR 和生成的 Python 代码
    """
    logger.info(f"Received NL Task: {request.prompt}")
    
    # 1. 编译 (NL -> IR)
    ir = compile_workflow(request.prompt)
    
    # 2. 生成 (IR -> Python)
    generated_python = generate_code(ir)
    
    return {
        "status": "success",
        "model": settings.MODEL_NAME,
        "payload": {
            "ir": ir,
            "code": generated_python
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "service": "FlowBeast Engine",
        "device": "Düsseldorf-Node-01" # 增加点个性
    }

# ==================== 商业占位 (未来扩展) ====================
# 这里可以留一个接口，但暂时不加 Depends 鉴权，方便你现在调试
@app.get("/v1/user/info")
async def get_user_placeholder():
    return {"tier": "architect_preview", "status": "active"}
