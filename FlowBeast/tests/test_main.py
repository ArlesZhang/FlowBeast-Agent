"""
验证 main 入口在「run_full_pipeline + FP3 种子」逻辑下可运行、可 mock。

运行（在项目根 FlowBeast/ 下）:
  uv run pytest tests/test_main.py -q
  # 或
  python -m pytest tests/test_main.py -q
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def import_main():
    """保证只加载一次 main，且把项目根放在 sys.path 最前。"""
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    if "main" in sys.modules:
        del sys.modules["main"]
    m = importlib.import_module("main")
    return m


def test_main_module_imports_flowbeast(import_main):
    """main 能完成导入（无 DramaPipeline / 无多余 asyncio）。"""
    m = import_main
    assert hasattr(m, "main")
    assert callable(m.main)
    assert hasattr(m, "run_full_pipeline")
    assert hasattr(m, "FP3_INDEX_PATH")


def test_main_skips_seeding_and_calls_pipeline_when_index_exists(import_main):
    m = import_main
    mock_path = MagicMock()
    mock_path.name = "fp3.index"
    mock_path.exists.return_value = True
    result = {
        "run_id": "test_run",
        "base_path": Path("/tmp/fb"),
        "script_path": Path("/tmp/fb/script.json"),
        "report_path": Path("/tmp/fb/report.json"),
        "audio_path": Path("/tmp/fb/audio"),
    }
    with patch.object(m, "FP3_INDEX_PATH", mock_path), patch.object(
        m, "run_full_pipeline", return_value=result
    ) as mock_pipe, patch.object(m, "run_seeding") as mock_seed, patch.object(
        sys, "argv", ["main.py"]
    ):
        m.main()
    mock_seed.assert_not_called()
    mock_pipe.assert_called_once()
    (topic_arg,) = mock_pipe.call_args[0]
    assert "程序员" in topic_arg


def test_main_runs_seeding_when_index_missing(import_main):
    m = import_main
    mock_path = MagicMock()
    mock_path.name = "fp3.index"
    mock_path.exists.return_value = False
    result = {
        "run_id": "after_seed",
        "base_path": Path("/tmp/x"),
        "script_path": Path("/tmp/x/script.json"),
        "report_path": Path("/tmp/x/report.json"),
        "audio_path": Path("/tmp/x/audio"),
    }
    with patch.object(m, "FP3_INDEX_PATH", mock_path), patch.object(
        m, "run_full_pipeline", return_value=result
    ) as mock_pipe, patch.object(m, "run_seeding") as mock_seed, patch.object(
        sys, "argv", ["main.py"]
    ):
        m.main()
    mock_seed.assert_called_once()
    mock_pipe.assert_called_once()


def test_main_handles_pipeline_failure(import_main):
    m = import_main
    mock_path = MagicMock()
    mock_path.name = "fp3.index"
    mock_path.exists.return_value = True
    with patch.object(m, "FP3_INDEX_PATH", mock_path), patch.object(
        m, "run_full_pipeline", return_value=None
    ), patch.object(m, "run_seeding") as mock_seed, patch.object(
        sys, "argv", ["main.py"]
    ):
        m.main()
    mock_seed.assert_not_called()


def test_no_drama_pipeline_name_in_source():
    """防止再次混进已删除的 DramaPipeline。"""
    text = (PROJECT_ROOT / "main.py").read_text(encoding="utf-8")
    assert "DramaPipeline" not in text
    assert "execute_workflow" not in text
    assert "run_full_pipeline" in text


def test_main_accepts_topic_flag(import_main):
    """main 支持 --topic 参数，传入自定义主题。"""
    m = import_main
    mock_path = MagicMock()
    mock_path.name = "fp3.index"
    mock_path.exists.return_value = True
    result = {
        "run_id": "topic_test",
        "base_path": Path("/tmp/fb"),
        "script_path": Path("/tmp/fb/script.json"),
        "report_path": Path("/tmp/fb/report.json"),
        "audio_path": Path("/tmp/fb/audio"),
    }
    with patch.object(m, "FP3_INDEX_PATH", mock_path), patch.object(
        m, "run_full_pipeline", return_value=result
    ) as mock_pipe, patch.object(m, "run_seeding"), patch.object(
        sys, "argv", ["main.py", "--topic", "custom topic here"]
    ):
        m.main()
    mock_pipe.assert_called_once()
    (topic_arg,) = mock_pipe.call_args[0]
    assert topic_arg == "custom topic here"
