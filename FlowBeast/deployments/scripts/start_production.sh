#!/bin/bash
echo "正在启动 FlowBeast 生产环境（docker compose）..."

# 一键启动全部服务：API + PostgreSQL + Redis（未来加）
docker compose -f deployments/docker/docker-compose.yml up -d --build

echo "FlowBeast Commercial 已上线 → http://localhost:8000/docs"
echo "Swagger 文档：http://localhost:8000/docs"
echo "健康检查：   http://localhost:8000/health"
