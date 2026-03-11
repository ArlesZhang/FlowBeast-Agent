#!/bin/bash
# 1. 进入项目根目录
cd ~/FlowBeast-p1/FlowBeast

# 2. 激活虚拟环境
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ 错误: 未找到虚拟环境，请先运行 uv sync"
    exit 1
fi

# 3. 打印欢迎信息
echo "========================================"
echo "    🌊 FlowBeast Agent 引擎已就绪！"
echo "    Python: $(python --version)"
echo "    状态: 🚀 环境已自动激活 (fbev)"
echo "----------------------------------------"
echo "    常用指令："
echo "    ./start_dev.sh   # 启动 API 服务器"
echo "    pytest           # 运行自动化测试"
echo "========================================"

# 4. 保持终端开启
exec bash
