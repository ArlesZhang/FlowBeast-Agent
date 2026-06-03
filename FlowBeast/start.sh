#!/bin/bash
# 1. 进入 Python 项目子目录
cd /app/FlowBeast

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
