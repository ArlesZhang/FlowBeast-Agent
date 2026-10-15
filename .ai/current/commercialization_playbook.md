# Commercialization Playbook

> ## ⚠️ 四条早期创业路径已被证伪 —— 读本文前先记住这一句
>
> **市场反馈表明，静态语料壁垒、低价抽取服务、特定品牌命名以及提示词包等四条早期创业路径已被证伪。AI 2.0 时代轻资产模式已难以为继，从业者需要转向更深层的系统级工作流集成与业务结果交付。**
>
> *English gloss: four early-stage playbooks — a static-corpus moat, cheap extraction services,
> a distinctive brand name, and prompt packs — have been empirically falsified by the market.
> Light-asset models no longer work in the AI 2.0 era; the way forward is deeper system-level
> workflow integration and delivery of business outcomes.*
>
> This is the premise of everything below. Every recommendation in this document is a
> **system-level workflow integration** or a **business-outcome delivery** — or it is not in here.

> **What this document is.** A decision document for turning FlowBeast from a working prototype
> into something that produces paid outcomes. It has two halves: (1) what the market has already
> built that you should borrow instead of writing, and (2) the shortest evidence-backed path to a
> first paying customer.
>
> **What it is not.** It is not a feature roadmap, and it is not a plan to keep building.

Created 2026-10-15. Method: direct code reproduction against the live FP3 index, plus verified
external research. Every claim is tagged:

| Tag | Meaning |
|---|---|
| `[REPRO]` | Ran the real code against the real data in this repo and reproduced it |
| `[V-live]` | Executed the tool live on this machine and read the actual output |
| `[V]` | A research agent fetched the live page and read it |
| `[S]` | Secondary source — page not opened |
| `[U]` | Vendor self-report, no methodology. Treat as marketing |
| `[UV]` | Unverified — flagged so it is not over-trusted |

**Exclusion rule.** Per the request, anything already enumerated in
[capability_map.md](capability_map.md) is out of scope as a *recommendation*. That document already
covers LangGraph, OpenAI Agents SDK, CrewAI, GitHub Actions, HF Spaces, Railway/Render/Fly.io,
Modal, Prefect, Dagster, Temporal, Dify, n8n, DSPy, GEPA, Promptfoo, Langfuse, Opik, Arize Phoenix,
RAGAS, DeepEval, OpenTelemetry GenAI semconv, W&B, MLflow, Evidently, scipy.stats, and
PEFT/LoRA/TRL/Unsloth. **None of those are repeated below.** Where new evidence contradicts a
conclusion in that file, it is flagged explicitly.

---

# Part 0 — The finding that changes the plan

> **Status note (2026-10-15):** this part is **historical evidence for why the old direction was
> dropped**, not a to-do list. The files it cites — `flowbeast/vto/`, `flowbeast/reverse/`,
> `flowbeast/observe/quality/calibrator.py`, `flowbeast/hooks/`, `flowbeast/data/raw/` — have since
> been **deleted from the repository**, so the links below are dead on purpose. F1, F3, F5 and the
> hooks finding went away with the code. F2, F4, F6, F7 describe code that is still live.

Before the market research matters, one thing has to be said plainly.

I ran FlowBeast's own code against its own index to check whether the moat works. It does not, in a
way that is invisible from the outside because nothing crashes.

## F1 — GRAFT transfers a constant, not a structure `[REPRO]`

Three unrelated topics were run through `graft_operator()`:

| Topic | hook_type | conflict_type | escalation_curve | reversal_count | highest_stakes | audience_question | emotional_payload |
|---|---|---|---|---|---|---|---|
| 程序员穿越修仙界 | 冲突爆发 | 权力碾压 | 压抑→升级→爆发→反转 | 1 | 尊严 | *(empty)* | *(empty)* |
| 豪门真假千金 | 冲突爆发 | 权力碾压 | 压抑→升级→爆发→反转 | 1 | 尊严 | *(empty)* | *(empty)* |
| 末日丧尸求生 | 冲突爆发 | 权力碾压 | 压抑→升级→爆发→反转 | 1 | 尊严 | *(empty)* | *(empty)* |

Byte-identical structure. Only `opening_line` varied — and only because that field falls back to the
retrieved record's `hook` text.

**Root cause.** [`fp3_meta.json`](../../flowbeast/data/outputs/vector_store/fp3/fp3_meta.json)
contains 60 records: 40 with the `PromptAtom` key set `(atom_id, embedding, layer, prompt_fragment,
role, source, tags, version, vto_metadata)` and 20 with `(emotion, hook, pattern)`.
**Zero records contain a `hook_structure` or `conflict_pattern` key.**

So in [graft.py:120](../../flowbeast/vto/graft.py#L120):

```python
hs = viral_script.get("hook_structure", {})   # always {} → every .get() default fires
```

Every `.get(..., default)` in `_extract_hook_structure` and `_extract_conflict_pattern` returns its
hardcoded literal — `"冲突爆发"`, `"权力碾压"`, `["压抑","升级","爆发","反转"]`, `1`, `"尊严"`. Those
literals are the entire "viral structure" the operator claims to have learned.

**Consequence for the product.** Two of the five migration instructions in the generated prompt
([graft.py:196](../../flowbeast/vto/graft.py#L196) and
[graft.py:200](../../flowbeast/vto/graft.py#L200)) interpolate `emotional_payload` and
`highest_stakes`-adjacent fields. The first is always an empty string. Instruction #3 in the GRAFT
prompt therefore reads, verbatim:

> 3. **情绪载荷保留**: 开场必须触发与原始钩子相同的情绪反应（），但通过"{topic}"的新情境来实现。

The prompt tells the model to preserve an emotion that was never specified.

## F2 — No type filter, and the failure is silent `[REPRO]`

[retriever.py](../../flowbeast/fp3/retriever.py) searches the index with no filter on record type:

```python
candidates = self.store.search_with_scores(vec, k=min(k * 3, 10))
sim_score = max(0, 1 - dist / 2)
combined = sim_score * 0.7 + feedback_boost * 0.3
```

A `PromptAtom` and a `ViralScript` are interchangeable to it. In my three test runs the top hit
happened to be a `ViralUnit` — so the failure did not fire — but that is luck, not design. If a
`PromptAtom` wins the retrieval, [injector.py](../../flowbeast/fp3/injector.py) hits bare `ex['hook']`
indexing and raises `KeyError`. That exception is then swallowed at
[generator.py:118](../../flowbeast/drama/generator.py#L118):

```python
except Exception as e:
    logger.warning(f"⚠️ FP3 增强失败，使用增强 prompt: {e}")
```

The pipeline continues with an unenhanced prompt and a warning line. **This is the worst possible
failure mode for a corpus-building project**: you add 30 real scripts, some retrievals still fall
through to defaults, nothing errors, and the natural conclusion is "the corpus doesn't matter."

I originally predicted this failure was live. It is not — it is latent. I am recording it as latent.

## F3 — The corpus factory has no factory `[REPRO]`

[raw/corpus_batch/sample_template/](../../flowbeast/data/raw/corpus_batch/sample_template/) defines the
unit of corpus work. It is seven files per sample, and `transcript.txt` contains literally:

```
[If available, paste the dialogue transcript here]
```

There is no ASR, no scene detection, no OCR anywhere in the repo. The real loop is:

> watch the drama → screenshot → **type the transcript by hand** → type the metrics → fill a
> seven-section interactive form ([reverse_engineer.py:111](../../flowbeast/reverse/reverse_engineer.py#L111))

`flowbeast/data/reverse_engineered/` is empty. Zero scripts. The blocker described in
[roadmap.md](roadmap.md) as "the sole blocker" has no tooling behind it at all.

## F4 — QualityGate has never returned ACCEPT `[REPRO]`

Across all 19 records in
[quality_audit/](../../flowbeast/data/quality_audit/):

| Action | Count |
|---|---|
| ACCEPT | **0** |
| REVIEW | 10 |
| REJECT | 9 |

Score range 0.2531–0.5195 against `QUALITY_ACCEPT_THRESHOLD = 0.60`
([config.py:32](../../flowbeast/observe/quality/config.py#L32)).

Six separate runs on the topic "一个普通的故事" scored **exactly 0.2531** — to four decimal places, on
different days. The score is a function of the topic string, not of what was generated.

All nine dimensions in [scorer.py](../../flowbeast/observe/quality/scorer.py) are regex keyword
counting over `unit.hook`. `_score_hook_strength` is length + count of `_STRONG_HOOK_MARKERS`
matches × 0.25 + a specificity bonus. It measures *whether certain words appear*, never whether the
script is any good.

**A gate that cannot pass its own output is not a gate.** It is a constant with extra steps. And
because `reverse_engineer.py` routes corpus ingestion through this gate
([`_gate_before_inject`](../../flowbeast/reverse/reverse_engineer.py#L362)), **the gate would reject
the real corpus you are trying to ingest.** That is a direct contradiction sitting in the code right
now: the tool that builds the memory is gated by a scorer that rejects everything.

## F5 — The test suite codifies the bug as correct `[REPRO]`

[test_graft.py:58](../../tests/test_graft.py#L58):

```python
assert hs["hook_type"] == "冲突爆发"  # default
```

The comment says it out loud. Nine GRAFT tests pass, and they pass *because* the default fires. No
test exercises the real `index → retrieve → extract` path. The suite gave false confidence that the
moat works.

## F6 — The calibration is circular by construction `[REPRO]`

[calibrator.py](../../flowbeast/observe/quality/calibrator.py) recommends dimension weights as

```
recommended_weights ∝ |pearson_corr(dimension, total_including_that_dimension)|
```

Every dimension is correlated with a total that *contains that dimension*. The correlation is
therefore partly an artifact of the part-whole overlap, not a measure of how much the dimension
predicts quality — the classic part-whole inflation (Pearson 1897; Kronmal 1993).

Reproduced on pure noise: 200 trials with **randomly generated, meaningless** dimension scores at
n = 21 still reproduce a stable weight vector (mean ρ = 0.423). `hook_strength` ranks #1 in **46%**
of pure-noise trials. A dimension given **zero weight** in the ground truth reaches |r| = 0.738.

**Consequence:** the weights are not learned from data. They are a fixed point of the formula, and
they will look the same whether or not the dimensions mean anything. Running the calibrator on real
labels would *not* fix this — the artifact is in the estimator, not the data.

## F7 — 45% of the gate's weight measures something the scorer cannot see `[REPRO]`

`ViralUnit` carries three fields: `hook`, `pattern`, `emotion`. The nine `_score_*` methods in
[scorer.py](../../flowbeast/observe/quality/scorer.py) all read **only `unit.hook`**. By the weights
in the scorer, the dimensions that depend on structure the unit does not store account for **0.45**
of the total.

So the gate's output is a function of one string field. Two units with identical hooks are
indistinguishable to QualityGate no matter how different their structure, emotion arc, or conflict
pattern. This is the schema-level cause of F1: GRAFT cannot transfer `hook_structure` because nothing
in the record it retrieves has one.

## The synthesis

FlowBeast currently has **five self-referential loops and no external anchor**:

1. **The corpus** is the builder's own judgment, entered by hand through a form, and gated by a
   scorer that rejects it.
2. **GRAFT** transfers five hardcoded constants and calls it structure transfer.
3. **QualityGate** is regex over keywords, has never accepted anything, and is therefore not
   measuring quality — it is measuring vocabulary.
4. **The calibration** derives its weights from a formula that returns the same answer on noise.
5. **The schema** cannot represent the structure that most of the gate's weight is supposed to
   measure.

There is no point in the system where reality — a real viewer's retention, a real hit, a real
failure — enters. That is why pushing forward feels vague. It is not a motivation problem. **The
system cannot tell you whether it is getting better.** Every additional feature is added to a
machine with no feedback signal.

This reframes the commercialization question. The instinct is "I need a better product before I can
sell it." The correct read is: **you cannot sell a moat you cannot measure, and you cannot improve
one either.** Two days of fixing the measurement loop is worth more than four weeks of corpus
grinding — because the corpus grinding currently produces no visible change.

---

# Part 1 — What the market has already answered

Six findings from external research that each close off a path. Read these before choosing a
direction, because four of them eliminate options that look attractive.

## 1.1 Your corpus is not scarce. It is nearly free.

| Asset | What it is | Scale | Access |
|---|---|---|---|
| **SkyScript-100M** ([arXiv 2408.09333](https://ar5iv.labs.arxiv.org/html/2408.09333)) | Shooting scripts for short drama: **shot descriptions, character/object descriptions, 3D layout, 爽点/highlight scores, emotion states, camera details** — sourced from 6,660 real short-drama episodes | ~10M annotated scripts; "1B pairs" headline is synthetic expansion | [github.com/vaew/SkyScript-100M](https://github.com/vaew/SkyScript-100M), dataset release `[V]` |
| **M-Drama** ([arXiv 2609.07107](https://huggingface.co/papers/2609.07107), EMNLP 2026) | 9,138 annotated **micro-drama** clips, 35K+ instances, bilingual | Micro-drama, not ads | `github.com/qyx1121/MDrama_SAGA` — **download link unconfirmed** `[V]` |
| **DramaChain Bench** ([arXiv 2609.00646](https://huggingface.co/papers/2609.00646)) | 5 axes → **63 leaf dimensions** over 5,785 items; **17,488 professional human scores** from 543 annotators; Agentic Judge reproducing human rankings at **PLCC 0.918** | Evaluates script → storyboard → keyframe → shot video → finished drama | Dimensions + judge are a **planned** release — not confirmed downloadable `[V]` |
| **DataEye / 剧查查** | The incumbent Chinese short-drama data business. **250,000+ short dramas indexed**, 750K+ industry professionals, 20K+ companies, 21 genres, domestic + overseas UA leaderboards | Already shipped | **¥3,000/yr entry** `[V]` |

**The implication is not subtle.** SkyScript-100M already ships shot-level descriptions with
highlight scores, emotion states, and camera details for exactly the genre FlowBeast targets. That
is a structured superset of what `EmotionalCurve` and `PacingProfile` are trying to capture. And
DataEye has already indexed 250,000 dramas and sells access for ¥3,000/year.

[capability_map.md §8](capability_map.md) states the corpus is "唯一真正稀缺的东西" (the only truly
scarce thing). **That conclusion is now wrong.** The corpus is available. What is scarce is a
*feedback loop* — real performance data on *your* outputs.

## 1.2 Your extraction step is a commodity API sold by hyperscalers

| Vendor | Product | Price |
|---|---|---|
| **BytePlus** (ByteDance cloud) | `las_short_drama_script_gen`: **feed it a short-drama episode URL → get a script back.** Auto-detects drama vs movie mode | **~$0.21 per input-video minute** `[S]` |
| **Alibaba Cloud** AnalyticDB / AI Screenwriter | Structure generation, episode outlines, cliffhanger/paywall hooks, **10-dimension screenplay quality check**, and — verbatim from their docs — **"framework adaptation: extracting narrative structure / conflict patterns / emotional arcs to transfer to new genres"** | Cloud consumption pricing `[S]` |

That second row is FlowBeast's thesis, described as a use case of a database product. "Extract
narrative structure and transfer it to a new genre" is GRAFT, written in Alibaba's documentation.

**What this means for positioning:** you cannot charge a premium for the mining. The mining is a
metered utility. Whatever you sell has to be something else.

## 1.3 The name is already taken by a funded competitor

**Alison.ai** shipped a product literally called **"Creative Genome"** on 2025-10-03 — verified
verbatim on their live site `[V]`. Homepage: *"The Intelligence to Guide Your Creative — Powered by
the Creative Genome."* They decompose creatives into **hooks, pacing, visuals, messaging, CTAs**, tie
them to performance, and regenerate. a16z participated; ~$13.3M seed, ~$21.5M total `[S]`. They also
ship an MCP server.

Same decompose → recombine loop. Same metaphor. Better funded. And they own the search results.

**Action:** if FlowBeast markets itself with "viral genome" or "creative genome" language, it enters
a buyer conversation as the smaller, later, unknown version of an existing company. Rename the
metaphor or accept permanent brand shadow.

## 1.4 The prompt-pack business is a dead cell — with numbers

This is the model most solo AI projects default to. The data on it is unambiguous.

| Evidence | Number |
|---|---|
| **Gumroad "ai prompts" category**, 36 listings, CC BY 4.0 open dataset, measured 2026-08-05 | Median price **$47**; middle half $39–$99; **most-rated listing in the entire category = 168 ratings, ever** `[V]` |
| **闲鱼 platform data, H1 2026** | 9.816M AI-service orders (+157% YoY), ~5M buyers — but **AI-service sellers average under ¥900/month GMV**, and 提示词优化 is the *cheapest* sub-category ("小到几块钱") `[V]` |
| **钛媒体's verdict on the same data** | *"暴富是假象，小额增收才是真相"* — and *"卖课的人赚走了所有稳定收益"* `[V]` |
| **The ¥59 即梦/可灵 prompt pack** | Real, well-structured (200 shot prompts, 24 motion types, 30-sec storyboard template). Ships this disclaimer verbatim: **"提示词未在两款工具中逐条测试"** — never tested one by one in the tools it targets `[V]` |
| **PromptBase** (the category flagship) | Has pivoted to `/create` (an AI app builder) and `/apps`. Their own seller guidance: *"prompts that provide utility instead of art … provide the best long term sales"* `[V]` |
| **Controlled field test** | Same 5 prompts: $15 → 3 sales/mo; repackaged with tutorial + docs at $35 → **8 sales/mo**. Same tester on PromptBase: 3 prompts over 2 weeks = **$14 total** `[V]` |
| **The surviving high-ticket cell** | 短剧创作辅助包 to *teams*: **¥500–2,000/set, custom ¥3,000–5,000, 95%+ gross margin** `[S]` |

**Do not price `prompt_package.json` at ¥19.9–59 or $19–47.** That is precisely the cell where the
¥900/month average, the 168-rating ceiling, and free GitHub compilations all live.

## 1.5 The shape that is actually working

**有戏AI** (风平智能 / Fengping Intelligence) `[V — 央广网 2026-02-05, vendor-originated]`:

- **Closed loop**: 剧本解析 → 角色设计 → 智能分镜 → 配音合成 → 成片导出, multi-agent
- Imports scripts up to 50,000 characters, auto-generates storyboard prompts
- **Pricing: ¥0.1/sec video, <¥10 per episode** — priced *per output*, not per seat or per prompt
- **First-month revenue annualized to ARR > ¥36M (~$5M); 68% first-month paid repurchase; >80% of monthly users converted to annual**
- 13,000 creators in 5 days
- Their headline claim is a **speed** claim, not a quality claim: *"新手熟练操作后，10分钟可制作一集完整短剧"* — a novice makes a full episode in 10 minutes; *"一人一天一部剧"* — one person, one drama per day
- Growth was **community-driven**: 邀请码 shared organically across AI短剧 WeChat groups and 知识星球

**Caveats, stated honestly:** this is a single-source, vendor-originated figure, and "ARR annualized
from the first month" is a founder-friendly metric — ¥3M in month one reported as ¥36M ARR. Their
¥0.1/sec is *below* MiniMax's ¥0.50/sec 768p list price, implying heavy subsidy or in-house
inference.

**But the shape is the signal**, and it is corroborated: they did not sell a prompt file. They sold a
closed-loop pipeline priced per finished output, and monetized on subscription conversion rate.

## 1.6 The base rate is brutal, and it argues against your premise

| Metric | Value | Source |
|---|---|---|
| AI microdramas that recoup costs | **~1.3%** | `[S — 36Kr]` |
| Q1 hit rate (Chinese AI short drama) | **0.16%** | `[S — 36Kr]` |
| Share of revenue eaten by ad delivery (投流) | **70–90%** | `[S — 36Kr]` |
| Mid/small teams' cost share spent on 投流 | **80%** | `[V — 猎云网]` |
| Teams dissolving within 3 months despite ¥1M+ revenue share | *many* — **margin under 5%** | `[V — 猎云网]` |
| 90%+ of new Chinese microdramas are AI-made | | `[S]` |

This matters for one specific reason: **if viral structure were transferable via mining, these
numbers would not look like this.** The winning dynamics at scale are distribution spend and platform
algorithm favor. Any pitch positioning "proven viral mechanics" as the primary success driver is
making a claim the market data contradicts — and sophisticated buyers in this market already know it.

The honest, defensible claim is narrower and still valuable: **structure is a necessary input, and
upstream defects cascade.** See §1.7.

## 1.7 The one external finding that argues *for* your positioning

DramaChain Bench measured the **cascade**: degrading an upstream stage costs a clip **0.07–0.13
points**, but the **finished drama 0.25–0.83 points** `[V]`. Upstream damage amplifies downstream by
roughly 2–6×. They also report the top configuration (gpt-5.5-xhigh + gpt-image-2 + seedance-2.0)
delivering a shippable short drama at **3.30 against a >3.0 "usable" line**.

That is published, human-validated evidence that **script-stage quality dominates finished-video
quality**. It is a measured argument for a compiler-stage tool, and it is the most valuable sentence
you can put in a pitch — far more valuable than any feature shipped this month.

---

# Part 2 — What to borrow

Organized by the capability it serves, in the order it should be adopted. Each entry: **what it is /
why this one / how to wire it in**. Nothing here duplicates [capability_map.md](capability_map.md).

## A. Make the moat measurable — do this first

Nothing else on this list matters until the system can tell a good output from a bad one. Currently
it cannot (F1–F5).

### A1. Fix the retrieval/extraction contract before importing anything

**What:** Not a library. A change to your own code, and the highest-value two hours available.
**Why:** Every hour spent on corpus work flows through this path. Import 30 scripts into a pipeline
that silently returns defaults and you will conclude the corpus was useless — which is exactly what
F2 sets you up to conclude.
**How:**
1. Add a `record_type` filter to `FP3Retriever.retrieve()` so `ViralScript` and `PromptAtom` can
   never be confused, and make `PromptAtom` unretrievable by the GRAFT path.
2. Make the extraction path **fail loudly**: if a retrieved record has no `hook_structure`, raise or
   return `graft_applied=False` — never fall back to a literal. A constant returned as if it were
   learned structure is worse than an error.
3. Fix [test_graft.py:58](../../tests/test_graft.py#L58) to assert against real index content, and
   add the missing `index → retrieve → extract` integration test.
**Verdict:** Do this before any corpus work. It is a prerequisite, not a task.

### A2. Use a human-scored narrative rubric as the external anchor

**What:** DramaChain Bench's 63 leaf dimensions across 5 axes, built on 17,488 professional human
scores, with an Agentic Judge at PLCC 0.918 `[V]`.

**Why this one:** Your current plan is to calibrate QualityGate against 30 scripts *you* annotated —
which makes the scorer a mirror of your own taste, with no external validation. DramaChain's rubric
was built by professional annotators and validated against human rankings. It is the only external
anchor available in this exact domain, and it covers the full chain (script → storyboard → keyframe →
shot video → finished drama), so it can grade every stage you produce.

**How:**
1. Replace the nine regex dimensions in [scorer.py](../../flowbeast/observe/quality/scorer.py) with an
   LLM judge prompted against DramaChain's leaf dimensions (or a subset you can afford to run).
2. Calibrate on their human scores rather than on your own annotations.
3. Keep the score **visible and named** — see §C3.
4. **Persist every audit as a structured record** (`{script, dimension_scores, judge_model,
   rubric_version, timestamp}`), so the 19 existing audits plus every future one become a re-scorable
   dataset. Then re-scoring after a rubric change is a batch job, not a re-run — this is exactly what
   [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) (UK AISI, MIT) provides:
   `inspect eval --no-score` stores the transcripts, `inspect score --scorer` re-scores them later.
   Adopt the *pattern* (separate generation from scoring) even if you do not adopt the library.
**Caveat:** the dimensions and judge are a *planned* release. Verify availability before betting the
roadmap on it. **Fallback:** if unavailable, use the paper's published axis definitions (the paper
describes them) or annotate 30 scripts against a simplified 10-dimension rubric derived from it.

**What to expect from an LLM judge — set this before you build it.** LitBench
([arXiv 2507.00769](https://arxiv.org/abs/2507.00769)) is the cleanest public measurement of how
well judges agree with humans on creative-writing preference:

| Judge | Agreement with human preference |
|---|---|
| Best off-the-shelf judge (zero-shot, no training) | **73%** |
| Trained Bradley-Terry reward model | **78%** |

73% is the realistic ceiling for the first version. That is *usable* — it is far above the current
scorer's zero-information output — but it means the score must never be presented as ground truth.
It is a noisy ranking signal.

**Three judge-bias traps, all measured, all cheap to avoid:**

1. **Pairwise vs pointwise.** Pairwise judging flips its verdict on **35%** of pairs when the two
   candidates are merely swapped in order; pointwise flipping is **9%**
   ([arXiv 2504.14716](https://arxiv.org/abs/2504.14716)). If you compare two scripts, run **both
   orders** and treat disagreement as "tie", or score each script independently and compare numbers.
2. **Rubric drift on Chinese text.** Judge agreement degrades measurably outside English; a Chinese
   short-drama rubric must be validated on Chinese scripts, not assumed to transfer.
3. **Self-consistency is not accuracy.** A judge can be perfectly consistent (CAR ≈ 0 across runs)
   and still be wrong ([arXiv 2602.07996](https://arxiv.org/abs/2602.07996)). Consistency checks
   cannot substitute for the human labels in A3.

**Verdict:** Highest-leverage external asset found in this entire research pass.

### A3. Replace the calibration statistics — and anchor them to humans

**What:** `scipy.stats` for the correlation in
[calibrator.py](../../flowbeast/observe/quality/calibrator.py), plus the correct estimator for the
weights (F6 rules out the current one).

**Why:** `_pearson_corr` is hand-written and reports no significance. More importantly, the
current weight formula is circular (F6), so swapping in `scipy` without changing the estimator
would produce the same meaningless weights with a p-value attached — which is worse than now,
because it would *look* rigorous.

**How:**
1. **Fix the estimator first.** Correlate each dimension against a total that **excludes** that
   dimension, or drop the correlation approach entirely and fit weights by regression / ranking
   against a held-out human-labelled set. Sanity check: run it on shuffled labels. If the weights
   survive shuffling, the estimator is still circular.
2. **Use exact statistics, not asymptotics.** With n = 30 there is no room for normal
   approximations. Everything needed is in the Python standard library or `scipy`:
   - **Clopper-Pearson** exact binomial CI — `scipy.stats.beta.ppf`
   - **Exact binomial sign test** for "is A better than B" — `scipy.stats.binomtest`
   - **Bootstrap** for score differences — `numpy.random.default_rng().choice`
3. **Label 30 scripts by hand, and report agreement.** 30 labels is enough to detect a large
   effect and to compute a kappa against the LLM judge. Report the kappa. If it is below ~0.4, the
   judge is not measuring what you think it is, and no amount of pipeline work will fix that.

**Sample-size arithmetic — read this before running any A/B test:**

| Goal | n needed |
|---|---|
| "7 of 10 preferred A" — first signal | **n = 30** (21/30 needed for p < 0.05) |
| Detect a 0.3-point shift on a 5-point scale | **n ≈ 174 per arm** |
| Number of comparisons to run at n = 30 | **one** |

At n = 30 you get **one** comparison. Test the score against *one* hypothesis. Testing five
variants and reporting the winner inflates the apparent effect by ~10.6 points (winner's curse:
E[max] of 5 standard normals ≈ 1.163), and at n = 30 that inflation is larger than most real
effects you are trying to detect.

**What this buys you:** a number you can put in front of a customer. "Our scorer agrees with
professional human raters at κ = X on 30 hand-labelled scripts" is a claim. "Our AI scores your
hook 87/100" is not.

**Verdict:** Trivial to implement, and it is the difference between a scorer and a demo.

### A4. Measure corpus diversity — Vendi Score, not vector count

**What:** [Vendi Score](https://arxiv.org/abs/2210.02410) — `exp(von Neumann entropy of the
similarity matrix)`, i.e. the **effective number of distinct modes** in a set. Reference
implementation `vendi-score` (MIT).

**Why this one:** the corpus is the moat *if* it is diverse. `index.ntotal` says 60 — it does not
say whether those 60 are 60 different patterns or one pattern written 60 ways. Given that GRAFT
returns a constant, "one pattern written 60 ways" is the live hypothesis, and there is currently
no way to tell. Vendi is ~5 lines on top of the existing embedding matrix, has no training, and
returns an interpretable number ("your corpus has 4.1 effective patterns, not 60").

**How:**
1. Load the existing FAISS vectors (they are already normalized in the store).
2. Build the n × n cosine similarity matrix, compute its eigenvalues, exponentiate the entropy.
3. **Track it as a headline number next to `ntotal`** — it belongs in the same place the gate score
   does (§C3). "60 units, 4.1 effective patterns" is the sentence that tells you what to do next.
4. **Add `hook_type` entropy** as the cheap companion check — a Shannon entropy over the
   `hook_type` field of the corpus. If GRAFT always returns `冲突爆发`, this number will show it
   immediately, without needing to run a single generation.

**Note on scope:** this is measurement, not a new subsystem. It adds no new pipeline stage and no
new dependency beyond `numpy` (which you already have).

**Guardrail:** do not build a new evaluation system. A2 is a *replacement* of `scorer.py`'s internals,
not an addition alongside it. A4 is a *measurement added to the existing store*, not a new module.
If it is not replacing regex-with-LLM-judge, it is scope creep.

## B. Build the corpus factory

Only after Part A. The goal is to turn "type the transcript by hand" into an automated pipeline, and
to stop building a corpus that already exists.

### B1. Do not build the corpus — import it

**What:** SkyScript-100M (shot descriptions, highlight scores, emotion states, camera details from
6,660 real short-drama episodes) and M-Drama (9,138 annotated micro-drama clips) `[V]`.
**Why:** This is the single largest time-saver available. Building a 30-script hand-annotated corpus
takes weeks and produces something strictly worse than what is already downloadable.
**How:** Download, map their fields onto `ViralScript`, and treat them as a *reference distribution*
— not as your product's memory. They give the scorer something to be anchored against (A2).
**Caveat:** verify licenses before any commercial use. SkyScript is HUST + Kunlun/SkyWork; check
whether the release permits commercial redistribution, and keep it out of anything you ship as an
asset.

### B2. Automate transcript extraction for the dramas you *do* watch

**What:** An ASR + scene-detection pass to replace manual transcript typing.
**Why:** F3. The manual step is the actual bottleneck, not the analysis.
**How:** There are mature open-source options for both ASR and shot/scene boundary detection; the
specific tool selection is covered in the accompanying tool research (see Appendix B). The target is
one command: video file in → draft `transcript.txt` + scene boundaries out → you correct rather than
transcribe.
**Verdict:** Do this only if you decide to keep watching and mining dramas yourself. If B1 gives you
enough, skip it.

### B3. Buy extraction instead of building it, for scale

**What:** BytePlus `las_short_drama_script_gen` at **~$0.21 per input-video minute** `[S]`.
**Why:** At $0.21/min, a 90-minute drama costs ~$19 to convert to a script. That is cheaper than one
hour of your time, and it is ByteDance's own short-drama-tuned model.
**How:** Use it as the *bulk* path and reserve human annotation for the 20–30 dramas you care most
about. Note the irony: this is the same capability you were going to build. Buying it is the correct
application of the never-reinvent-the-wheel principle.
**Verdict:** Strong buy. Costs ~¥140 for a batch of 10 dramas.

## C. The last mile — closing the loop to a finished video

### C1. The boundary in `decisions/002` blocks validation, and should be narrowed

[decisions/002](decisions/002_what_we_do_not_do.md) §1 forbids video-generation code and §4 forbids
publishing/analytics. Those boundaries were written to stop FlowBeast drifting into being a worse
video tool.

**The problem:** without ever producing a finished video, you cannot observe retention, and without
observing retention you have no feedback signal — which is the entire content of Part 0. The rule
protects the architecture and starves the moat.

**The resolution:** a **thin, disposable validation harness** that lives outside the product and is
never imported by `flowbeast/`. It calls an external video API, posts the result, reads back the
numbers, and writes them into `feedback_ingest`. It is a measuring instrument, not a feature. Draw
the boundary at "this code must never become a dependency of the core," not at "we never render a
video."

### C2. Rent the last mile; do not build it

**What:** Volcengine Ark / Seedance for generation, DashScope CosyVoice for narration, FFmpeg for
assembly. Every one of them is a rent, not a build.
**Why:** Generation cost is falling and will keep falling. MiniMax API list is **¥0.50/sec at 768p**,
**¥0.025/image**, **¥3.50/万字符 TTS** `[S]`; a 60-second episode's raw video cost is roughly ¥30.
Anyone pricing on "we save you generation cost" is anchored to a falling number. Rent, and keep the
integration behind an interface.
**Caveat:** DramaChain found the top configuration was **gpt-5.5-xhigh + gpt-image-2 + seedance-2.0**
at 3.30 vs the >3.0 usable line `[V]`. That is a useful starting point for model selection, but it is
a single benchmark on their task distribution — re-verify on your own content before standardizing.

#### C2.1 The generator: Volcengine Ark, and why it costs zero integration work

**What:** `seedance-2.0` through **Volcengine Ark** — `https://ark.cn-beijing.volces.com/api/v3`,
OpenAI-SDK compatible `[V]`.
**Why this one over the aggregators:**
- **`openai>=1.0.0` is already a dependency** ([pyproject.toml:16](../../pyproject.toml#L16)). There is
  nothing to install; it is a base-URL change.
- China-first: no cross-border payment, no proxy, no currency risk for a CN-market wedge.
- **Failures are not billed**, which matters when you are iterating on prompts — the failed generations
  are exactly the ones you generate most of while tuning.
- Token billing is a published formula, so per-episode cost is computable *before* you hit send.
- `camera_fixed` / `ratio` / `duration` map **1:1 onto the `shots[]` array** that
  `flowbeast/drama/pipeline.py` already emits (21 shots / 85s in the current run).

**Kling 3.0 is the control-maximizing alternative** `[V]`: its multi-shot grammar accepts a `shots[]`
list natively, which is a direct structural match to FlowBeast's own shot array — the compiler's output
is already 90% of Kling's input schema. ToS §6.4 permits commercial use. It costs roughly 2.4× Ark at
1080p ($9.52 vs $5.94 for 85s), so it is a *quality tier*, not the default.

**How:** Build the render layer as a **sibling of the provider layer** — `flowbeast/render/` with
`get_video_backend()` dispatching on a new `settings.VIDEO_BACKEND`, mirroring the existing
`AUDIO_PROVIDER = "edge"` switch in [pipeline.py](../../flowbeast/drama/pipeline.py) and the
`MODEL_PROVIDER` dispatch in [flowbeast/core/providers/\_\_init\_\_.py](../../flowbeast/core/providers/__init__.py).
Add `ARK_API_KEY` / `ARK_BASE_URL` to [config.py](../../flowbeast/core/config.py) alongside the
existing per-provider keys.

**Verdict:** ADOPT. This is the cheapest possible path to a finished video and it adds no dependency.

#### C2.2 The narration and the captions — a 6-line change unlocks the whole finish

**This is the highest-leverage finding in the entire research set, and it is not a new tool. It is a
bug in your own file.**

**What:** `edge-tts` already emits **word-level timestamps**, and
[flowbeast/drama/audio.py:79](../../flowbeast/drama/audio.py#L79) throws them away by calling
`await communicate.save(...)`.

**Why it matters:** `[V-live]` I ran edge-tts 7.3.1 (the pinned version) against the 20-character line
`她跪在暴雨里，手里攥着那份亲子鉴定报告。` and it returned **12 `WordBoundary` events with
100-nanosecond tick offsets** — e.g. `('暴雨', offset=6125000, duration=4375000)` = 0.6125s → 1.05s.
That means accurate captions and shot-cut-to-narration sync are available **today, at zero cost, with
zero new dependencies and zero GPU** — and they are *more* accurate than ASR, because you already know
the text you asked it to say.

**One precision that matters for implementation** `[V-live]`: the boundaries are **word-level, not
character-level**. `暴雨` and `手里` each arrive as a single token. Character-by-character `\kf` karaoke
therefore requires interpolating a token's duration across its characters (proportional or even split).
Plan for that — it is the difference between "captions work" and "captions look wrong at 2× speed."
Also confirmed: punctuation (`。`, `，`) is stripped from the boundary text, which is the second reason
captions must be re-derived from the source script rather than concatenated from events.

**How** — the whole change:

```python
communicate = edge_tts.Communicate(text, voice=EDGE_VOICE, boundary="WordBoundary", ...)
submaker = edge_tts.SubMaker()
with open(mp3_path, "wb") as f:
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            f.write(chunk["data"])
        elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
            submaker.feed(chunk)
srt = submaker.get_srt()
```

**Two traps**, both verified:
1. `Communicate.__init__` defaults to `boundary="SentenceBoundary"` (`communicate.py:335`). Omit the
   argument and you silently get sentence granularity.
2. **Punctuation is dropped from the boundary text.** Captions must be re-derived from the source
   script by alignment, not concatenated from the boundary events.

**Verdict:** ADOPT — **before anything else in Part 2.** Two days of work currently stands between
FlowBeast and a properly-finished video; this removes most of it.

**Then the captions themselves:** `pysubs2` (MIT, py≥3.12) → ASS with `\kf` karaoke tags →
`ffmpeg -vf "ass=cap.ass:fontsdir=/app/fonts"`.
[audio_assembly.py](../../flowbeast/drama/audio_assembly.py) **already shells to ffmpeg at lines 68 and
93**, so the marginal cost is one filter. Ship **Noto Sans SC** (OFL) with it — never 微软雅黑 (see A.6).

**Line-breaking is the one piece you must own** `[V]`: BudouX (Apache-2.0, py≥3.10) plus a 避头尾
(kinsoku) table is ~50–100 lines. Nothing off-the-shelf does Chinese line-breaking headlessly, and
without it burned-in captions break in the middle of words.

#### C2.3 The assembly: FFmpeg, and the Dockerfile is currently broken

**What:** FFmpeg as the rendering core — `overlay` → `xfade` → `ass` → `sidechaincompress` → `loudnorm`.
**Why:** Zero license, zero sidecar, zero telemetry, one pass. `[V-live]` local ffmpeg 6.1.1 has
`enable-libass` and working `ass`/`subtitles` filters. **Remotion's license cliff is headcount, not
revenue** — free at ≤3 people including contractors, paid at 4+ `[V]`; decide that before architecting
around it. There is no pure-Python render path worth using.

**The blocker:** `[V-live]` the Docker production stage is `python:3.12-slim` with **no ffmpeg and no
fonts**, yet `audio_assembly.py` calls `ffmpeg` via subprocess. **The capture step cannot work in the
shipped image today.** One line fixes it:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*
```

**The ducking chain**, verified working — narration side-chains the music so dialogue stays intelligible:

```
[2:a]volume=0.35,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[bgm];
[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[nar];
[nar]asplit=2[narmix][narside];
[bgm][narside]sidechaincompress=threshold=0.03:ratio=8:attack=5:release=250:makeup=1:level_sc=1:detection=rms[bgmduck];
[narmix][bgmduck]amix=inputs=2:duration=longest:normalize=0[mixed];
[mixed]loudnorm=I=-14:TP=-1.5:LRA=11[outa]
```

**Design BGM as a replaceable slot.** Every music source has a rights trap (A.6); making the track
swappable in-app lets the operator drop in a 抖音-library track they already have rights to.

#### C2.4 What the whole last mile actually costs

85-second vertical 1080×1920 `[V]`:

| Component | Cheap path | Cost | Premium path | Cost |
|---|---|---|---|---|
| Character refs | text-only prompts | $0 | Nano Banana 2 × 3 chars | $0.24 |
| Video generation | Vidu Q3-turbo 1080p off-peak | **$2.60** | Kling 3.0 1080p + native audio | $14.28 |
| Narration | DashScope `cosyvoice-v3-flash` (~400 chars) | $0.006 | Doubao TTS 2.0 + 声音复刻 | ~$0.20 |
| Timestamps | edge-tts `WordBoundary` | **$0** | same | $0 |
| Captions + karaoke | pysubs2 → ASS → libass | **$0** | same | $0 |
| Lip-sync pass | — | $0 | MuseTalk 1.5 on a rented 4090 | $0.15 |
| Music + SFX | Freesound CC0 | $0 | ElevenLabs Music + SFX | $0.25 |
| Assembly, ducking, loudnorm | FFmpeg | **$0** | same | $0 |
| Compliance label + C2PA | ffmpeg drawtext + `c2patool` | $0 | same | $0 |
| Publish | `social-auto-upload` | $0 | 快手 official API | $0 |
| **Total marginal cost** | | **≈ $2.61 ≈ ¥18.7** | | **≈ $14.88 ≈ ¥106** |

**The takeaway: video generation is ~99% of unit cost.** Everything else in the last mile — TTS,
timestamps, captions, assembly, ducking, loudness, labeling — totals under $0.30 and drives to ~$0.
**If you need to cut cost, cut it in the generator** (Vidu off-peak, Seedance mini, Kling 2.6), never by
degrading the finish. A well-captioned, correctly-ducked, loudness-normalized video with mediocre footage
outperforms the reverse on 抖音, where sound-off viewing makes burned-in captions near-mandatory.

**`DASHSCOPE_API_KEY` and `DASHSCOPE_BASE_URL` already exist in
[config.py](../../flowbeast/core/config.py)** `[V-live]`. CosyVoice is a config branch, not a build.
At volume, self-host **CosyVoice3-0.5B** (Apache-2.0).

#### C2.5 Two build-order priorities that come before any new feature

1. **Fix [audio.py:79](../../flowbeast/drama/audio.py#L79)** — `save()` → `stream()` with
   `boundary="WordBoundary"` + `SubMaker`. ~6 lines. Unlocks every caption and every shot-to-narration
   sync in the product.
2. **Add `ffmpeg` + `fonts-noto-cjk` to the Dockerfile.** The shipped image cannot render audio today.

Both are preconditions for §C3 (shipping a finished artifact) and for §3.3's two-day fix.

### C3. Ship the score as a named, visible artifact

**What:** OpusClip's **Virality Score 0–99** (hook strength, emotional flow, perceived value, trend
alignment — Hook/Flow/Engagement/Trend tabs) is the reason people pay $15–29/mo `[V]`. It is a black
box; a reviewer measured only ~60–70% hook accuracy `[S]`. **It is still the product surface.**

**Why this matters for FlowBeast:** QualityGate is currently internal, regex-based, and returns
REJECT 100% of the time. Nobody in the market has a **legible, named quality gate for AI-generated
narrative** — that is the least-copied part of the FP3 thesis. OpusClip proves people will pay for a
single legible score even when the score is imperfect.
**How:** Give the score a name, surface it on every output, and show what changed between runs. The
value is the *comparison*, not the number.
**Verdict:** High. This is packaging, not engineering — and it is the cheapest differentiator
available.

## D. Distribution and trend intelligence

### D1. Steal Alison.ai's Preflight pattern

**What:** Alison ships **Preflight Plus** — free, **no credit card, no connected ad account, results
in ~30 seconds** — grading any video against Google's ABCD framework and Meta/LinkedIn best practices
`[V]`. A funded company chose a *scorer* as their free wedge.
**Why:** It is the cleanest PLG motion in this market: the free tool is the product's core
capability applied to a user's own asset, with zero onboarding friction and an instant result.
**How:** A public, no-signup page: paste a topic or drop a script → get the drama score with
per-dimension breakdown. Rate-limit and cap spend before exposing it (`api/main.py` currently lets
any visitor trigger a real LLM call).
**Verdict:** Strong. This is the highest-conversion shape available for what FlowBeast already is.

### D2. Sell unattended throughput, not single generations

**What:** Revid.ai's **"Auto-Mode workers"** — scheduled, unattended production — is a paid tier
feature `[V]`. Revid also ships **API + MCP server + CLI on every plan**, including the $39 tier `[V]`.
**Why:** One-off generation is a commodity. Recurring, scheduled output is a subscription. And
putting the API on the cheapest plan (rather than gating it to enterprise) is how they get embedded
in other people's workflows.
**How:** A minimal MCP server exposing the compiler is a small amount of work on top of the existing
FastAPI surface, and it puts FlowBeast inside Claude/Cursor/agent workflows where creators already
are. `capability_map.md §9` already identifies the FastAPI endpoints as the surface webhook/MCP should
grow from. Register at [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/).

**Ranked by leverage, with real effort estimates** `[V]`:

| Surface | Effort | Verdict |
|---|---|---|
| **MCP server** (official registry) | **8–16 h** | **ADOPT** — reaches exactly the agent-using audience that wants a prompt compiler |
| **Claude Code plugin/skill** | **4–8 h** | **ADOPT** — nearly free, same audience. *Owner-only submission on Team/Enterprise, and the first org to submit a repo folder holds the listing permanently — submit from the org that should own it long-term* |
| **n8n community node** | 16–40 h | TRIAL. **Hard requirement: from 2026-05-01, nodes submitted for verification must be published via GitHub Actions with a provenance statement — local-machine publishes are rejected** `[V]` |
| ComfyUI node | 20–40 h | WATCH — ComfyUI users are image/video-first, weak fit |
| Dify plugin / Coze plugin | 16–24 h | WATCH — Coze's mainland monetization needs a business entity |
| VS Code / Chrome extension | 20–40 h+ | SKIP — poor fit for a batch compiler |

These three (MCP → Claude Code skill → n8n) share one HTTP client and reach people who already pay
for AI tooling. Note the contrast with §3.1 Wedge 3: `LeCheung/ai-shortdrama-toolkit` built a
*marketing* funnel and got 0 stars; these are *integration* surfaces that put the tool where work
already happens.

### D3. Watch trends as a feature, not a data pipeline

**What:** Revid gates **trend-watching by tier** — "Watch 5 channels for viral ideas" vs "Watch 50"
is literally a paid feature `[V]`. They also run a wall of free SEO surfaces: TikTok Hooks Library,
"Most Viewed TikToks (100M Club)", Viral Video Rankings, TikTok Trends Today.
**Why:** Trend data feels like a heavy infrastructure project. Competitors ship it as a **tier
differentiator** — the count of watched channels is the pricing axis, not the sophistication of the
signal.
**How:** Start with a small number of manually-tracked sources surfaced inside the product UI.
Do not build a trend-ingestion pipeline before you have paying users.

### D4. Publishing in China is browser automation, not an API

**This is the finding that most changes what "last mile" means.** §3.2 says the compounding asset is
channel-owned telemetry. This is what stands between you and that channel.

**What:** [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) — **15,506★,
MIT** `[V]`. Browser-automation upload to 抖音 / 视频号 / 小红书 / B站 / 快手 via a CLI (`sau douyin
upload-video …`).

**Why it is the only route** `[V]`:

| Platform | Official publish API | The gate |
|---|---|---|
| **快手** | ✅ Yes | **The cleanest official route.** Cleanest of the four — use this one first |
| **抖音** | ⚠️ Exists | **≥¥500,000 registered capital AND an enterprise registered ≥1 year. 个体工商户 excluded.** This is a company-formation problem, not an engineering problem |
| **视频号** | ❌ None | — |
| **小红书** | ❌ None | — |

**Why this matters strategically:** the 抖音 API bar means the *official* route to the largest short-drama
platform is closed to a solo operator, regardless of what you build. Two consequences:

1. **The wedge in §3.1 must sell to teams that already clear the bar**, or route through 快手, or publish
   on the customer's behalf through *their* enterprise account. Do not architect a product whose only
   distribution path requires the customer to be someone you are not.
2. **Browser automation works but is fragile and against some platforms' ToS** — treat it as a
   customer-side convenience, never as a guaranteed product SLA. Do not promise unattended posting.

**Globally:** `upload-post` ($16/mo, `pip install upload-post`) is a real API with a Python SDK and
maps `is_aigc` / `containsSyntheticMedia` fields `[V]`. The contrast is stark — outside China this is a
$16/month solved problem.

**Verdict:** ADOPT for the customer-facing path, but **price and promise around 快手 and manual export**,
and treat 抖音 automation as best-effort. The gating constraint is legal entity, not code.

### D5. Compliance labeling is a hard gate, not a feature

**What:** Two Chinese regulations now apply to every AI-generated video you produce `[V]`:

- **《人工智能生成合成内容标识办法》** (CAC, in force 2025-09-01). **Art. 4 requires the label at the
  starting frame** — an explicit, perceivable mark, not a description in the caption. **Art. 10 prohibits
  removing or concealing labels** — so a pipeline that strips labels downstream is itself the violation.
- **GB 45438-2025** — the labeling standard that specifies the mark.
- **《微短剧发展管理办法》NRTA Order No. 16**, effective **2026-09-01** — pre-broadcast review and a
  节目编号 (program number) regime for 微短剧.

**Why it matters commercially:** this is simultaneously a **risk and the strongest argument for
FlowBeast's existence**. A tool that emits a compliant, correctly-labeled, correctly-metadata'd video by
default is selling regulatory safety, not just speed. Chinese short-drama teams are about to need this
and most of them are assembling pipelines out of DeepSeek + 即梦 + 剪映 by hand `[S]`.

**How:** Burn the AI overlay with ffmpeg `drawtext` **and** embed C2PA metadata (`c2patool`) — the C2PA
embed additionally triggers auto-labeling on TikTok / Meta / LinkedIn / Pinterest `[V]`. Both cost $0 and
belong in the same FFmpeg pass as §C2.3. Ship it **on by default, not as an option**.

**The open legal question, flagged honestly** `[UV]`: **Order 16's Art. 2 language points to serialized
drama, and Art. 33(3) suggests platform-level handling — so it is not established that a
non-serialized 60–90s AI story video counts as 微短剧** and therefore requires a 节目编号. Resolve this
before making compliance a headline claim. GB 45438-2025's exact parameters (wording, corner, minimum
font height, opacity, duration) must be read off [openstd.samr.gov.cn](https://openstd.samr.gov.cn) before
hard-coding a watermark — do not guess them from secondary sources.

**Verdict:** Build the label into the render pass now. It is free, it is required, and it is sellable.

## E. Commercial plumbing — gateway, cost, and deployment

### E1. LiteLLM proxy — and a correction to `capability_map.md`

**What:** Self-hosted OpenAI-compatible gateway (MIT, SOC 2 Type II) in front of 100+ providers.
Virtual keys, per-key `max_budget` + `budget_duration`, `rpm_limit`/`tpm_limit`, spend logs,
fallbacks, caching, and a UI. **It also serves `/v1/embeddings`.** `[V]`

**Why:**
- [capability_map.md §7](capability_map.md) marks the hand-written provider registry as correct —
  "✅ 这个写得对, 7 家厂商统一抽象." The abstraction *is* well-written. **But it implements none of the
  metering layer.** `flowbeast/api/main.py` has zero rate limiting, auth, budget, quota, or token
  counting — I confirmed by grepping `rate.?limit|slowapi|budget|quota|api_key|auth|usage|token_count`
  across `flowbeast/api/` and `flowbeast/hooks/`. LiteLLM is that entire missing layer.
- It is also the mechanism that makes §D1 (a free public scorer) safe to ship. Right now **any
  visitor can trigger a real LLM call with no cap.**
- **Verified Chinese provider support:** `deepseek`, `dashscope`/qwencloud, `zai` (Zhipu), `moonshot`,
  `minimax`, `volcano`/Volcengine — plus ollama, openrouter, gemini, anthropic, openai. `[V]`

**How:** Stand up Postgres (Neon or Supabase free tier) → deploy the proxy → port
[openai_compatible.py](../../flowbeast/core/providers/openai_compatible.py) to
`litellm.completion(model="deepseek/deepseek-flash", ...)` → mint one virtual key per public surface
(Streamlit, API, MCP) with `max_budget: 5`, `budget_duration: "30d"`, and an `rpm_limit`.

**Cost:** $0 software. **4–8 hours.**

**Caveat:** semantic caching is documented as unsafe for multi-turn/agentic traffic — consecutive
turns score ~0.99 similar. FlowBeast's topic→package flow is single-shot so it fits, but set
`"cache": {"no-cache": true}` on any agent or retry keys.

### E2. Kill the Ollama dependency — the "768-dim blocker" is a myth

`capability_map.md §2` frames the embedding switch as a project: it says changing `EMBED_PROVIDER`
without rebuilding the index hits a FAISS dimension mismatch, and lists "换成托管 embedding 厂商 →
按新维度重建索引" as a multi-step plan. **The actual numbers:**

```
magic 49784632   d (dims) 768   ntotal 60   file bytes 184365
```

**Sixty vectors.** `fp3_meta.json` holds 60 entries. Re-embedding them is ~12,000 tokens —
**$0.0002 at Voyage-4-lite rates, i.e. covered entirely by their free tier**, and seconds of runtime.
There is no migration project. Under the free tiers below, the embedding bill is **$0 for years.**

**The best answer is not an API at all.** `[V]` **fastembed** (Qdrant's ONNX Runtime wrapper,
Apache-2.0) ships **`nomic-ai/nomic-embed-text-v1.5-Q` — 768 dimensions, 130 MB ONNX, Apache-2.0** —
which is *the same model family your index is already built on*, quantized. In-process, no daemon, no
GPU, no torch, milliseconds per call on CPU.

| Option | Dims | Cost | Note |
|---|---|---|---|
| **fastembed `nomic-embed-text-v1.5-Q`** | **768** ✅ | **$0, in-process** | **Recommended.** Same model family as the current index — *the index shape does not change.* 130 MB ONNX. Built for serverless |
| fastembed `nomic-embed-text-v1.5` (full) | 768 ✅ | $0 | Same, 520 MB, maximum fidelity |
| `voyage-4-lite` (API) | 1024 | $0.02/M, 200M free `[V]` | Strong multilingual, but changes index shape for no gain here |
| Alibaba `text-embedding-v4` (API) | 768 configurable ✅ | ~$0.072/M, 1M free | Zero index churn — the best *hosted* option |
| `bge-m3` (SiliconFlow / Novita) | 1024 | $0.01/M | Chinese workhorse; 实名认证 required |
| `nomic-embed-text` (Ollama, **current**) | 768 | $0 local | **The deployment blocker** — a daemon on `localhost:11434` |

**This supersedes the API-first recommendation.** `sentence-transformers` is the wrong shape (PyTorch
drags in hundreds of MB to >1 GB installed and dominates image size and cold start). fastembed gets to
768 dims with no network, no daemon, and no dimension migration — which means **E2's "re-embed the 60
vectors" step becomes a verification step rather than a migration.** Keep the same acceptance test
either way: existing `uv run pytest tests/ -q` passes and existing index queries return the same top-k.

**One useful side effect** `[V]`: fastembed also carries **rerankers** (`cross-encoder/ms-marco-MiniLM-L-6-v2`,
0.08 GB; `jina-reranker-v1-turbo-en`, 0.15 GB) at negligible cost. A reranker pass is a cheap quality win
for §A2's retrieval and worth wiring behind the same interface.

**And a dead end worth not exploring:** Ollama Cloud exists ($20/mo Pro) but its catalog is
**chat/generation models only — there is no embedding model of any kind** `[V]`. There is no hosted
drop-in for your current call.

**Three code fixes in [store.py](../../flowbeast/fp3/store.py) and
[config.py](../../flowbeast/core/config.py):**
1. `FP3Store.__init__` calls `embed_text("probe")` to auto-detect `dim`, then `load()` immediately
   overwrites `self.index` from disk — **a wasted network round-trip on every instantiation.**
2. Because of that overwrite, a provider switch surfaces as a **FAISS assertion at `search()`**, not
   at init. Add an explicit `assert index.d == configured_dim` in `load()`.
3. `_embed_vendor()` **hard-defaults to `"ollama"`** — flip it so a missing env var fails loudly
   instead of silently pointing at `localhost:11434`.

### E3. What it costs to serve 100 users/day — ~$9–14/month

**Workload model (from the real code):** 1 compile = topic → `prompt_package.json`. Input ≈ 5,000
tokens (the 1,200-token static system prompt from [prompt.py](../../flowbeast/drama/prompt.py) + trend
context + 2 FP3 examples + topic); output ≈ 2,500 tokens. Retry factor 1.3×. At 3,000 compiles/month
= 3,900 calls = **19.5M input / 9.75M output tokens.** Infra = Fly.io 512MB + 10GB volume = $5.19.

| Model | in/out per 1M | LLM/mo | **All-in/mo** |
|---|---|---|---|
| **claude-haiku-5-5** | $0.10 / $0.50 | $6.83 | **~$12** |
| **qwen3.8-flash** (DashScope) | $0.15 / $0.47 | $7.51 | **~$13** |
| **GLM-5.3-Flash** | $0.15 / $0.50 | $7.81 | **~$13** |
| **deepseek-flash** (off-peak) | $0.15 / $0.60 | $8.78 | **~$14** |
| **GLM-4.7-Flash** (free, limited-time) | $0 / $0 | $0.00 | **~$5** |
| deepseek-v4-pro (off-peak) | $0.66 / $1.98 | $32.18 | ~$37 |
| claude-sonnet-5-5 | $2.00 / $10.00 | $136.50 | ~$142 |

**With caching applied** (~22% off input + ~30% semantic hit rate): deepseek-flash off-peak drops to
**~$9.7/mo all-in**; claude-haiku-5-5 to **~$8.8/mo**.

**Two caching levers, both free:**
- **Provider-side prefix caching.** DeepSeek's cache hit is **$0.003/M vs $0.15/M miss off-peak — 50×
  cheaper.** The 1,200-token system prompt in `prompt.py` is sent on *every* call; put it **first** in
  the message array and it caches automatically. Also note DeepSeek peak pricing (01:00–04:00 and
  06:00–10:00 UTC Mon–Fri) is exactly **2× off-peak** — batch jobs should avoid it.
- **Semantic caching** via LiteLLM with `qdrant-semantic` — **`qdrant-client` is already in
  `pyproject.toml`**, so this needs no new dependency or service.

**This is the number that makes everything else work.** At ~$12/month to serve 100 users/day, a
¥10/episode price carries ~99% gross margin. The binding constraint is not cost — it is distribution.

### E4. Deployment — the ephemeral-disk problem is also not real at this size

`capability_map.md §2` lists "索引本身在临时磁盘上" as blocker #3. **The index is 184KB and the
Dockerfile already does `COPY . .`** — it ships inside the image. It is *already* a build artifact.

**Verified rate card** `[V]` — and one correction: **Fly.io's free tier is gone.** "New organizations
don't have a free tier or a monthly free usage allowance"; new accounts get a trial only, then require
a card. `shared-cpu-1x` 256MB **$2.19** · 512MB **$3.69** · 1GB **$6.70**, volumes **$0.15/GB-mo
billed even while detached or stopped**. **Fly's Managed Postgres is $38/mo — skip it and use a volume.**

| Target | Verified price `[V]` | Verdict |
|---|---|---|
| **Fly.io** `shared-cpu-1x` 512MB + 1GB volume | **$3.84/mo** | **ADOPT** — closest thing to a purpose-built box for "FastAPI + a file on disk." Scale-to-zero via `auto_stop_machines` |
| **Railway** Free | **$0/mo**, $1 credit/mo, 0.5GB volume, no card | **ADOPT** — fastest afternoon deploy. Serverless sleeps after 5–10 min idle and **the wake request may 502** — the Streamlit UI needs a retry |
| **Northflank** Sandbox | **$0/mo, always-on, "no sleeping :)"** | **ADOPT** as the free always-on option. *Free-tier volume support is `[UV]` — verify before committing* |
| **Neon** (Postgres + pgvector) | **$0**, no time limit, scales to zero, 1GB | **ADOPT** — pgvector on every plan, no add-on. HNSW capped at 2,000 dims (fine at 768). One free tier serves both LiteLLM's DB and a hosted vector store |
| **Qdrant Cloud** | **$0**, ~**1M vectors at 768 dims** | Nice-to-have. **Suspended after 1 week idle, deleted after 4** — needs a keepalive cron |
| **Hetzner CAX11 + Coolify** | ~€4.19 `[UV]` (third-party) | TRIAL — 2 vCPU / 4GB for the price of Fly's 256MB box. Highest ceiling if you'll own a server |
| **Cloud Run** | `[UV]` — **google.com was unreachable from a China-based network** | WATCH. No persistent disk, and unreachable from the target market's network |
| Render (free) | $0 | **SKIP** — 15-min spin-down + ~60s cold start + **no persistent disk on free**. Worst possible shape for an interactive compiler |
| Turbopuffer | **$16/mo minimum** | SKIP — 4× the entire hosting budget |
| Deno Deploy / AWS App Runner / Glitch / Deta / Marqo | — | SKIP — JS-only / bills while idle / dead / dead / pivoted |

**On the vector DB question: it is premature.** At 60 vectors, two years of growth at 600 vectors/month
is ~22 MB of raw vectors. **Every free tier above is large enough** — the differentiators are liveness
policy and card requirement, not capacity. Do not adopt a managed vector DB until you have more than
one instance. `qdrant-client` is already in `pyproject.toml` when you do.

**Critical path to "cloud deployed, cost-capped, no Ollama": ~1.5 days, $0–4/month.** Add `fastembed`
(E2) → write `scripts/build_index.py` so the index is reproducible → deploy to Fly/Railway → put the
corpus in object storage (Cloudflare R2: 10GB free, **zero egress**; or Tigris on Fly: 5GB free) →
stand up Postgres + deploy LiteLLM (E1) → mint metered virtual keys → turn on caching → add a
keepalive cron.

**A China-accessibility finding worth recording** `[V]`, single sample: from a China-based IP
(183.23.109.72), **fly.io, railway.com, render.com, qdrant.tech, neon.com, supabase.com,
developers.cloudflare.com, github.com and ollama.com all returned full content**, while
**`google.com` and `cloud.google.com` both timed out** in the same second. That is a direct argument
against Google Cloud as the primary host for a China-market product — and it means every vendor
recommended above is reachable from the target market's network.

## F. Pricing, packaging, and getting paid

### F1. Price per output, not per seat or per prompt

**What:** 有戏AI's model: **¥0.1/sec, <¥10/episode** `[V]`. Submagic's API: **$0.23/min declining to
$0.10/min** at volume `[V]`. Klap: pure volume tiers on clips (100/300/1,000), no credit abstraction `[V]`.
**Why:** Every recurring creator payout found in this research is **usage-metered, not one-shot**.
Per-output pricing aligns your revenue with the customer's production volume, which is the metric
they actually care about.
**How:** Define the billable unit as a finished `prompt_package.json` (or a finished episode). Keep
the credit abstraction out — Klap's simpler volume tiers are easier to understand than credits.

### F2. Credit rollover and series continuity as retention devices

**What:** Sudowrite: unused credits **roll over 12 months**, and *"ensure continuity across a series"*
is a named feature `[V]`.
**Why:** Series continuity across 60–90 episodes is the same problem short drama has, and it is the
#1 recurring technical complaint in the 漫剧 tool comparisons. Naming it as a feature is free.
**How:** `ViralScript.characters` already has `transformation_arc`. Surface cross-episode continuity
as a product capability rather than an internal data structure.

### F3. Getting paid — and the China constraint that shapes the wedge

| Option | MoR? | Headline fee | Note |
|---|---|---|---|
| **Polar** | **Yes** | ~4% + 40¢ | Developer/OSS-oriented, **usage-based billing built in.** Best fit for selling API credits solo |
| **Paddle** | **Yes** | ~5% + $0.50 | Longest-standing MoR |
| **Lemon Squeezy** | **Yes** | ~5% + $0.50 | **Now owned by Stripe** — roadmap risk, verify terms |
| **Stripe** | No | ~2.9% + $0.30 | You become merchant of record → **you own global VAT/sales-tax registration** |

Fee percentages are widely-published headline rates; **spot-check the basis points before committing.**

**For usage-based metering:** Lago (open-source, self-hostable) or Polar's built-in usage billing.
**LiteLLM already produces the per-key spend numbers that feed either** — another reason E1 comes first.

**The constraint that matters for Part 3:** 微信支付 / 支付宝 merchant accounts require a
**营业执照 (business license)**, and a personal 收款码 is not a viable product payment rail. A
mainland-hosted storefront additionally requires **ICP 备案**. `[V]`

**This does not block the recommended wedge, and the reason is structural:** a done-with-you
production engagement is invoiced to a company, not sold through a payment gateway. The friction
lands on the *self-serve SaaS* path — which is another argument for the service wedge as the revenue
engine (§3.2) and the free scorer as the distribution surface rather than a paid product.

**Also worth copying as product design, not billing infra:** OpenRouter caps free usage at
`FREE_MODEL_NO_CREDITS_RPD = 50` and `FREE_MODEL_HAS_CREDITS_RPD = 1000` `[V]`. A free tier
hard-capped at N runs/day, uncapped after a credit purchase, is cheaper to build than a real billing
stack and is enough to start.

---

# Part 3 — The shortest path to a paid outcome

## 3.1 Three candidate wedges, ranked by evidence

### Wedge 1 — Sell the closed loop to teams with revenue, priced per output

**Evidence for:** 有戏AI's numbers (§1.5); buyers are capitalized and the pain is quantified (teams
spend **80% of cost on 投流** with **<5% margin**, many dissolving within 3 months `[V — 猎云网]`);
high-ticket adjacent sales already clear **¥500–5,000 at 95%+ margin** `[S]`; repackaging measurably
works ($15→$35 = 3→8 sales/mo `[V]`).

**Counterargument:** 有戏AI is a single vendor-originated source. The category is structurally
brutal — **1.3% recoup, 0.16% Q1 hit rate, UA eats 70–90%** (§1.6). If your customer's business is
structurally unprofitable, your pricing power is capped by their survival.

### Wedge 2 — Free public scorer, monetize the metered API behind it

**Evidence for:** Alison's Preflight Plus (§D1); OpusClip's score is why people pay (§C3); metered
pricing is the proven shape (§F1); **serving this costs ~$12/month for 100 users/day (§E3)** — so a
free tier is genuinely affordable; 21st.dev hit **$10K MRR in 6 weeks with zero marketing** `[V]`.

**Counterargument:** **Being commoditized from above.** Alibaba Cloud documents a 10-dimension
screenplay quality check as a database use case; BytePlus sells extraction at $0.21/min `[S]`. Both
are hyperscalers who can price a scoring endpoint at near-zero marginal cost. And a free scorer is
trivially cloneable — AdGenius already ships a free Claude-powered **Hook Score 0–100** Chrome
extension `[S]`.

### Wedge 3 — Open-source a core piece, sell the hosted compiler

**Evidence for:** **hypit — 11K stars in under 2 months, and an immediate 闲鱼 economy: ¥95 for
materials packs, ¥100 for deployment services** `[S]`. That is *observable, priced* willingness to
pay generated purely by open-sourcing. **Pixelle-Video (Alibaba AIDC): 5,136 stars in one week** `[S]`.
ComfyUI: open source → $30M raise at $500M valuation `[U]`.

**Counterargument:** no verified revenue exists for *any* paid ComfyUI node pack, any MCP server
maker, or any OSS→paid conversion above. **<5% of MCP servers are monetized** `[V]`. And the decisive
negative: **LeCheung/ai-shortdrama-toolkit** — a direct FlowBeast clone with a *complete* funnel
(free 10 Viral Hooks + Shot-List lead magnet, free in-browser Hook Generator, 8 SEO guides including
Chinese-language targeting of 短剧提示词/即梦/可灵/Seedance, paid packs at $19–39) — has **0 stars, 0
forks, 11 commits** `[V]`.

Open-sourcing buys distribution. **Distribution is not revenue**, and that competitor shows a
well-executed funnel does not create an audience by itself.

## 3.2 Recommendation

**Wedge 1 as the revenue engine. Wedge 2 as the distribution surface. Wedge 3 only if it serves
Wedge 1.**

The combination that follows from the evidence: **sell done-with-you AI short-drama production to
small Chinese teams at a per-episode price, with a free public scorer as the top of funnel.**

Rationale:
- Teams have budget and the pain is existential, not aspirational.
- Per-output pricing matches how they already think about cost (投流 per episode).
- The free scorer is the one PLG shape proven in this exact market, and it doubles as your
  data-collection instrument.
- Every customer engagement feeds `feedback_ingest` with **real performance numbers** — which is the
  only asset in this entire analysis that compounds, and the one thing FlowBeast currently has zero of.

**Do not** position as selling prompt packs (§1.4). **Do not** use "viral genome" language (§1.3).

### On the feedback loop

The uncomfortable truth in §1.6 and §5.5: every competitor analyzed is **open-loop** — mine →
generate. `feedback_ingest` is the only step that compounds, and a feedback loop requires either your
own distribution or a customer who owns telemetry. That is what StoReel has ($34M raised, own
platform, creator revenue share, claims 22% better D7 retention `[U]`), what VidMob has (18M+
creatives analyzed, ~$0.5B valuation `[S]`), and what FlowBeast has none of.

**This is why Wedge 1 must be a service, not a SaaS.** A done-with-you engagement gets you the
telemetry a self-serve tool cannot, because you are in the room when the numbers come back. It is
also the honest answer to "how do I get distribution": you buy it with labor, at the start.

## 3.3 Before any of this: the two-day fix

**Day 1 — Make failure visible.**
- Add the `record_type` filter to `FP3Retriever.retrieve()`
- Make `_extract_hook_structure` / `_extract_conflict_pattern` raise instead of defaulting
- Fix [test_graft.py:58](../../tests/test_graft.py#L58); add the missing integration test
- Import one real `ViralScript` and verify the extracted structure is *different* for two different
  topics. If it is not, nothing downstream is worth doing.

**Day 2 — Replace the scorer's internals.**
- Swap regex dimensions for an LLM judge against a narrative rubric (A2)
- Re-score the 19 existing audit records and see whether the new scorer can produce an ACCEPT at all.
  If it cannot, the threshold is wrong — not the outputs.

**Why two days first:** both are prerequisites for learning anything from the corpus. Building the
corpus before this is spending weeks to generate an unreadable signal.

**Runs in parallel — an independent half-day, and it is not optional:** the two §C2.5 fixes
(`audio.py:79` word timestamps; `ffmpeg` + `fonts-noto-cjk` in the Dockerfile). They touch nothing in
the moat, they add no dependency, and without them **the shipped image cannot render audio at all**.
Do them on the same day as Day 1; they are the difference between a tool that emits JSON and a tool
that emits a video.

## 3.4 The 30-day shape

| Week | Focus | Exit criterion |
|---|---|---|
| 1 | Part 0 fixes + scorer replacement | Two different topics produce two different GRAFT structures; scorer produces at least one ACCEPT |
| 2 | Cloud deployment (§E4, ~1–2 days) + metered keys (§E1) + free public scorer live (Wedge 2) + real corpus imported (B1/B3) | Scorer is publicly reachable with a hard spend cap; ≥100 scorer uses from real creators; retrieval measured against a real distribution |
| 3 | Find 3 pilot teams; produce 3 episodes end-to-end with the disposable harness (C1), assembled per §C2.4 (~$2.61–14.88 each) | 3 finished, **captioned, ducked, loudness-normalized, compliance-labeled** episodes with real posted performance numbers |
| 4 | First paid engagement; `feedback_ingest` running on real data | ≥1 paying customer; ≥1 closed feedback cycle where a score change is traceable to a retention change |

The week-4 exit criterion is the whole point. Everything before it is setup for the first time
reality enters the system.

## 3.5 Reconciliation with `decisions/002`

| Rule | Status under this plan |
|---|---|
| §1 No video generation code | **Narrowed, not violated.** Disposable harness outside `flowbeast/`, never imported by core |
| §2 No PromptAtom composition engine | Keep. But note §2 also claims "retriever.py searches ViralUnit/ViralScript, not PromptAtom" — **this is factually wrong**, the index holds both and there is no type filter (F2) |
| §3 No multi-agent orchestration | Keep |
| §4 No publishing/analytics | **Narrowed.** Read-back of performance numbers on *your own* productions is measurement, not a publishing product. **Note the constraint discovered in §D4:** 抖音's official API requires ≥¥500k capital + a 1-year-old enterprise, so a *publishing product* is doubly out of scope — the customer publishes |
| §5 No general LLM wrapping | Keep |
| §6 No new abstractions without working code | Keep — and it argues against starting with B2 before A. **The §C2 render layer does not violate this:** it dispatches to a real API and produces a real file from day one, which is exactly the "working code first" condition |
| §7 No over-architecture | Keep |
| §8 No Phase 0 optimization until 30 real samples | **This rule is the reason for the current stall.** It forbids building the ingestion tooling that would produce the 30 samples. B3 (buy the extraction) is the cheapest way to satisfy it without violating its intent |

---

# Part 4 — Why this could fail

Ordered by how likely it is to actually kill the effort.

**1. The regulatory gate is a hard gate, and it is closing on 2026-09-01.** NRTA Order No. 16
(《微短剧发展管理办法》) brings pre-broadcast review and a 节目编号 regime into force; the CAC labeling
rules (Art. 4: label at the starting frame; Art. 10: removing labels is itself the violation) already
apply. This is categorically different from the market risks below — it is not a matter of competition,
it is a matter of **whether the recommended Chinese wedge is legally shippable**. Two open questions
must be resolved before compliance becomes a headline claim: whether a non-serialized 60–90s AI video
counts as 微短剧 at all (`[UV]` — Order 16 Art. 2 points to serialized drama), and GB 45438-2025's exact
mark parameters. **Mitigation is real, and it is also the opportunity:** §D5 makes the label a shipped
default, which converts a regulatory burden into a selling point most hand-rolled pipelines do not have.

**2. The name is taken by a funded competitor.** Alison.ai owns "Creative Genome," has a16z on the
cap table, and markets in the same buyer conversation `[V]`. Any "viral genome" framing enters as the
smaller version of an existing company.

**3. The core capability is being commoditized by hyperscalers.** BytePlus sells the extraction at
$0.21/min; Alibaba Cloud documents structure extraction + transfer + a 10-dim quality check as a
*database use case* `[S]`. Neither will be beaten on price.

**4. The loop is reproducible by one developer in a weekend.** `hypit` clones any viral video and
ships 100 variants `[S]`. `musabqazi/viral-script-generator` does view-outlier scoring → top-500
corpus → pgvector retrieval → ranked generation, solo `[S]`. The GRAFT/PARASITE operator formalism is
a genuine design contribution, but it is **unpatentable and trivially re-implementable once
described.**

**5. The corpus is not exclusive and the metric that matters is invisible.** Ads scrape at
$1.88/1,000 `[S]`; DataEye already indexed 250,000 dramas at ¥3,000/yr `[V]`. And **no public
conversion or ROAS data exists for competitors' commercial ads anywhere** — everyone mines the same
weak proxies (CTR, likes, days-running) `[S]`.

**6. The distribution path may be closed regardless of what you build.** 抖音's official publish API
requires **≥¥500,000 registered capital and an enterprise registered ≥1 year**, excluding
个体工商户 `[V]`; 视频号 and 小红书 have no public API at all. The route to the largest platform is a
company-formation problem, which means **the wedge must sell to teams that already clear the bar, or
route through 快手.** See §D4.

**7. The only compounding asset requires distribution FlowBeast does not have.** As §3.2. A compiler
with no channel has no flywheel, and without a flywheel the "memory" is a static prompt library that
decays as platform algorithms shift.

**8. The platforms are absorbing the job.** 即梦 now ships **Agent 模式 + 画布 (canvas)** natively `[V]`.
Revid puts API + MCP + CLI on the cheapest plan and sells auto-mode workers `[V]`. OpusClip gives away
a virality score. When the video tool becomes the agent surface with persistent context, a package
pasted into a chat box is a step behind.

**9. The premise has a brutal base rate.** 90%+ of Chinese microdramas are AI-made, ~1.3% recoup,
Q1 hit rate 0.16%, UA eats 70–90% `[S]`. "Proven viral mechanics" as the *primary* success driver is
contradicted by the market data.

**10. The first market does not use your channels.** Product Hunt: 487 of 500 SaaS launches dead;
traffic down 80% by week 2; a Harvard study of 9,746 launches found upvotes "noisy at best" `[S]`.
Chinese short-drama creators are on 小红书 and 抖音. And the one competitor who did the bilingual SEO
play targeting 即梦/可灵/Seedance got **0★** `[V]`.

**What would make it defensible:** own a channel that produces real performance telemetry (the only
compounding asset); pick a genre or language niche whose corpus cannot be reconstructed from a web
scrape; **make the feedback loop the product** — "your memory measurably improves every week" is
defensible, "we mined 250k dramas" is not; **ship the QualityGate as the visible, named artifact**,
which nobody in this market currently does; and **ship regulation-compliance as a default** — a
correctly-labeled, C2PA-metadata'd video is a legal requirement from 2026-09-01 onward that most
hand-rolled creator pipelines will not satisfy.

---

# Appendix A — Quick-reference tables

## A.1 Open source with real traction

| Project | Stars | What to steal |
|---|---|---|
| [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | **130,935** `[V]` | Ships an **agent skill** (`docs/skill/SKILL.md`) so an LLM agent can drive the pipeline; monetizes via a sponsor hosting the free tier, at zero cost to the project |
| [MoneyPrinterV2](https://github.com/FujiwaraChoki/MoneyPrinterV2) | 32,108 `[V]` | Channel-native output — posts to platforms, not just renders a file |
| [KrillinAI](https://github.com/KrillinAI/KrillinAI) | 13,065 `[V]` | The 出海 wedge: dubbing + vertical reformat, not creation |
| [NarratoAI](https://github.com/linyqh/NarratoAI) | 11,400 `[V]` | Clip selection from source footage as a first-class step |
| [hypit](https://github.com/hypit-ai/hypit) | ~11K in <2 months `[S]` | **Named viral-structure templates ≈ your operator set**; and the 闲鱼 economy it created is observable WTP |
| [Pixelle-Video](https://github.com/Ran-Chou/Pixelle-Video) (Alibaba AIDC) | 5,136 in one week `[S]` | Closest OSS product to FlowBeast. **Template-driven, not mined-from-hits-driven** — that is your differentiator, if you keep it |
| [Toonflow](https://github.com/JamStrak/Toonflow-app-jam) | ~15.5K `[S]` | Character consistency across episodes — the #1 technical complaint in 漫剧 comparisons |
| [musabqazi/viral-script-generator](https://github.com/musabqazi/viral-script-generator) | — `[S]` | Proof the architecture is a weekend project by one dev |
| [viral-hooks-skill](https://github.com/rediumvex/viral-hooks-skill) | — `[S]` | 100 hook formulas / 10 psychological triggers — **your atom library, already free** |
| [LeCheung/ai-shortdrama-toolkit](https://github.com/LesCheung/ai-shortdrama-toolkit) | **0** `[V]` | **The negative finding.** Complete funnel, correct niche, bilingual SEO — and no traction. The "build it and they will come" failure mode |
| [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) | **15,506** `[V]` | **The only working route to 抖音/视频号/小红书/B站.** MIT. §D4 |
| [redotvideo/revideo](https://github.com/redotvideo/revideo) | — `[V]` | MIT programmatic video render — the license-clean answer to Remotion's headcount cliff (§C2.3) |
| **CosyVoice 3** (Alibaba FunAudioLLM) | — `[V]` | **Apache-2.0 Chinese TTS**, the license-clean pick. `cosyvoice-v3-flash` hosted at **¥1/万字符** `[V]` |
| **LongCat-Video-Avatar 1.5** (Meituan) | — `[V-live]` | **MIT license file, confirmed by reading it.** Audio-driven, Chinese-native, anime-capable — the only clean option in the lip-sync class (§A.6) |

## A.2 Western SaaS — live pricing read 2026-10-15

| Product | Price `[V]` | What to steal |
|---|---|---|
| [Revid.ai](https://www.revid.ai/pricing) | $39 / $99→$39 / $199/mo; scale to $2,799 | Trend-watching gated by tier; free SEO tools as funnel; auto-mode workers; **API+MCP+CLI on every plan** |
| [OpusClip](https://www.opus.pro/pricing) | Free (watermarked) / $15 / $29 ($14.50 annual) | **A single legible score as the product surface**; free tier watermarked, not crippled |
| [Submagic](https://www.submagic.io/pricing) | $19 / $39 / $69/member; API $0.23→$0.10/min | **Metered API with declining per-minute rate** |
| [Creatify](https://creatify.ai/pricing) | $15 / $55 / $95 / $195; API $99 / $299 | **"Ad Clone — remake any ad from a URL"** — the best-packaged mine→recombine framing. $15.5M Series A, ~$9M ARR `[S]` |
| [Klap](https://klap.app/pricing) | $14 / $39 / $94 | Volume tiers on *clips*, no credits abstraction |
| [Sudowrite](https://www.sudowrite.com/pricing) | $10 / $22 / $44 | **Credit rollover (12mo)**; "continuity across a series" as a named feature |
| [Alison.ai](https://alison.ai/) | No public pricing — demo only `[V]` | **Preflight Plus**: free, no-signup, 30-second scorer. And the name collision |

**The pitch every one of these sells:** replacing a production team. OpusClip: "save $2,700 monthly
on editing cost." Revid: "Create a finished video without a production team." **Nobody sells
"prompts."**

## A.3 The Chinese market

| Player | What / price | Signal |
|---|---|---|
| **有戏AI** (风平智能) | Full loop; **¥0.1/sec, <¥10/episode** | **ARR >¥36M annualized from month one; 68% first-month repurchase; >80% monthly→annual** `[V, vendor-originated]` |
| **DataEye / 剧查查** | **250,000+ dramas indexed**, 750K+ professionals | **¥3,000/yr** `[V]`. "We mined 250k dramas" is not a selling point — it is a commodity |
| **StoReel** | AI microdrama platform, creator rev-share | **$34M raised Mar 2026** `[S]`; $29.99/week or $239.99/yr. **Owns distribution AND telemetry** |
| **即梦 (Dreamina)** | ByteDance; Seedance 2.0/2.5 up to 4K | **Agent 模式 + 画布 now platform-native** `[V]` |
| **MiniMax / Hailuo** | API **¥0.50/sec 768p, ¥0.025/image, ¥3.50/万字符 TTS** `[S]` | Compute is cheap and falling |
| **Douyin AI短剧 creators** | Manual chain: DeepSeek/ChatGPT → 即梦/可灵 → Runway → 剪映 | **One clip in 15 min; top teams 10/day** `[S]`. That manual chain **is** FlowBeast's job |
| **红果 (Red Fruit)** | **DAU 168M, +107% YoY** — more than iQiyi+Tencent Video+Youku+Mango combined `[V]` | Distribution volume exists |

**Market size 2026:** China short-drama ~¥90B (2025) `[V]`. AI漫剧 >¥20B (2025) → est. ¥24.3B (2026),
600+ new titles/day. Overseas AI short drama **$100M (2025) → $650M (2026)**, 6× `[V]`.

## A.4 Academic anchors worth citing

| arXiv | Contribution |
|---|---|
| **2609.00646** | **DramaChain Bench** — 63 dimensions, 17,488 human scores, Agentic Judge PLCC 0.918, **cascade finding** (§1.7) |
| 2609.07107 | M-Drama — 9,138 micro-drama clips, EMNLP 2026 |
| 2408.09333 | SkyScript-100M — short-drama shooting scripts with highlight/emotion/camera labels |
| 2606.16053 | Theory-grounded LLM annotation of TikTok engagement — hooks and direct address predict saves; response-soliciting codas predict comments; original spoken audio predicts shares `[S]` |
| 2406.06499 | NarrativeBridge — Causal-Temporal Narrative benchmark, cross-dataset generalization `[S]` |
| 2602.22299 | *Decoding the Hook* — first-3s keyframes → multimodal → GBDT predicting CPI `[S]` |

## A.5 Where the surviving money is

| Channel | Evidence |
|---|---|
| 短剧 production bundles to **teams** | **¥500–2,000/set, custom ¥3,000–5,000, 95%+ margin** `[S]` |
| Usage-metered API | Submagic $0.23→$0.10/min `[V]`; Apify **$500K+/mo payouts**, 80/20 split `[V]` |
| Creator marketplaces with per-generation payouts | Civitai **~$2.3M paid out in 2025**, top creators $100K+/yr, 70% share `[S]` |
| Freemium with no marketing | **21st.dev $10K MRR in 6 weeks** `[V]` |
| **Dead:** prompt packs | See §1.4 — every number in that table |

## A.6 Licensing traps — the list that must not be skipped

Every item here is something a reasonable person would reach for and ship by accident. These are
**commercial blockers, not preferences** — and several are actively mislabeled in secondary sources.

| Trap | Reality | Action |
|---|---|---|
| **微软雅黑 / 宋体 / 黑体 / FounderType fonts** | **Not free for commercial use.** FounderType litigates aggressively. Default fonts are silent liability | **Ship Noto Sans SC only** (OFL). Never ship 微软雅黑 |
| **InsightFace** | Code MIT, **models non-commercial**. Used by LivePortrait, Hallo2/3, HunyuanVideo-Avatar | Avoid, or swap to MediaPipe |
| **Wav2Lip / Sonic** | **Non-commercial** (LRS2 / CC BY-NC-SA). Sonic is falsely described as Apache-2.0 in Chinese blog posts | Do not ship |
| **F5-TTS weights** | **CC-BY-NC-4.0** | Do not ship |
| **VibeVoice-TTS** | Code removed from the repo; research-only | Do not ship |
| **IndexTTS 2.5** | **Bilibili Model Use License, NOT Apache-2.0** despite the HuggingFace tag. Anti-distillation §3.4(c); PRC arbitration §6 | Email Bilibili; **keep the written reply** |
| **LatentSync** | Apache-2.0 **code** vs `openrail++` **weights** — two different licenses | Legal review before use |
| **HunyuanVideo-Avatar** | License **void in EU, UK, South Korea** | CN-domestic only — and it still has the InsightFace problem |
| **Stable Audio weights** | License **terminates automatically above $1M company revenue**, plus a "Powered by Stability AI" obligation | Avoid for a venture-scale plan |
| **Suno** | Download-channel gating ⇒ a stored library is **unlicensed**; no ownership; 20–60 downloads/mo cap | Do not build on it |
| **ElevenLabs Music** | Free/Starter/Creator/Pro are **Individual Use Only** — a company needs **Scale $299/mo** | Pick the tier deliberately, before designing around it |
| **Remotion / Editframe** | **Headcount** cliff at 3→4 **including contractors**; Remotion 5.0 makes telemetry mandatory for Automators | **Decide the headcount question before the architecture** |
| **MiniMax / Fish Audio billing** | 1 Chinese char = **2 chars** (MiniMax); **per-UTF-8-byte** (Fish, 3× for CJK) | Convert before comparing headline rates |
| **Kie.ai** | **Blocks mainland China entirely by 2026-12-31** | Do not depend on it for a CN product |
| **Codec patents (H.264/HEVC/AAC)** | Excluded from both Remotion's and FFmpeg's licenses | Moot for platform upload; **never ship your own encoder** |

**The pattern to internalize:** in this stack, the *hosted API* and the *open weights* frequently carry
different licenses, and Chinese blog posts misreport the weights one. Verify by reading the LICENSE file
in the repo, not a mirror's tag.

---

# Appendix B — Research still landing

The following tool-level research was commissioned alongside this document. Each lands as a subsection
under Part 2 with the same what/why/how/verdict format:

| Area | Landed under | Status |
|---|---|---|
| Last-mile video stack (generation, captions, assembly, music, publishing, compliance) | §C2, §D4, §D5, A.6 | ✅ **Landed** |
| Commercial plumbing (routing, embeddings, cost, billing, deployment, distribution surfaces) | §E, §F3, §D2 | ✅ **Landed** |
| Competitor and market research | Part 1, Appendix A | ✅ **Landed** |
| Narrative evaluation tooling (LLM-as-judge, pairwise, Elo/Bradley-Terry) | §A2, §A4 | ✅ **Landed** |
| Pairwise ranking and small-n statistics | §A2, §A3 | ✅ **Landed** |
| Craft-of-narrative + creative Arena | §A2 | ⏳ Outstanding |
| Corpus automation (ASR, scene detection, video-LLM pre-annotation) | §B2 | ⏳ Outstanding |
| Viral trend intelligence | §D3 | ⏳ Outstanding |
| Short-drama data platforms | §1.1 | ⏳ Outstanding |
| Coze and China accessibility | §D2 | ⏳ Outstanding |

**Nothing in Part 0, Part 1, Part 3, or Part 4 depends on the outstanding results.** The strategic
conclusions are already determined by the code reproduction (Part 0) and the market evidence
(Part 1). The pending research adds implementation detail to Part 2 — it does not move the
recommendation.

**One caveat that applies to every vendor table in this document:** all Chinese TTS benchmark numbers
are vendor-self-reported and the published tables contradict each other (FireRedTTS-2 appears as
CER 8.22 in one and 1.14 in another). **Use them to shortlist, then measure on FlowBeast's own scripts
before committing.**

---

# Appendix C — Unverified and single-source claims

Listed so that nothing here is over-trusted in a pitch or a decision.

1. **有戏AI's ¥36M first-month ARR** — 央广网 and 猎云网 both relay 风平智能's own disclosure.
   Single-source, vendor-originated.
2. **All 抖音 AI短剧 income figures** (¥500K/month, ¥80,000/video ad rate) — MCN- or
   creator-self-reported. Ceiling cases, not medians.
3. **Chinese consumer tool pricing** (即梦, 可灵 membership) — their pages are JS-rendered and were
   not captured. MiniMax API rates and 有戏AI's ¥0.1/sec come from secondary Chinese sources.
4. **DramaChain's dimension set and judge — planned release, not confirmed downloadable.**
5. **M-Drama's download link** — repo identified, availability unconfirmed.
6. **SkyScript-100M license terms** — must be checked before any commercial use.
7. **VidMob's reported ~85% valuation markdown**; **Icon.com's reported pivot**; **TikTok PineDrama
   timing** — all single-source, 2026-dated secondary.
8. **Any Gumroad revenue figure** — Gumroad publishes no sales counts. The $47 median and 168-max
   ratings are solid; anything in dollars is inferred.
9. **Faceless.video, Pictory, Syllaby, InVideo pricing** — JS-only or Cloudflare-blocked. Not
   captured.
10. **`genra.ai` "ReelShort Playbook"** — surfaced in search, never fetched. Could be a direct
    competitor. Highest-value follow-up.
11. **arXiv 2602.22299 and 2606.16053** — reached via aggregators; verify IDs before citing.

**From the last-mile research (§C2, §D4, §D5):**

12. **GB 45438-2025's exact video-label parameters** (wording, corner, minimum font height relative to
    the shorter side, opacity, duration) — not read off the standard. **Do not hard-code a watermark
    from this document.** Read the standard first.
13. **Whether a non-serialized 60–90s AI story video legally counts as 微短剧.** Order 16's Art. 2
    language points to serialized drama and Art. 33(3) suggests platform-level handling, but no binding
    interpretation was found. **This determines whether a 节目编号 is required** — resolve before
    making compliance a headline claim.
14. **抖音 / 快手 publish-API AI-disclosure fields** — parameter tables are JS-rendered; a raw scan
    found no `aigc` / `is_ai` field. Plan to set the label via UI, not API.
15. **TikTok Content Posting API unaudited-client rules** — whether an unaudited app can post publicly
    at all, and the daily cap. `developers.tiktok.com` was network-blocked. Determines whether
    unattended TikTok posting is possible.
16. **快手's entity/qualification bar** for `user_video_publish` (historical 404/504s on the docs).
17. **LongCat-Video-Avatar 1.5 minimum VRAM** — no published figure; official examples use 1–2 GPUs with
    `--use_int8` / `--use_distill`.
18. **Epidemic Sound pricing** (sales-call only) and **Mureka / Artlist / Google Lyria** terms
    (unreachable or JS-only). Music rights in §C2.3 are therefore incompletely surveyed — which is why
    the BGM slot is designed to be swappable.
19. **Suno's 2026 terms** — secondary source; suno.com unreachable.
20. **NRTA's 一类/二类/三类 investment thresholds** — not published in the 办法 itself.
21. **Veo 3.1 / BytePlus pricing pages** — JS-rendered SPAs returned only the shell; the numbers used
    came from alternate server-rendered doc pages.

**From the deployment research (§E2, §E4):**

22. **Cloud Run pricing and limits** — `google.com` and `cloud.google.com` were unreachable from the
    research network (HTTP 000). The structural finding (no persistent disk) is solid regardless; the
    numbers are not. This is also why Cloud Run is not recommended as a primary host.
23. **Hetzner's official prices** — the pricing page is JS-rendered and returned no price tokens. The
    CAX11 ≈ €4.19 figure is **third-party only**. Verify before budgeting.
24. **Northflank free-tier volume support** — the Sandbox tier is verified always-on and free; whether
    it can attach a persistent volume is not.
25. **model2vec output dimensions** — HuggingFace fetches timed out. Check dims before adopting; a
    non-768 output means a separate index.
26. **CPU-only `nomic-embed-text` throughput** — not benchmarked. Do not quote a number that has not
    been measured on your own target box.
27. **Oracle Cloud A1 reclamation window** beyond the documented "memory utilization < 20% over 7 days";
    **LanceDB Cloud and Replit pricing** (JS-rendered); **Pinecone Starter's exact index/region limits**.

---

*Related: [goal.md](goal.md) · [status.md](status.md) · [roadmap.md](roadmap.md) ·
[capability_map.md](capability_map.md) · [decisions/002](decisions/002_what_we_do_not_do.md)*
