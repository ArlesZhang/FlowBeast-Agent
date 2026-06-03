# ============================================
# Stage 1: Development (used by .devcontainer)
# ============================================
FROM python:3.12-slim AS development

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for devcontainer
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install uv via pip (works better in China network than ghcr.io)
RUN pip install --no-cache-dir uv

WORKDIR /app

ENV UV_CACHE_DIR=/tmp/uv_cache
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV UV_HTTP_TIMEOUT=600

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Set ownership to vscode user
RUN chown -R $USERNAME:$USERNAME /app

ENV PATH="/app/.venv/bin:$PATH"

USER $USERNAME

EXPOSE 8000

CMD ["sleep", "infinity"]


# ============================================
# Stage 2: Production (default)
# ============================================
FROM python:3.12-slim AS production

# Install uv via pip (works better in China network than ghcr.io)
RUN pip install --no-cache-dir uv

WORKDIR /app

ENV UV_CACHE_DIR=/tmp/uv_cache
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV UV_HTTP_TIMEOUT=600

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-dev

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["sh", "-c", "uv run uvicorn flowbeast.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]