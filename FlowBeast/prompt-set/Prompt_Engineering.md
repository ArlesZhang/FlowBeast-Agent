# Prompt Engineering — Thinking & Principles

> 本文档是 README.md 的补充，记录在与 AI 协作工具（Claude Code、Cursor 等）实战中提炼的核心原则。
> README 定义"怎么建"，本文定义"怎么想"。

---

## 核心原则：注入 vs 剔除（Injection vs Exclusion）

**Prompt 工程的本质不是"往里塞什么"，而是"控制上下文窗口里最终剩下什么"。**

上下文窗口 = 注入 − 剔除

| 维度 | 注入（加） | 剔除（减） |
|---|---|---|
| 显式上下文 | CLAUDE.md、skills、agents、MCP | — |
| 隐式上下文 | 对话历史、代码引用 | `.claudeignore`、`.gitignore`、`.cursorignore` |
| 运行时环境 | 环境变量、工具权限 | 虚拟环境隔离、进程数限制 |
| 文件范围 | 指定读取的文件 | 排除的目录/文件模式 |

**教训**：一次"多线程僵尸风暴"（OOM 杀死 Claude Code）的根因不是 prompt 太长，而是 `.claudeignore` 缺失导致 `.venv/`（675MB、144 个第三方包）+ `__pycache__/`（13 个目录）+ `.git/` 全部被纳入扫描。注入再好的 prompt，也会被无限制的上下文污染淹没。

**结论**：剔除 > 注入。先建 fence，再建 house。

---

## 守则

### 1. 隔离优先（Isolation First）

在让 AI 读代码之前，先用 ignore 文件划定边界：

- `.claudeignore` — 控制 AI 索引上下文（比 `.gitignore` 更重要）
- `.gitignore` — 控制版本控制范围
- `.venv/` 必须被 `.claudeignore` 排除（否则 144 个包的源码全部进入窗口）

**新项目第一步不是写 CLAUDE.md，而是建 `.claudeignore`。**

### 2. 上下文窗口不是"越大越好"，而是"越干净越好"

Claude Code 的索引器是贪婪的——没有 `.claudeignore` 时会递归扫描所有可达文件。一个 675MB 的 `.venv/` 加上十几个 `__pycache__/` 目录，可以在一次复杂任务中产生数千个文件读取请求。

**规则**：每次添加新依赖（`uv add`、`npm install`）后，确认 ignore 文件覆盖了新增目录。

### 3. Agent/Sub-Agent/Team 的上下文是独立的，但也各自需要剔除

子代理（Agent、Team）有自己独立的上下文窗口，但如果它们的工作目录共享同一个 `.claudeignore`，隔离策略就有效。注意：

- 子代理不会继承主代理的 ignore 配置——它们从文件系统重新读取
- 如果 `.claudeignore` 不存在，每个子代理都会独立触发全量扫描
- **多个子代理同时扫描 `.venv/` = 内存乘以子代理数量**

### 4. 环境变量和运行时配置也算 prompt 工程的一部分

- `.env` 里写错的 `ACTIVE_VENDOR` 会导致代码走错误的协议路径（比如 `aliyun` → 404）
- 代理地址（`ANTHROPIC_BASE_URL`）本质上是 prompt 的"路由指令"
- **配置错误 = 隐式 prompt 注入**，且比显式 prompt 更难调试

### 5. 区分"协议层"和"厂商层"

AI Infra 配置中，**API 协议**（OpenAI-compatible / Anthropic-compatible / Google GenAI）和**服务厂商**（Qwen / Token Plan / OpenAI / Gemini）是两个不同的抽象层级：

- 协议层决定用什么 SDK（`openai.OpenAI` vs `anthropic.Anthropic`）
- 厂商层决定 key 和 URL 指向哪里
- 按协议拆分代码，比按厂商拆分更稳定（新增厂商只需加配置，不改逻辑）

### 6. 配置的一致性高于一切

- `.env` 里的值应该和代码的解析逻辑一一对应，不要搞"别名回退"（比如 `aliyun → qwen`）
- 配置错误应该在 `.env` 层修复，不要在代码里加 workaround
- **代码是规则的体现，配置是规则的实例**——不一致会让未来的维护者无法判断哪个是真相

### 7. 调试 AI 行为时，先看环境，再看 prompt

当 Claude Code / Cursor 出现奇怪行为（卡死、闪退、读错文件）时：

1. 检查 `.claudeignore` / `.cursorignore` 是否缺失或过时
2. 检查 `__pycache__/`、`.venv/`、`.git/` 是否被索引
3. 检查环境变量是否干净（`env | grep -i proxy` 等）
4. **然后**才看 prompt 和对话内容

环境问题的优先级永远高于 prompt 调优。

---

## 快速检查清单（新项目 / 新会话）

```bash
# 1. 是否有 .claudeignore？
test -f .claudeignore || echo "⚠️ 缺失 .claudeignore"

# 2. .venv 是否被排除？
grep -q "\.venv/" .claudeignore || echo "⚠️ .venv/ 未被 .claudeignore 排除"

# 3. __pycache__ 是否被排除？
grep -q "__pycache__" .claudeignore || echo "⚠️ __pycache__ 未被排除"

# 4. 环境变量是否干净？
env | grep -iE "HTTP_PROXY|HTTPS_PROXY|ALL_PROXY" && echo "⚠️ 存在代理环境变量"

# 5. 虚拟环境是否激活？
echo $VIRTUAL_ENV || echo "⚠️ 虚拟环境未激活"
```
