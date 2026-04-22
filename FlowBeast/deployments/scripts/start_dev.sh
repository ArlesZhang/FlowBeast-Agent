#!/bin/bash
# 自动定位到脚本所在目录
cd "$(dirname "$0")"

# 1. 激活虚拟环境 (确保依赖隔离)
source .venv/bin/activate

# 2. 启动服务 (使用环境变量文件，保持代码纯净)
# --reload 方便开发，--env-file 自动加载 Key
exec uvicorn flowbeast.api.main:app --reload --port 8000 --env-file .env
