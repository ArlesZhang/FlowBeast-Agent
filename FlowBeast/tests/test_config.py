#!/usr/bin/env python3
"""快速配置验证 - 运行: uv run pytest tests/test_config.py -q"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from flowbeast.core.config import (
    settings,
    FP3_INDEX_PATH,
    FP3_META_PATH,
    OUTPUTS_DIR,
    VECTOR_STORE_PATH
)

def test_paths():
    """验证所有路径设置正确"""
    print("Testing config paths...")

    # 测试 1: FP3 路径是 Path 对象
    assert hasattr(FP3_INDEX_PATH, 'parent'), "FP3_INDEX_PATH 应该是 Path 对象"
    assert hasattr(FP3_META_PATH, 'parent'), "FP3_META_PATH 应该是 Path 对象"
    print(f"✅ FP3_INDEX_PATH: {FP3_INDEX_PATH}")
    print(f"✅ FP3_META_PATH: {FP3_META_PATH}")

    # 测试 2: 目录存在
    assert FP3_INDEX_PATH.parent.exists(), f"FP3 目录应该存在: {FP3_INDEX_PATH.parent}"
    print(f"✅ FP3 目录存在")

    # 测试 3: Settings 有必需属性
    assert hasattr(settings, 'FLOWBEAST_OUTPUT_DIR')
    assert hasattr(settings, 'MODEL_PROVIDER')
    print(f"✅ Settings 属性正常")

    print("\n🎉 所有配置测试通过!")

if __name__ == "__main__":
    test_paths()
