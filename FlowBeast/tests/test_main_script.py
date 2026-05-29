#!/usr/bin/env python3
"""
独立脚本：快速验证 main 入口（不跑真实 LLM / 不全量写盘）。

用法（在仓库根目录 FlowBeast/）:
  uv run python scripts/test_main_script.py
  # 若已安装依赖: python scripts/test_main_script.py

退出码: 0 成功, 1 失败
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_main():
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    if "main" in sys.modules:
        del sys.modules["main"]
    return importlib.import_module("main")


def run_checks() -> bool:
    ok = True
    m = _load_main()

    # 1) 基础结构
    assert hasattr(m, "main") and callable(m.main), "main.main 不存在"
    assert "DramaPipeline" not in Path(PROJECT_ROOT / "main.py").read_text(
        encoding="utf-8"
    ), "main.py 不应再包含 DramaPipeline"

    # 2) mock 全链路
    mock_path = MagicMock()
    mock_path.name = "fp3.index"
    mock_path.exists.return_value = True
    result = {
        "run_id": "dry_run",
        "base_path": PROJECT_ROOT / "flowbeast" / "data" / "outputs" / "dry_run",
        "script_path": PROJECT_ROOT / "flowbeast" / "data" / "outputs" / "dry_run" / "script.json",
        "report_path": PROJECT_ROOT / "flowbeast" / "data" / "outputs" / "dry_run" / "production_report.json",
        "audio_path": PROJECT_ROOT / "flowbeast" / "data" / "outputs" / "dry_run" / "audio",
    }
    with patch.object(m, "FP3_INDEX_PATH", mock_path), patch.object(
        m, "run_full_pipeline", return_value=result
    ) as pipe, patch.object(m, "run_seeding") as seed:
        m.main()
    seed.assert_not_called()
    assert pipe.call_count == 1, "run_full_pipeline 应只调用一次"

    print("test_main_script: OK (mocked run_full_pipeline)")
    return True


def main() -> int:
    try:
        run_checks()
    except AssertionError as e:
        print(f"test_main_script: FAIL — {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"test_main_script: ERROR — {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
