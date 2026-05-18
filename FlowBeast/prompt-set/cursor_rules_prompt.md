FlowBeast Cursor Rules Pack

下面是一套适合我当前 FlowBeast 阶段（AI Content Engine / RAG / Agent / Pipeline / Docker / FastAPI）的 Cursor Rules。

目标不是“完美企业规范”，而是：

保持 AI 输出稳定
降低架构漂移
提升长期一致性
减少 AI 擅自 over-engineering
适配 Claude / DeepSeek / Qwen 多模型协作
适合单人 AI 创业项目快速迭代

建议目录结构：

.cursor/
└── rules/
    ├── 01-project.md
    ├── 02-architecture.md
    ├── 03-coding-style.md
    ├── 04-testing.md
    ├── 05-python.md
    ├── 06-ai-agent.md
    ├── 07-docker-devcontainer.md
    └── 08-git-workflow.md



# 01-project.md

> FlowBeast Project Rules

FlowBeast is an AI-native content generation and automation system.

Current focus:
- Viral content pipeline
- AI drama/comic generation
- RAG + retrieval enhancement
- Multi-agent orchestration
- Automated video/content workflow
- Fast iteration MVP

Project priorities:
1. Working systems over theoretical perfection
2. Fast iteration over premature abstraction
3. Simplicity over enterprise complexity
4. Maintainability over clever code
5. Production pipeline stability over experimentation

The assistant must:
- Preserve existing architecture unless explicitly instructed
- Avoid unnecessary abstractions
- Avoid introducing frameworks unless required
- Avoid rewriting unrelated modules
- Prefer incremental refactors
- Keep functions and modules understandable
- Preserve backward compatibility when possible

The assistant should understand:
- This is a long-term evolving monorepo
- Architecture consistency is critical
- Token/context efficiency matters
- Docker/devcontainer environment is important
- Local development workflow must remain stable

When generating code:
- Prefer explicit code over magic
- Prefer readability over extreme DRY
- Prefer predictable behavior over hidden automation
- Prefer modular design without fragmentation

Never:
- Silently rename public APIs
- Change project structure without reason
- Introduce heavy dependencies casually
- Generate fake implementations pretending to work
- Over-engineer abstractions for future possibilities
- Replace existing stable implementations unnecessarily

The project is optimized for:
- AI-assisted development
- Multi-model collaboration
- Long context engineering
- Rapid experimentation
- Local-first workflows


# 02-architecture.md

> FlowBeast Architecture Rules

Core architecture:
FP2 -> FP3 -> IP1 -> IP2 ->  Product -> Observe -> FP2


Definitions:

- FP2 = data processing layer
- FP3 = viral knowledge base + retrieval
- IP1 = generation enhancement/RAG
- IP2 = multi-agent automation
- Product = video/content pipeline MVPObservation and Feedback Center
- Observe = Observation and Feedback Center


Architecture rules:


## Module Boundaries


Each module should:
- Have a clear responsibility
- Minimize cross-dependencies
- Expose stable interfaces
- Avoid circular imports


## Preferred Design


Prefer:
- Service layer
- Adapters
- Config-driven systems
- Explicit pipelines
- Typed models
- Stateless processing


Avoid:
- Deep inheritance trees
- Hidden side effects
- God objects
- Overuse of decorators
- Meta-programming unless necessary


## Configuration


Configuration must:
- Use centralized config
- Support .env loading
- Work inside Docker/devcontainers
- Avoid hardcoded paths
- Support proxy/network configuration


## AI Pipelines


AI pipeline code should:
- Be traceable
- Be debuggable
- Preserve intermediate outputs
- Support retries
- Support caching when useful
- Preserve prompts for observability


## Long-term Maintainability


The assistant must think about:
- Future agent expansion
- Long context workflows
- Retrieval scaling
- Async task orchestration
- Content generation reliability


But should NOT prematurely build infrastructure for them.


## File Organization


Prefer:
- Small focused modules
- Clear naming
- Predictable directory structure


Avoid:
- 2000-line files
- Utility dumping grounds
- Random helper modules


# 3-coding-style.md

> FlowBeast Coding Style Rules

- One-letter variables
- Clever hacks
- Deep nesting
- Massive functions
- Unnecessary async


## Comments


Comments should explain:
- Why
- Architectural intent
- Non-obvious decisions


Do NOT comment obvious code.


## Logging


Prefer structured logging.


Log:
- Pipeline stages
- Errors
- Retries
- Important state transitions
- AI request metadata


Avoid noisy logs.


## Error Handling


Never silently swallow exceptions.


Prefer:
- Explicit exception handling
- Meaningful error messages
- Retry-safe operations


## Imports


Prefer:
- Absolute imports
- Stable import paths
- Grouped imports


Avoid:
- Wildcard imports
- Circular dependencies


## Refactoring


Refactors should:
- Preserve behavior
- Be incremental
- Avoid unnecessary rewrites
- Minimize architectural drift


## AI-Generated Code


AI-generated code must:
- Be production-readable
- Avoid placeholder implementations
- Avoid fake mocks unless requested
- Avoid TODO-heavy output
- Prefer working minimal solutions


# 04-testing.md

> FlowBeast Testing Rules


Testing philosophy:
- Reliability over coverage vanity
- Test critical pipelines first
- Preserve iteration speed


## Priority Testing Areas


Highest priority:
- Retrieval logic
- Prompt pipelines
- Agent orchestration
- Config loading
- Docker/devcontainer behavior
- API boundaries
- File processing pipelines


Lower priority:
- Thin wrappers
- Simple DTOs
- Trivial utility functions


## Preferred Test Style


Prefer:
- pytest
- Clear test naming
- Small focused tests
- Integration tests for pipelines
- Realistic test data


Avoid:
- Over-mocking
- Brittle snapshot tests
- Artificial enterprise test patterns


## Test Naming


Use:
- test_<behavior>
- test_<condition>_<result>


Examples:
- test_load_config_from_env
- test_retriever_returns_ranked_results
- test_pipeline_handles_timeout


## AI Pipeline Testing


AI-related tests should:
- Validate structure
- Validate schema
- Validate retries/fallbacks
- Avoid depending on exact wording


## Regression Prevention


Important bug fixes should include tests.


## Performance


Tests should:
- Run locally
- Work inside devcontainers
- Avoid external dependency requirements when possible


# 05-python.md

> FlowBeast Python Rules

Preferred stack:
- Python 3.11+
- FastAPI
- Pydantic
- pytest
- uv


## Async


Use async only when:
- IO-bound
- External API heavy
- Parallel workflows are beneficial


Avoid unnecessary async complexity.


## Pydantic


Prefer Pydantic for:
- Config
- Request schemas
- Structured outputs
- Pipeline contracts


## File Paths


Never hardcode absolute paths.


Use:
- pathlib.Path
- Config-driven paths


## Environment


Code must work in:
- Local Linux
- Docker
- Dev Containers
- CI environments


## External APIs


External API integrations must:
- Support retries
- Handle timeouts
- Handle rate limits
- Preserve observability


## AI API Calls


AI model calls should:
- Preserve prompts
- Preserve responses
- Support provider swapping
- Avoid provider lock-in


# 06-ai-agent.md

> FlowBeast AI Agent Rules


Agent philosophy:
- Agents are tools, not magic
- Deterministic pipelines are preferred when possible
- Observability is mandatory


## Agent Design


Agents should:
- Have clear responsibilities
- Have explicit inputs/outputs
- Be composable
- Be debuggable


Avoid:
- Monolithic autonomous agents
- Hidden prompt chains
- Untraceable tool calls


## Prompt Engineering


Prompts should:
- Be versioned
- Be modular
- Be reusable
- Be observable


## Tool Usage


Tool interfaces should:
- Be stable
- Be explicit
- Return structured data


## Multi-Agent Systems


Prefer:
- Coordinator patterns
- Explicit orchestration
- Shared memory abstractions


Avoid:
- Recursive uncontrolled agent loops
- Excessive autonomy


# 07-docker-devcontainer.md

> FlowBeast Docker & DevContainer Rules


Environment philosophy:
- Reproducible development
- Local-first workflows
- Stable container environments


## Docker


Dockerfiles should:
- Be minimal
- Be cache-friendly
- Avoid unnecessary layers
- Preserve readability


Avoid:
- Huge all-in-one images
- Unnecessary system packages


## Dev Containers


Devcontainer environments must:
- Mirror production reasonably
- Support VS Code workflows
- Support AI coding tools
- Preserve bind mount behavior


## Volumes and Mounts


Understand:
- /app is bind-mounted from host
- File changes are real-time
- Containers are ephemeral
- Source code lives on host filesystem


## Networking


Support:
- Proxy configuration
- OpenAI-compatible APIs
- OpenRouter
- Local model providers


## Scripts


Scripts should:
- Be idempotent
- Be readable
- Fail loudly
- Avoid destructive defaults


# 08-git-workflow.md

> FlowBeast Git Workflow Rules


Git philosophy:
- Small commits
- Clear history
- Observable evolution


## Commit Style


Prefer:
- feat:
- fix:
- refactor:
- docs:
- test:
- chore:


Examples:
- feat: add fp3 retriever ranking pipeline
- fix: resolve docker env loading issue
- refactor: simplify agent orchestration


## Branching


Prefer short-lived branches.


Avoid:
- Massive long-running divergence
- Huge mixed-purpose commits


## AI-Generated Commits


AI-generated changes must:
- Be reviewed
- Preserve architecture consistency
- Avoid broad unrelated modifications


## Hooks


Hooks should:
- Improve quality
- Remain fast
- Avoid blocking iteration unnecessarily


## Repository Hygiene


Keep:
- Clear structure
- Predictable naming
- Minimal dead code


Avoid:
- Random experiments on main branch
- Large unrelated rewrites


# 使用建议（非常重要）

不要一次性把所有规则都写得极其严格。

Cursor Rules 的真正目的不是：“限制 AI”

而是：“稳定 AI 的长期输出风格”

对于你现在的 FlowBeast 阶段,最重要的是：

防止 AI over-engineering
防止架构漂移
保持长期一致性
提高多模型协作稳定性
减少上下文污染

你后面会发现：真正强大的 AI coding workflow,不是“最强模型”,而是：
稳定规则
稳定上下文
稳定工程结构

# Prompt

You are acting as a senior AI engineering architect and repository governance assistant for the FlowBeast project.

Your task is to transform the rule specification document below into a real Cursor Rules system for this repository.

Source file:
- /home/arleszhang/FlowBeast-p1/FlowBeast/prompt-set/cursor_rules_prompt.md

Objectives:
1. Read and understand the entire rule document.
2. Design the most appropriate `.cursor/rules/` directory structure for the current FlowBeast project stage.
3. Split the content into logically separated rule files.
4. Create the actual directory and markdown files.
5. Refactor duplicated sections if necessary.
6. Preserve architectural intent and wording consistency.
7. Optimize for long-term AI-assisted development.
