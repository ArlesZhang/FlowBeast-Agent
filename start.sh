#!/bin/bash
# 1. 进入项目目录（相对于脚本自身，容器内外都成立）
cd "$(dirname "$0")"

# 2. 激活虚拟环境
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ 错误: 未找到虚拟环境，请先运行 uv sync"
    exit 1
fi

# 3. 启动 FastAPI 服务器
echo "🌊 启动 FlowBeast API 服务器..."
exec bash start_dev.sh
