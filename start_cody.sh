#!/bin/bash
# =========================================
# DataCody Agent 一键启动脚本
# 功能：打开终端 → 进入项目 → 激活 venv → 提示就绪
# 使用：bash start_cody.sh   或   ./start_cody.sh
# =========================================

# 1. 进入项目根目录
cd ~/datacody-agent-project/datacody-agent

# 2. 激活虚拟环境
source ~/datacody-venv/bin/activate

# 3. 打印欢迎信息
echo "========================================"
echo "   DataCody Agent 已就绪！"
echo "   当前目录: $(pwd)"
echo "   Python: $(python --version)"
echo "   venv: $(which python)"
echo "   可用命令："
echo "     pytest -q          # 运行测试"
echo "     python main.py     # 运行入口"
echo "     bash start_cody.sh # 重新进入"
echo "   source ~/datacody-venv/bin/activate  #come in venv "
echo "========================================"

# 4. 启动交互式 shell
exec bash
