#!/bin/bash
set -e

echo "🚀 初始化 FlowBeast Docker 环境..."

# UID / GID  --写入身份 (保持解耦)
echo "USER_ID=$(id -u)" > .env.docker
echo "GROUP_ID=$(id -g)" >> .env.docker

# 创建目录   --物理创建两个隔离目录（如果不存在）
mkdir -p flowbeast/data/outputs
mkdir -p flowbeast/market_material/raw_data
mkdir -p flowbeast/data/vector_store

# 权限
chown -R $(id -u):$(id -g) flowbeast/data
chown -R $(id -u):$(id -g) flowbeast/market_material

chmod -R 755 flowbeast/data
chmod -R 755 flowbeast/market_material

echo "✅ 完成"
