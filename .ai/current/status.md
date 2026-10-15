# Current Status

> **⚠️ 商业化定位（2026-10-15）。** 见 [commercialization_playbook.zh.md](commercialization_playbook.zh.md)。
>
> 市场反馈表明，静态语料壁垒、低价抽取服务、特定品牌命名以及提示词包等四条早期创业路径已被证伪。
> AI 2.0 时代轻资产模式已难以为继，从业者需要转向更深层的系统级工作流集成与业务结果交付。
>
> **唯一验收标准：有真实付费证据。**

**Last updated:** 2026-10-15（项目瘦身：删除已证伪方向的代码与文档）

---

## 这次删掉了什么

| 删除项 | 原因 |
|--------|------|
| `flowbeast/vto/`（GRAFT 算子） | VTO 算子路线证伪；且它传的是硬编码常量，不是检索到的结构 |
| `flowbeast/reverse/`（逆向工程 CLI） | 静态语料壁垒证伪；产出为 0 |
| `flowbeast/observe/quality/calibrator.py` | 校准权重是循环论证，无意义 |
| `flowbeast/hooks/`（开发期钩子） | 从未接进 `.git/hooks/`，纯装饰 |
| `flowbeast/data/raw/`、`.ai/archive/`、`.ai/current/tasks/`、`.serena/memories/` | 语料流水线与历史任务，方向已作废 |
| `tests/test_graft.py`、`tests/evidence_package.py` | 测被测对象已删 |
| `tests/test_config.py`、`tests/test_main.py` | 断言类型存在性与源码文本，抓不到真 bug |
| `codebase-map.html`、`demo_recording_guide.md`、`.ai/current/content_strategy.md` | 过期 |
| `README.md` 里的 GRAFT 演示、截图章节、7 个入口点表 | 与当前代码不符 |

**文件数：143 → 约 100。**

---

## 代码现状（现在真实的样子）

| 组件 | 状态 | 说明 |
|------|------|------|
| CLI 全流程 (`python main.py --topic "..."`) | ✅ | 端到端跑得通（本地） |
| FastAPI（4 端点） | ✅ | `/health`、`POST /api/v1/generate`、`GET /api/v1/tasks/{id}`、`GET /api/v1/download/{type}/{run_id}` |
| Streamlit UI | ✅ | `flowbeast/demo/app.py`（已去掉 GRAFT 勾选框与结构面板） |
| FP3 记忆（检索 / 注入 / 反馈） | ✅ | 约 20 条手写演示数据 |
| QualityGate（9 维评分 + 去重 + 审计） | ⚠️ | 能跑，但**从未给出过 ACCEPT**，权重未标定 |
| Edge TTS 音频 | ✅ | 本地可用 |
| 容器内音频拼接 | 🔴 | 镜像缺 ffmpeg/字体 —— 定型前不修 |
| 测试 | ✅ | 34 个用例通过 |
| **真实付费客户** | 🔴 | **0 —— 唯一重要的数字** |

### ⚠️ 别把上表的 ✅ 当成「验证过」

2026-10-15 的代码复现（对活索引）发现七个缺陷，详见 playbook Part 0。
最要紧的两个：QualityGate 从未返回 ACCEPT；9 个维度里有 4 个（0.45 权重）只读 `unit.hook` 一个字段。
GRAFT 的问题已随代码删除而消失。

---

## 当前优先级

**拿到第一笔真实付费证据。** 见 [goal.md](goal.md)。

1. 打通交付路径（本地跑通 → 产物可交付）
2. 找到第一个客户（谈「一集成片」，不谈 API）
3. 免费评分器做获客入口

---

## How to Run

```bash
# CLI 全流程
uv run python main.py --topic "your topic"

# API 服务
uvicorn flowbeast.api.main:app --reload --port 8000

# Streamlit UI
uv run streamlit run flowbeast/demo/app.py --server.port 8501

# 测试
uv run pytest tests/ -q
```
