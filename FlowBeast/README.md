## Text_scripts

### Drama Pipeline Structure

**flowbeast/drama** 目录下的逻辑流：

> **总览**：一条「选题 →（prompt + fp3）→ 剧本 JSON → 落盘 → 配音 → 报告」流水线。`fp3` 只在 **generator** 内参与：在调用 LLM 之前把检索到的基因拼进 prompt。

```mermaid
flowchart LR
  topic[topic 字符串]
  prompt[prompt.py: build_prompt]
  subgraph FP3[fp3]
    RET[retriever.retrieve]
    INJ[injector.inject_prompt]
    RET --> INJ
  end
  gen[generator.py: generate_script]
  disk[(script.json 等)]
  aud[audio.py: generate_audio]
  rep[(production_report.json)]

  topic --> prompt
  topic --> RET
  prompt --> INJ
  INJ --> gen
  gen --> disk
  gen --> aud
  aud --> rep
```

### FP3 子系统（与上图中 `FP3` 框一致）

```mermaid
flowchart LR
  subgraph WRITE["① 建库（离线）"]
    direction TB
    SCH[schema: ViralUnit]
    BLD[builder + embed_unit]
    SEED[seed_data + embed_text]
    STW[store.add → save]
    SCH -.-> BLD
    BLD --> STW
    SEED --> STW
  end

  subgraph READ["② 在线检索（generator 内）"]
    direction LR
    EMB[embedding.embed_text]
    SRH[store.search]
    EMB --> SRH
  end

  WRITE -.->|索引与 meta 文件| READ
```

**drama 与 fp3 的结合点**（唯一）：`flowbeast/drama/generator.py` → `generate_script`：先 `build_prompt(topic)`，再 `FP3Retriever.retrieve(topic)`（内部 **embedding → store.search**），再 `inject_prompt(base_prompt, examples)`，最后 `llm_call`。

`core/config` 的 `settings` 在 pipeline、generator、audio、fp3 的 `store` 路径上提供目录、模型、Key 等。

一流项目:用 pytest + 清晰目录/标记 + pyproject 约定 + CI 分档 + 文档 解决「又全又快」和「脚本 vs 测」的边界；很少靠「一个统一入口文件」。