# Corpus Factory Report

**Date:** 2026-06-01  
**Scope:** reverse_engineer.py, ViralScript schema, FP3 storage, QualityGate  
**Objective:** Validate that 1 script can be reverse-engineered correctly before scaling to 30.

---

## 1. Current Schema Weaknesses

### 1.1 Critical Gaps (Blocks Viral Structure Transfer)

| Field | Status | Impact |
|-------|--------|--------|
| `prompt_atoms` | Never populated by any extraction path | The Viral Prompt Compiler has no atom references — this is a dead-end field |
| `vertical_name` | Never populated | Lost tracking of which content vertical the script belongs to |
| `latent_embedding` | Never populated | Semantic layer for preventing over-templatization doesn't exist |
| `audience_question` | Empty in `from-script` mode | GRAFT's audience psychology transfer requires this field |
| `reversal_count` | 0 in `from-script` mode | GRAFT's reversal mechanics transfer broken |
| `highest_stakes` | Hardcoded "尊严" in `from-script` mode | GRAFT's stakes alignment uses wrong value |
| `peak_position` | Hardcoded "late" in `from-script` mode | Emotional arc timing lost |
| `resolution_type` | Hardcoded "爽点收尾" in `from-script` mode | Ending diversity lost |

### 1.2 Fields GRAFT Uses But Schema May Not Capture Well

GRAFT extracts these from the ViralScript:

| GRAFT Consumes | Source Field | Quality of Data |
|----------------|-------------|-----------------|
| hook_type | `hook_structure.hook_type` | Interactive: good. From-script: hardcoded "悬念开场" |
| opening_line | `hook_structure.opening_line` | Always set (interactive: manual, from-script: `core_hook`) |
| time_to_hook | `hook_structure.time_to_hook` | Interactive: choice-based. From-script: hardcoded "immediate" |
| audience_question | `hook_structure.audience_question` | Interactive: manual. From-script: empty string |
| emotional_payload | `hook_structure.emotional_payload` | Interactive: manual. From-script: `emotion_curve[0]` |
| conflict_type | `conflict_pattern.conflict_type` | Interactive: manual. From-script: first scene's conflict |
| escalation_curve | `conflict_pattern.escalation_curve` | Interactive: manual. From-script: not extracted |
| reversal_count | `conflict_pattern.reversal_count` | Interactive: integer input. From-script: 0 |
| highest_stakes | `conflict_pattern.highest_stakes` | Interactive: choice. From-script: hardcoded "尊严" |

### 1.3 Fields GRAFT Ignores (But PARASITE Would Need)

| Field | Future Operator | Why It Matters |
|-------|----------------|----------------|
| `emotional_curve` (full) | PARASITE | Need full curve to match trend events to compatible spines |
| `pacing_profile` | PARASITE | Need beat distribution to know where to inject trend events |
| `characters` | PARASITE | Need archetypes to match trend to character-driven narratives |
| `special_techniques` | DISTORT | Need to know which techniques to exaggerate/compress |
| `semantic_summary` | ALL | One-line "why this went viral" — critical for GRAFT instruction quality |

### 1.4 Schema Design Assessment

**Strengths:**
- 4 sub-models (HookStructure, ConflictPattern, EmotionalCurve, PacingProfile) are well-scoped
- `quality_label` with viral/average/failed supports positive and negative sample learning
- `to_viral_unit()` provides clean backward compatibility for FAISS search
- `special_techniques` as a list captures production tricks not covered by other fields

**Weaknesses:**
- No field for "why did this go viral" beyond `semantic_summary` (optional, free-text)
- No field for platform-specific adaptation patterns (Douyin vs Kuaishou have different viral mechanics)
- `prompt_atoms` as a list of strings is disconnected from the actual PromptAtom instances
- No validation that `characters` must have at least 1 entry (empty list passes)
- `tags` has no controlled vocabulary — "身份反转", "身份揭露", "identity_reveal" all mean the same thing

---

## 2. Recommended Schema Changes

### 2.1 Additions (Must-Have for Gold Standard)

| New Field | Type | Purpose |
|-----------|------|---------|
| `viral_reason: str` | Required | One-line "why this went viral" — more structured than `semantic_summary` |
| `platform_adaptation: str` | Optional | How the script was adapted for its platform (Douyin vertical, Kuaishou rural, etc.) |
| `comparable_scripts: List[str]` | Optional | IDs of similar viral scripts — helps GRAFT find related structures |
| `annotation_notes: str` | Optional | Human annotator's notes on what was hard to classify |
| `confidence_score: float` | Optional | Human annotator's confidence in their classification (0-1) |

### 2.2 Modifications

| Field | Change | Reason |
|-------|--------|--------|
| `hook_type` | Add controlled vocabulary (dropdown in interactive mode) | "悬念开场", "冲突爆发", "身份错位", "悬念留白", "好奇驱动" — prevent drift |
| `conflict_type` | Add controlled vocabulary | "权力碾压", "身份揭露", "逻辑反杀", "情感背叛", "资源争夺" |
| `escalation_curve` | Add allowed step vocabulary | "压抑", "升级", "爆发", "反转", "悬念", "铺垫", "高潮", "余韵" |
| `quality_label` | Keep as-is | viral/average/failed is correct |
| `reversal_count` | Make 0-5 range explicit in interactive mode | Current allows any int, but realistic range is 0-5 |

### 2.3 Deprecations

| Field | Action | Reason |
|-------|--------|--------|
| `prompt_atoms` | Keep but rename to `atom_references` and make it a dict `{atom_id: relevance_score}` | Current list of strings loses relevance weighting |
| `vertical_name` | Keep but make it a required field in interactive mode | Critical for corpus organization |
| `latent_embedding` | Remove from schema (computed at build time) | Never populated manually, always generated by embedding pipeline |

### 2.4 What NOT to Change

- **Don't add new sub-models** — the 4 existing sub-models cover the space well enough
- **Don't add video-specific fields** — we output prompt packages, not video
- **Don't add engagement metrics beyond views/likes** — `viral_metrics` is sufficient for now
- **Don't add more than 5 new fields** — schema bloat is the enemy at this stage

---

## 3. Gold Standard ViralScript Structure

A "gold standard" ViralScript is one where **every field that GRAFT consumes is accurately populated**, and the human annotator is confident in their classification.

### 3.1 Minimum Viable Fields (Must Be Accurate for GRAFT)

These 10 fields are the minimum for GRAFT to work:

1. `hook_structure.hook_type` — from controlled vocabulary
2. `hook_structure.opening_line` — the actual first line
3. `hook_structure.time_to_hook` — from controlled vocabulary
4. `hook_structure.audience_question` — what the viewer asks after the hook
5. `hook_structure.emotional_payload` — core emotion of the hook
6. `conflict_pattern.conflict_type` — from controlled vocabulary
7. `conflict_pattern.escalation_curve` — sequence of escalation steps
8. `conflict_pattern.reversal_count` — integer 0-5
9. `conflict_pattern.highest_stakes` — from controlled vocabulary
10. `emotional_curve.curve_sequence` — full emotion sequence

### 3.2 Supporting Fields (Must Be Present, Accuracy Less Critical)

11. `source_title` — the script's title
12. `source_platform` — where it was found
13. `source_url` — link to original
14. `quality_label` — viral / average / failed
15. `genre` — from controlled vocabulary
16. `tags` — free-form but consistent within a genre
17. `semantic_summary` — one-line "why this went viral"
18. `pacing_profile.duration_sec` — approximate duration
19. `pacing_profile.scene_count` — number of scenes
20. `special_techniques` — notable production techniques

### 3.3 Nice-to-Have Fields

21. `characters` — at least protagonist + antagonist
22. `music_style`
23. `voice_style`
24. `visual_style_notes`
25. `pacing_profile.beat_distribution`
26. `emotional_curve.peak_emotion`
27. `emotional_curve.peak_position`
28. `emotional_curve.resolution_type`

---

## 4. Human Annotation Workflow

### 4.1 The Process (Per Script)

**Time budget:** 20-30 minutes per script

```
1. Watch the viral short drama (3-5 minutes)
2. Take notes on key moments (hook, conflict, escalation, resolution) (5 minutes)
3. Fill interactive reverse_engineer.py prompts (10 minutes)
4. Review the saved JSON and verify all Gold Standard fields are populated (5 minutes)
5. Run reverse_engineer.py --input saved.json --no-inject to verify no Pydantic errors
6. Check QualityGate result — if REJECT, review and fix classification errors
7. Accept the entry into FP3
```

### 4.2 Interactive Mode Usage

```bash
uv run python -m flowbeast.reverse.reverse_engineer
```

This launches the 7-section interactive builder. Fill in each section:
1. Source info (title, platform, URL)
2. Viral metrics (views, likes)
3. Hook structure (opening line, type, time_to_hook, audience_question, emotional_payload)
4. Conflict pattern (type, escalation curve, reversal count, highest stakes)
5. Emotional curve (sequence, peak emotion, peak position, resolution type)
6. Pacing profile (duration, scene count, beat distribution)
7. Special techniques and production notes

### 4.3 File Import Mode (After Building a Template)

```bash
# Edit TEMPLATE_viral_analysis.json with real data
uv run python -m flowbeast.reverse.reverse_engineer --input flowbeast/data/reverse_engineered/your_script.json
```

---

## 5. Corpus Quality Checklist

A corpus entry passes quality check if ALL of the following are true:

### 5.1 Structural Validity

- [ ] `ViralScript(**data)` deserializes without error (Pydantic validation passes)
- [ ] All 10 Minimum Viable Fields (Section 3.1) are non-empty
- [ ] `hook_type` is from controlled vocabulary
- [ ] `conflict_type` is from controlled vocabulary
- [ ] `escalation_curve` has at least 2 steps
- [ ] `curve_sequence` has at least 3 emotions
- [ ] `reversal_count` is 0-5
- [ ] `quality_label` is one of: viral, average, failed

### 5.2 Content Validity

- [ ] `opening_line` is the actual first line of the script (not a summary)
- [ ] `audience_question` is a question a viewer would naturally ask (not a label)
- [ ] `emotional_payload` describes a specific emotion (not "复杂" or "各种情绪")
- [ ] `escalation_curve` shows progression (not just ["好", "更好"])
- [ ] `semantic_summary` explains WHY it went viral (not just what happened)
- [ ] `genre` is specific (not "短剧" or "网络剧")

### 5.3 Provenance Validity

- [ ] `source_url` points to a real video (not a placeholder)
- [ ] `source_platform` is accurate
- [ ] `source_title` matches the original content's title
- [ ] `viral_metrics` has at least views OR likes

### 5.4 GRAFT Readiness

- [ ] If you ran GRAFT on this entry for a new topic, would the LLM have enough structural information to produce a differentiated script? (Yes/No)
- [ ] Does the `hook_type` + `conflict_type` combination represent a proven viral pattern? (Yes/No)
- [ ] Would a human annotator be able to verify the classification by watching the source video? (Yes/No)

### 5.5 Scoring

| Score | Criteria |
|-------|----------|
| **GOLD** | All 5 sections pass. Human confidence >= 0.8. GRAFT would produce clearly differentiated output. |
| **SILVER** | Sections 5.1, 5.2, 5.3 pass. One or two items in 5.4 are uncertain. |
| **BRONZE** | Sections 5.1 and 5.3 pass. Some fields in 5.2 are weak. GRAFT may produce generic output. |
| **REJECT** | Any item in 5.1 fails. Must be fixed before acceptance. |

---

## 6. Definition of Done: Valid FP3 Entry

A ViralScript entry is "done" when:

1. **Structurally valid** — deserializes, all required fields populated, controlled vocabularies used correctly
2. **Content-accurate** — fields describe the actual content, not placeholder text
3. **Provenance-verified** — source URL works, platform and title are accurate
4. **QualityGate-approved** — passes ACCEPT or REVIEW (not REJECT)
5. **GRAFT-ready** — the 10 Minimum Viable Fields are accurate enough for structural transfer
6. **Human-verified** — a human has watched the source video and confirmed the classification

---

## 7. Current Weaknesses in reverse_engineer.py

### 7.1 From-Script Mode Needs Heuristic Improvement

The `analyze_generated_script()` function hardcodes 9 fields. This is acceptable for its purpose (analyzing our own output), but means from-script mode cannot produce gold-standard entries. **Recommendation:** Keep from-script mode as-is (it's for analyzing our output, not for building the corpus). Focus on improving interactive mode.

### 7.2 Interactive Mode Needs Controlled Vocabularies

Current interactive mode uses `_ask_choice` for some fields but doesn't enforce controlled vocabularies for `hook_type`, `conflict_type`, `highest_stakes`. **Recommendation:** Add predefined options as the first choices in each section.

### 7.3 No Validation of Field Combinations

A user could enter `hook_type="冲突爆发"` with `emotional_payload="甜蜜"` — this combination may not make sense. **Recommendation:** Add cross-field validation warnings (not hard blocks) in interactive mode.

### 7.4 Bare Exception Handlers

Lines 265 and 379 use bare `except Exception`. This masks errors during batch import and quality gate evaluation. **Recommendation:** Replace with specific exception types and proper error logging.

---

## 8. Immediate Next Steps

1. **Update interactive mode** to add controlled vocabularies for hook_type, conflict_type, highest_stakes, escalation_curve steps, and resolution_type
2. **Make `vertical_name` required** in interactive mode
3. **Add `viral_reason` field** to schema and interactive mode
4. **Add confidence_score field** to schema and interactive mode
5. **Produce 3 gold examples** using the updated interactive mode
6. **Verify GRAFT produces differentiated output** from each gold example
7. **Only then** scale to 30 scripts
