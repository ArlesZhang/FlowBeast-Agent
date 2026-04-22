# 使用官方 Python 瘦版作为底座
FROM python:3.12-slim

# 安装 uv (直接从官方镜像拷贝二进制文件，极速！)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 设置工作目录
WORKDIR /app

# ✅ uv cache 改到可写目录
ENV UV_CACHE_DIR=/tmp/uv_cache

# 1. 缓存依赖安装 (这是构建提速的核心)
# 先拷贝依赖声明文件，利用 Docker 的层缓存
COPY pyproject.toml uv.lock ./

# 🟢 关键配置：注入清华源和超时时间
# UV_INDEX_URL 是 uv 识别镜像源的标准变量
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV UV_HTTP_TIMEOUT=600

# ✅ 只在 build 阶段安装依赖
RUN uv sync --frozen --no-cache --no-dev

# 2. 拷贝源代码
COPY . .

# 3. 环境准备
# 确保使用 uv 创建的虚拟环境路径
ENV PATH="/app/.venv/bin:$PATH"

# 暴露 FastAPI 默认端口
EXPOSE 8000

# 如果你现在主要是开发 API，用下面这行：
#CMD ["python", "-m", "uvicorn", "flowbeast.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 如果你现在只想跑通视频生成的 Pipeline，就把上面那行注释掉，用下面这行：
 CMD ["uv", "run","python", "-m", "flowbeast.drama.pipeline"]



# ❗关键：不要在 runtime 再执行 uv  --this is why I commented it out
#CMD ["uv", "run", "uvicorn", "flowbeast.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
