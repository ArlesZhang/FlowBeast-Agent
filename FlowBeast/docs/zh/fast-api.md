# 从零到一：为 FlowBeast 构建工业级 API 层

> AI Agent / Content Factory 系统的 API 架构设计与实践

---

## 目录

- [一、为什么 FlowBeast 必须有 API 层](#一why-flowbeast-needs-an-api-layer)
- [二、为什么是 FastAPI](#二why-fastapi)
- [三、FlowBeast API 架构设计](#三flowbeast-api-architecture)
- [四、项目目录结构](#四project-directory-structure)
- [五、第一个 API](#五first-api)
- [六、Pydantic 数据模型](#六pydantic-schemas)
- [七、异步架构](#七async-architecture)
- [八、Pipeline API](#八pipeline-api)
- [九、Agent API](#九agent-api)
- [十、Streaming](#十streaming)
- [十一、Background Tasks](#十一background-tasks)
- [十二、Queue / Celery](#十二queue--celery)
- [十三、WebSocket](#十三websocket)
- [十四、Auth](#十四auth)
- [十五、数据库设计](#十五database-design)
- [十六、RAG API](#十六rag-api)
- [十七、OpenAI 兼容 API](#十七openai-compatible-api)
- [十八、Docker 部署](#十八docker-deployment)
- [十九、Nginx 配置](#十九nginx-configuration)
- [二十、Kubernetes](#二十kubernetes)
- [二十一、 Observability](#二十一observability)
- [二十二、最佳实践](#二十二best-practices)
- [二十三、FlowBeast 推荐最终架构](#二十三flowbeast-recommended-architecture)

---

## 一、Why FlowBeast Needs an API Layer

### 1.1 当前状态 vs 未来目标

**你现在有：**
```python
# 单文件入口
python main.py

# 模块内调用
from flowbeast.drama.pipeline import run_full_pipeline
```

**你需要：**
| 能力 | 说明 |
|------|------|
| 前端调用 | Web UI / Dashboard |
| 外部服务调用 | SaaS / API 网关 |
| 多端调用 | Mobile / Web / VSCode Extension |
| Agent 编排 | 多 agent 协作 |
| Worker 调度 | Pipeline Queue |
| Streaming | LLM token 实时输出 |
| Async Jobs | 视频生成（30s-10min） |
| SDK | Python / JavaScript SDK |
| 微服务化 | 后续模块拆分 |

### 1.2 API 的本质

> **FastAPI 本质上是：把你的 AI 能力产品化**

---

## 二、Why FastAPI

### 2.1 Flask 的问题

- 没有类型系统
- Async 支持弱
- OpenAPI 文档不完整
- 不适合 AI streaming
- 大项目容易失控

### 2.2 Django 的问题

- ORM 绑定太深
- AI 系统不需要传统 MVC
- Async 不够优雅
- 不适合 agent pipeline

### 2.3 FastAPI 的优势

| 特性 | AI 系统价值 |
|------|------------|
| async 原生 | LLM 调用非阻塞 |
| StreamingResponse | Token 实时流式输出 |
| Pydantic | Prompt Schema 验证 |
| OpenAPI 自动生成 | SDK / 前端生成 |
| 类型安全 | Agent Contract |
| 高性能 | Inference Gateway |
| WebSocket | 实时 Agent 交互 |
| BackgroundTasks | 视频渲染后台任务 |
| Dependency Injection | Model/Router/Plugin |

**现代 AI Infra 生态：** vLLM, Ollama, OpenWebUI, LangServe, LlamaIndex

---

## 三、FlowBeast API Architecture

### 3.1 推荐目录结构

```
flowbeast/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app 入口
│   ├── deps.py              # 依赖注入
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── logging.py       # Request logging
│   │   ├── auth.py          # JWT Auth
│   │   ├── rate_limit.py    # Rate limiting
│   │   └── tracing.py       # OpenTelemetry
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py        # Health check
│   │   ├── fp3.py           # FP3 RAG API
│   │   ├── ip2.py           # IP2 Script Generation
│   │   ├── drama.py         # Drama Pipeline
│   │   ├── audio.py         # Audio Generation
│   │   ├── agent.py         # Agent Orchestration
│   │   └── auth.py          # User Auth
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── fp3.py           # FP3 schemas
│   │   ├── ip2.py           # IP2 schemas
│   │   ├── drama.py         # Drama schemas
│   │   ├── agent.py         # Agent schemas
│   │   └── common.py        # Common schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── fp3_service.py   # FP3 operations
│   │   ├── rag_service.py   # RAG operations
│   │   ├── ip2_service.py   # Script generation
│   │   ├── audio_service.py # Audio generation
│   │   └── video_service.py # Video generation
│   │
│   └── core/
│       ├── __init__.py
│       ├── config.py        # API config
│       ├── logging.py       # Structured logging
│       ├── security.py      # Security utils
│       └── exceptions.py    # Custom exceptions
│
├── fp3/                     # Viral Gene KB
├── ip2/                     # Script Generation
├── agents/                  # Agent system
├── execution/               # Task execution
├── drama_pipeline/          # Drama pipeline
└── core/                    # Core utilities
```

### 3.2 API 分层设计

```
┌─────────────────────────────────────────┐
│           API Layer (FastAPI)           │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │  Routes  │  │ Schemas  │  │ Middleware│
│  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────┘
            ↓                      ↓
┌─────────────────────────────────────────┐
│          Service Layer                  │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │  FP3     │  │  IP2     │  │ Drama  │ │
│  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────┘
            ↓                      ↓
┌─────────────────────────────────────────┐
│         Business Logic                  │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ LLM Call │  │  RAG     │  │ Audio  │ │
│  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────┘
```

---

## 四、Project Directory Structure

### 4.1 创建目录

```bash
mkdir -p flowbeast/api/middleware
mkdir -p flowbeast/api/routes
mkdir -p flowbeast/api/schemas
mkdir -p flowbeast/api/services
mkdir -p flowbeast/api/core
```

### 4.2 基础文件

**flowbeast/api/__init__.py**
```python
"""FlowBeast API Layer - Industrial Grade API for AI Content Factory"""
```

**flowbeast/api/routes/__init__.py**
```python
from flowbeast.api.routes import health, fp3, ip2, drama, audio

__all__ = ["health", "fp3", "ip2", "drama", "audio"]
```

---

## 五、First API

### 5.1 api/main.py

```python
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from flowbeast.api.routes import health, fp3, ip2, drama, audio
from flowbeast.api.core.config import settings
from flowbeast.api.core.logging import setup_logging

# Setup logging
setup_logging()

# Create app
app = FastAPI(
    title="FlowBeast API",
    version=settings.API_VERSION,
    description="AI-Driven Short-Drama Content Generation Engine",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(fp3.router, prefix="/api/v1", tags=["FP3"])
app.include_router(ip2.router, prefix="/api/v1", tags=["IP2"])
app.include_router(drama.router, prefix="/api/v1", tags=["Drama"])
app.include_router(audio.router, prefix="/api/v1", tags=["Audio"])


@app.get("/")
async def root():
    return {
        "name": "FlowBeast API",
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "flowbeast.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
```

### 5.2 启动服务

```bash
uvicorn flowbeast.api.main:app --reload --port 8000
```

访问：`http://localhost:8000/docs`

---

## 六、Pydantic Schemas

### 6.1 schemas/common.py

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, Dict, List
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class APIResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Any]


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    progress: float = Field(ge=0, le=1, default=0)
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ErrorResponse(BaseModel):
    error: str
    message: str
    code: int
```

### 6.2 schemas/fp3.py

```python
from pydantic import BaseModel
from typing import List
from .common import APIResponse


class ViralUnit(BaseModel):
    """FP3 爆款基因单元"""
    id: Optional[str] = None
    hook: str          # 开头钩子
    pattern: str       # 叙事模式
    emotion: List[str] # 情感标签
    viral_score: Optional[float] = None


class FP3SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    k: int = Field(default=2, ge=1, le=10)
    min_viral_score: Optional[float] = Field(default=0.5, ge=0, le=1)


class FP3SearchResponse(APIResponse):
    results: List[ViralUnit]


class FP3IndexRequest(BaseModel):
    viral_units: List[ViralUnit]


class FP3IndexResponse(APIResponse):
    indexed_count: int
```

### 6.3 schemas/ip2.py

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from .common import TaskResponse


class ScriptGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    genre: Optional[str] = Field(default="drama")
    hooks: Optional[List[str]] = Field(default_factory=list)
    fp3_enhanced: bool = Field(default=True)
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_scenes: int = Field(default=3, ge=1, le=10)


class ScriptGenerateResponse(TaskResponse):
    script_id: Optional[str] = None
    script: Optional[dict] = None  # Script object


class ScriptRewriteRequest(BaseModel):
    script_id: str
    rewrite_prompt: str = Field(..., min_length=1)
    keep_core_hook: bool = Field(default=True)


class ScriptRewriteResponse(TaskResponse):
    script_id: str
    original_hook: str
    new_hook: str
```

### 6.4 schemas/drama.py

```python
from pydantic import BaseModel
from typing import List, Optional


class SceneInput(BaseModel):
    hook: str
    conflict: str
    emotion_curve: List[str]
    summary: str
    dialogue: List[dict]


class DramaRenderRequest(BaseModel):
    script: dict
    audio_provider: str = Field(default="edge")
    voice: Optional[str] = None
```

---

## 七、Async Architecture

### 7.1 为什么必须 async

```python
# IO 密集型操作
await llm.generate()      # LLM 调用
await vector_db.search()  # 向量搜索
await audio.generate()    # 音频生成
```

### 7.2 FastAPI async 示例

```python
# api/routes/ip2.py

from fastapi import APIRouter
from flowbeast.api.services.ip2_service import generate_script_service

router = APIRouter()

@router.post("/generate", response_model=ScriptGenerateResponse)
async def generate_script(request: ScriptGenerateRequest):
    """生成短剧剧本（异步）"""
    result = await generate_script_service(request)
    return result


@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """查询任务状态"""
    status = await get_task_status_service(task_id)
    return status
```

---

## 八、Pipeline API

### 8.1 api/routes/drama.py

```python
from fastapi import APIRouter, BackgroundTasks
from flowbeast.api.schemas.drama import DramaRenderRequest
from flowbeast.api.services.audio_service import render_audio_pipeline

router = APIRouter()

@router.post("/render")
async def render_drama(
    request: DramaRenderRequest,
    background_tasks: BackgroundTasks
):
    """渲染戏剧（异步后台任务）"""
    task_id = str(uuid.uuid4())[:8]
    
    background_tasks.add_task(
        render_audio_pipeline,
        task_id=task_id,
        script=request.script,
        provider=request.audio_provider
    )
    
    return {
        "task_id": task_id,
        "status": "queued",
        "message": "Rendering started in background"
    }


@router.get("/status/{task_id}")
async def get_render_status(task_id: str):
    """获取渲染状态"""
    # Check task status from Redis/DB
    pass
```

### 8.2 使用 Pipeline

```bash
# 1. 创建渲染任务
curl -X POST http://localhost:8000/api/v1/drama/render \
  -H "Content-Type: application/json" \
  -d '{
    "script": { "title": "...", "scenes": [...] },
    "audio_provider": "edge"
  }'

# 2. 查询状态
curl http://localhost:8000/api/v1/drama/status/{task_id}
```

---

## 九、Agent API

### 9.1 api/routes/agent.py

```python
from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
from typing import List, Optional
import uuid

router = APIRouter()

class AgentMessage(BaseModel):
    agent_id: str
    role: str  # user / assistant / system
    content: str


class AgentRunRequest(BaseModel):
    topic: str
    agents: List[str] = ["hook_generator", "script_writer", "editor"]
    stream: bool = False


class AgentChatRequest(BaseModel):
    session_id: str
    message: str


@router.post("/run")
async def run_agent(request: AgentRunRequest):
    """运行 agent 网络"""
    session_id = str(uuid.uuid4())[:8]
    return {"session_id": session_id, "status": "started"}


@router.post("/chat")
async def agent_chat(request: AgentChatRequest):
    """与 agent 对话"""
    return {"session_id": request.session_id, "response": "..."}


# WebSocket for real-time agent interaction
@router.websocket("/ws/{session_id}")
async def agent_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        # Process and respond
        await websocket.send_json({"type": "response", "content": "..."})
```

---

## 十、Streaming

### 10.1 LLM Token Streaming

```python
# api/routes/ip2.py

from fastapi.responses import StreamingResponse
import asyncio

async def llm_stream(prompt: str):
    """流式生成 LLM 响应"""
    # Call LLM with streaming enabled
    async for token in llm_client.generate_stream(prompt):
        yield token


@router.post("/generate/stream")
async def generate_script_stream(request: ScriptGenerateRequest):
    """流式生成剧本"""
    prompt = build_prompt(request.topic)
    
    return StreamingResponse(
        llm_stream(prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.post("/generate/full")
async def generate_script_full(request: ScriptGenerateRequest):
    """完整响应（非流式）"""
    result = await generate_script_service(request)
    return result
```

### 10.2 SSE Event Streaming

```python
from fastapi.responses import JSONResponse
import asyncio

async def generate_events(task_id: str):
    """生成事件流"""
    yield f"data: {json.dumps({'event': 'started', 'task_id': task_id})}\n\n"
    
    yield f"data: {json.dumps({'event': 'stage_complete', 'stage': 'hook_generation', 'progress': 0.2})}\n\n"
    
    yield f"data: {json.dumps({'event': 'stage_complete', 'stage': 'script_writing', 'progress': 0.7})}\n\n"
    
    yield f"data: {json.dumps({'event': 'completed', 'task_id': task_id, 'result': {...}})}\n\n"


@router.get("/generate/events/{task_id}")
async def generate_events_stream(task_id: str):
    return StreamingResponse(
        generate_events(task_id),
        media_type="text/event-stream"
    )
```

---

## 十一、Background Tasks

### 11.1 FastAPI BackgroundTasks

```python
from fastapi import BackgroundTasks

def generate_video_task(task_id: str, script: dict):
    """视频生成后台任务"""
    # 1. 生成音频
    audio_files = generate_audio(script)
    
    # 2. 合成视频
    video_path = composite_video(audio_files)
    
    # 3. 保存结果
    save_result(task_id, video_path)


@router.post("/video/generate")
async def generate_video(
    request: ScriptGenerateRequest,
    background_tasks: BackgroundTasks
):
    task_id = str(uuid.uuid4())[:8]
    
    background_tasks.add_task(
        generate_video_task,
        task_id=task_id,
        script=request.script
    )
    
    return {"task_id": task_id, "status": "queued"}
```

### 11.2 限制

> ⚠️ FastAPI BackgroundTasks 适合轻量级任务，生产环境应使用 Celery/Dramatiq

---

## 十二、Queue / Celery

### 12.1 Celery 架构

```
FastAPI (API Layer)
    ↓
Redis Queue
    ↓
Celery Workers (Process Pool)
    ↓
Video Generation / Audio / LLM
```

### 12.2 Celery Setup

**flowbeast/api/core/queue.py**
```python
from celery import Celery
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "flowbeast_tasks",
    broker=redis_url,
    backend=redis_url,
    include=["flowbeast.api.tasks"],
)

# 配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
)
```

**flowbeast/api/tasks.py**
```python
from flowbeast.api.core.queue import celery_app
from flowbeast.api.services.video_service import generate_video_service
from loguru import logger


@celery_app.task(bind=True, max_retries=3)
def generate_video_task(self, task_id: str, script: dict):
    """视频生成任务"""
    try:
        result = generate_video_service(task_id, script)
        logger.success(f"Video generated: {task_id}")
        return result
    except Exception as exc:
        logger.error(f"Task {task_id} failed: {exc}")
        raise self.retry(exc=exc, countdown=60)  # Retry after 60s
```

**api/routes/drama.py**
```python
from flowbeast.api.tasks import generate_video_task

@router.post("/video/generate")
async def generate_video(request: ScriptGenerateRequest):
    task_id = str(uuid.uuid4())[:8]
    
    # Async task submission
    generate_video_task.delay(task_id, request.script)
    
    return {"task_id": task_id, "status": "queued"}
```

### 12.3 启动 Celery Worker

```bash
# API Server
uvicorn flowbeast.api.main:app --reload --port 8000

# Celery Worker
celery -A flowbeast.api.tasks.celery_app worker --loglevel=info

# Celery Beat (periodic tasks)
celery -A flowbeast.api.tasks.celery_app beat --loglevel=info
```

---

## 十三、WebSocket

### 13.1 Agent 实时交互

```python
# api/routes/agent.py

from fastapi import WebSocket, WebSocketDisconnect

active_connections: Dict[str, WebSocket] = {}


@router.websocket("/ws/agent/{session_id}")
async def agent_ws(websocket: WebSocket, session_id: str):
    """Agent WebSocket 交互"""
    await websocket.accept()
    active_connections[session_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "message":
                # Process message
                response = await process_agent_message(
                    session_id=session_id,
                    message=data["content"]
                )
                
                await websocket.send_json({
                    "type": "response",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
            
            elif data["type"] == "ping":
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        del active_connections[session_id]
        logger.info(f"Agent {session_id} disconnected")
```

### 13.2 前端示例

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/agent/123");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === "response") {
    console.log("Agent:", data.content);
  }
};

ws.send(JSON.stringify({
  type: "message",
  content: "写一个关于人工智能的爱情故事"
}));
```

---

## 十四、Auth

### 14.1 JWT Authentication

**flowbeast/api/core/security.py**
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

### 14.2 Dependency Injection

**flowbeast/api/deps.py**
```python
from fastapi import Header, HTTPException, Depends
from flowbeast.api.core.security import verify_token


async def get_current_user(authorization: str = Header(...)):
    """获取当前用户"""
    try:
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Not authenticated")
```

### 14.3 Protected Routes

```python
from fastapi import APIRouter, Depends
from flowbeast.api.deps import get_current_user

router = APIRouter()

@router.get("/user/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    return {"user_id": user["sub"], "email": user["email"]}


@router.post("/generate", dependencies=[Depends(get_current_user)])
async def generate(request: ScriptGenerateRequest):
    return {"result": "..."}
```

---

## 十五、Database Design

### 15.1 数据库选型

| 数据类型 | 推荐 DB | 说明 |
|---------|---------|------|
| Users | PostgreSQL | 关系型数据 |
| Tasks | PostgreSQL | 任务状态 |
| Vectors | Qdrant | 向量检索 |
| Cache | Redis | 缓存 |
| Analytics | ClickHouse | 分析查询 |
| Logs | Loki | 日志 |

### 15.2 SQLAlchemy Models

```python
# flowbeast/api/db/models.py

from sqlalchemy import Column, String, Integer, DateTime, JSON, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    task_type = Column(String)  # script_generation, audio, video
    status = Column(String)  # pending, processing, completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    progress = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
```

---

## 十六、RAG API

### 16.1 FP3 Search API

```python
# api/routes/fp3.py

from fastapi import APIRouter
from flowbeast.api.schemas.fp3 import FP3SearchRequest, FP3SearchResponse
from flowbeast.api.services.fp3_service import fp3_search_service

router = APIRouter()


@router.post("/fp3/search", response_model=FP3SearchResponse)
async def search_fp3(request: FP3SearchRequest):
    """搜索 FP3 爆款知识库"""
    results = await fp3_search_service(request.query, request.k, request.min_viral_score)
    
    return FP3SearchResponse(
        success=True,
        results=results
    )


@router.post("/fp3/index")
async def index_fp3(viral_units: List[ViralUnit]):
    """索引新的爆款基因"""
    count = await fp3_index_service(viral_units)
    return {"indexed_count": count}
```

### 16.2 FP3 Service

```python
# api/services/fp3_service.py

from flowbeast.fp3.retriever import FP3Retriever
from flowbeast.fp3.schema import ViralUnit


async def fp3_search_service(query: str, k: int = 2, min_score: float = 0.5) -> List[ViralUnit]:
    """搜索 FP3 知识库"""
    retriever = FP3Retriever()
    results = retriever.retrieve(query, k=k)
    
    # Filter by score if needed
    filtered = [r for r in results if r.viral_score >= min_score]
    
    return filtered
```

### 16.3 使用示例

```bash
curl -X POST http://localhost:8000/api/v1/fp3/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "逆袭：被开除后的百亿首富",
    "k": 2,
    "min_viral_score": 0.5
  }'
```

---

## 十七、OpenAI Compatible API

### 17.1 为什么需要

让 FlowBeast 兼容 OpenAI API 格式，可以接入：
- OpenWebUI
- LangChain
- Claude Code
- Cursor
- Agent frameworks

### 17.2 实现

```python
# api/routes/openai_compat.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "flowbeast-v1"
    messages: List[ChatMessage]
    temperature: float = 0.7
    stream: bool = False


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[dict]
    usage: dict


@router.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """OpenAI 兼容的聊天接口"""
    # Extract prompt from messages
    prompt = "\n".join([m.content for m in request.messages if m.role == "user"])
    
    # Call FlowBeast LLM
    result = await llm_generate(prompt)
    
    return ChatCompletionResponse(
        id=str(uuid.uuid4()),
        created=int(datetime.now().timestamp()),
        model="flowbeast-v1",
        choices=[{
            "index": 0,
            "message": {"role": "assistant", "content": result},
            "finish_reason": "stop"
        }],
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    )


# Streaming version
@router.post("/v1/chat/completions_stream")
async def chat_completions_stream(request: ChatCompletionRequest):
    """流式 OpenAI 兼容接口"""
    prompt = "\n".join([m.content for m in request.messages if m.role == "user"])
    
    async def stream():
        async for token in llm_stream(prompt):
            yield f"data: {json.dumps({'choices': [{'delta': {'content': token}}]})}\n\n"
    
    return StreamingResponse(stream(), media_type="text/event-stream")
```

### 17.3 使用示例

```bash
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flowbeast-v1",
    "messages": [
      {"role": "user", "content": "写一个关于人工智能的爱情故事"}
    ]
  }'
```

---

## 十八、Docker Deployment

### 18.1 Dockerfile

```dockerfile
# FlowBeast API Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies with uv
RUN pip install --no-cache-dir uv && \
    uv sync --frozen

# Copy application code
COPY flowbeast ./flowbeast
COPY .env .env

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/v1/health || exit 1

# Run server
CMD ["uvicorn", "flowbeast.api.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8080", \
     "--workers", "4"]
```

### 18.2 docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8080"
    environment:
      - MODEL_PROVIDER=qwen
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - ./flowbeast/data:/app/flowbeast/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  celery_worker:
    build: .
    command: celery -A flowbeast.api.tasks.celery_app worker --loglevel=info
    environment:
      - MODEL_PROVIDER=qwen
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    restart: unless-stopped

  celery_beat:
    build: .
    command: celery -A flowbeast.api.tasks.celery_app beat --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    restart: unless-stopped

volumes:
  redis_data:
```

### 18.3 启动

```bash
# Build and start
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f api
```

---

## 十九、Nginx Configuration

### 19.1 Basic Configuration

```nginx
upstream flowbeast_api {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.flowbeast.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.flowbeast.com;

    ssl_certificate /etc/ssl/certs/flowbeast.com.crt;
    ssl_certificate_key /etc/ssl/private/flowbeast.com.key;

    # Gzip compression
    gzip on;
    gzip_types application/json text/plain;

    # Proxy settings
    location / {
        proxy_pass http://flowbeast_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://flowbeast_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

---

## 二十、Kubernetes

### 20.1 Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flowbeast-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flowbeast-api
  template:
    metadata:
      labels:
        app: flowbeast-api
    spec:
      containers:
      - name: api
        image: flowbeast/api:latest
        ports:
        - containerPort: 8080
        env:
        - name: MODEL_PROVIDER
          value: "qwen"
        - name: DASHSCOPE_API_KEY
          valueFrom:
            secretKeyRef:
              name: flowbeast-secrets
              key: dashscope-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1"
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: flowbeast-api
spec:
  selector:
    app: flowbeast-api
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### 20.2 Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flowbeast-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.flowbeast.com
    secretName: flowbeast-tls
  rules:
  - host: api.flowbeast.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flowbeast-api
            port:
              number: 80
```

---

## 二十一、Observability

### 21.1 Logging

```python
# flowbeast/api/core/logging.py

import sys
from loguru import logger

def setup_logging():
    """Setup structured logging"""
    logger.remove()
    
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        level="INFO",
        backtrace=True,
        diagnose=True,
    )
    
    logger.add(
        "logs/api_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="7 days",
        encoding="utf-8",
        level="DEBUG",
    )


# Example usage
logger.info("API request received", method="POST", path="/api/v1/generate", user_id="123")
logger.success("Script generated", script_id="abc123", model="qwen-turbo", latency_ms=2350)
```

### 21.2 Metrics (Prometheus)

```python
# flowbeast/api/middleware/tracing.py

from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI

def setup_metrics(app: FastAPI):
    """Setup Prometheus metrics"""
    instrumentator = Instrumentator()
    instrumentator.add().instrument(app)
    
    @instrumentator.expose(
        app,
        endpoint="/metrics",
        include_in_schema=False,
        tags=["System"]
    ):
        pass
```

### 21.3 Tracing (OpenTelemetry)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

tracer = trace.get_tracer(__name__)

# Usage
with tracer.start_as_current_context("script-generation"):
    # Generation logic
    pass
```

---

## 二十二、Best Practices

### 22.1 Error Handling

```python
# flowbeast/api/core/exceptions.py

from fastapi import HTTPException


class FlowBeastError(HTTPException):
    """Base exception for FlowBeast"""
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class LLMError(FlowBeastError):
    def __init__(self, detail: str = "LLM service error"):
        super().__init__(detail=detail, status_code=503)


class FP3NotFoundError(FlowBeastError):
    def __init__(self, detail: str = "FP3 data not found"):
        super().__init__(detail=detail, status_code=404)
```

### 22.2 Rate Limiting

```python
# flowbeast/api/middleware/rate_limit.py

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Usage
@router.post("/generate")
@limiter.limit("10/minute")
async def generate(request: ScriptGenerateRequest):
    return {"result": "..."}
```

### 22.3 Request Validation

```python
from fastapi import HTTPException
from pydantic import ValidationError


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Request validation failed",
            "details": exc.errors()
        }
    )


@app.exception_handler(FlowBeastError)
async def flowbeast_exception_handler(request: Request, exc: FlowBeastError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "message": exc.detail}
    )
```

---

## 二十三、FlowBeast Recommended Architecture

### 23.1 Phase 1: Current State

```
┌─────────────────────────────────────────┐
│          FastAPI (v1.0)                 │
│  ┌──────────┐  ┌──────────┐            │
│  │ Routes   │  │ Schemas  │            │
│  └──────────┘  └──────────┘            │
│           ↓      ↓                     │
│  ┌────────────────────────┐            │
│  │   Services Layer       │            │
│  │  FP3 / IP2 / Drama     │            │
│  └────────────────────────┘            │
└─────────────────────────────────────────┘
           ↓         ↓
    ┌─────────┐  ┌──────────┐
    │ LLM API │  │ FP3 KB   │
    └─────────┘  └──────────┘
```

### 23.2 Phase 2: Async Processing

```
┌─────────────────────────────────────────┐
│         FastAPI (API Gateway)           │
│         Redis (Task Queue)              │
└─────────────────────────────────────────┘
              ↓
    ┌────────────────┐
    │  Celery Worker │
    │  (Pool of N)   │
    └────────────────┘
              ↓
    ┌────────────────┐
    │  Background    │
    │  Tasks         │
    │  Video/Audio   │
    └────────────────┘
```

### 23.3 Phase 3: Microservices

```
┌─────────────────────────────────────────┐
│       API Gateway (Traefik)             │
└─────────────────────────────────────────┘
              ↓
    ┌──────────────────────────┐
    │  Microservices Cluster   │
    │  ┌────────┐ ┌────────┐  │
    │  │ Script │ │ Audio  │  │
    │  │ Service│ │ Service│  │
    │  └────────┘ └────────┘  │
    └──────────────────────────┘
              ↓
    ┌──────────────────────────┐
    │     Shared Services      │
    │  ┌────────┐ ┌────────┐  │
    │  │  LLM   │ │  FP3   │  │
    │  │  Pool  │ │  KB    │  │
    │  └────────┘ └────────┘  │
    └──────────────────────────┘
```

### 23.4 Recommended Stack

| Component | Recommendation |
|-----------|----------------|
| API Framework | FastAPI |
| Server | Uvicorn / Gunicorn |
| Queue | Redis + Celery |
| DB | PostgreSQL + Qdrant |
| Cache | Redis |
| Auth | JWT (python-jose) |
| Monitoring | Prometheus + Grafana |
| Logging | Structured (loguru) |
| Tracing | OpenTelemetry |
| Deployment | Docker + Kubernetes |
| Gateway | Nginx / Traefik |

---

## 快速开始路线图

### Week 1: 基础架构

1. 创建 `flowbeast/api/` 目录结构
2. 实现 `GET /api/v1/health`
3. 实现 `POST /api/v1/fp3/search`
4. 实现 `POST /api/v1/ip2/generate`

### Week 2: 进阶特性

1. 添加 Streaming Response
2. 实现 Background Tasks
3. 集成 Redis Queue
4. 添加 Auth (JWT)

### Week 3: 生产准备

1. Dockerize API
2. Setup Prometheus metrics
3. Configure Nginx
4. Add OpenAI-compatible API

### Week 4: 完整系统

1. WebSocket Agent
2. Kubernetes deployment
3. SDK generation
4. Documentation

---

## 相关文档

- [架构文档](architecture.md) - 系统架构详解
- [FP3 知识库](fp3/README.md) - 爆款基因检索系统
- [快速开始](getting-started.md) - 项目安装与配置
