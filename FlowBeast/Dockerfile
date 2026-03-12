# 使用官方 Python 瘦版作为底座
FROM python:3.12-slim

# 安装 uv (直接从官方镜像拷贝二进制文件，极速！)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 设置工作目录
WORKDIR /app

# 1. 缓存依赖安装 (这是构建提速的核心)
# 先拷贝依赖声明文件，利用 Docker 的层缓存
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-dev

# 2. 拷贝源代码
COPY . .

# 3. 环境准备
# 确保使用 uv 创建的虚拟环境路径
ENV PATH="/app/.venv/bin:$PATH"

# 暴露 FastAPI 默认端口
EXPOSE 8000

# 启动脚本（使用我们之前写好的 start_dev.sh 的逻辑，但改为直接运行）
CMD ["uv", "run", "uvicorn", "flowbeast.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
