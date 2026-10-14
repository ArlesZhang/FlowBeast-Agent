# Gold Standard ViralScript — Controlled Vocabularies

**Version:** 1.0  
**Date:** 2026-06-01

This document defines the controlled vocabularies that MUST be used when reverse-engineering viral scripts. Using free-text for these fields causes schema drift and makes GRAFT less effective.

---

## 1. Hook Types (hook_type)

Choose ONE from this list:

| Value | Description | Example |
|-------|-------------|---------|
| `冲突爆发` | Conflict explodes immediately | "你被开除了" — first line is confrontation |
| `身份错位` | Identity mismatch / wrong person | Protagonist mistaken for someone else |
| `悬念开场` | Suspense / mystery opening | A strange scene with no context |
| `好奇驱动` | Curiosity-driven hook | "你知道他为什么这样做吗?" |
| `情感暴击` | Emotional暴击 / heartbreak | Betrayal revealed in first 3 seconds |
| `权力反转` | Power dynamic established | Subordinate holds secret power over boss |
| `超自然介入` | Supernatural element introduced | System, rebirth, time travel |

**NOT allowed:** Free-text hook types. If none of the above fit, use `其他` and describe in `annotation_notes`.

---

## 2. Conflict Types (conflict_type)

Choose ONE from this list:

| Value | Description | Example |
|-------|-------------|---------|
| `权力碾压` | Power oppression — weaker fights stronger | Employee vs CEO, student vs teacher |
| `身份揭露` | Identity reveal changes everything | Hidden billionaire, secret agent |
| `逻辑反杀` | Logic/reasoning counterattack | Protagonist outsmarts antagonist |
| `情感背叛` | Emotional betrayal | Partner cheats, friend deceives |
| `资源争夺` | Resource competition | Fight for money, position, status |
| `尊严捍卫` | Dignity defense | Humiliated character fights back |
| `规则博弈` | Rule manipulation / loophole | Exploiting system rules to win |
| `立场对立` | Ideological conflict | Right vs right, both sides have valid points |

---

## 3. Escalation Steps (escalation_curve)

Build a sequence of 3-5 steps from this vocabulary:

| Step | Meaning |
|------|---------|
| `压抑` | Suppression — protagonist is pushed down |
| `铺垫` | Setup — background, world-building |
| `升级` | Escalation — conflict intensifies |
| `爆发` | Explosion — conflict reaches climax |
| `反转` | Reversal — unexpected turn |
| `悬念` | Cliffhanger — unresolved tension |
| `高潮` | Peak — maximum emotional intensity |
| `余韵` | Aftermath — resolution / lingering emotion |

**Common patterns:**
- Standard: `压抑 → 升级 → 爆发 → 反转`
- Suspense: `铺垫 → 悬念 → 爆发 → 反转 → 余韵`
- Fast: `爆发 → 反转 → 爆发` (3 steps, no setup)

---

## 4. Highest Stakes (highest_stakes)

Choose ONE:

| Value | Description |
|-------|-------------|
| `尊严` | Dignity / face / reputation |
| `生存` | Survival / livelihood |
| `情感` | Love / family / friendship |
| `权力` | Power / status / control |
| `真相` | Truth / justice / revelation |
| `自由` | Freedom / escape from oppression |

---

## 5. Time to Hook (time_to_hook)

Choose ONE:

| Value | Description |
|-------|-------------|
| `immediate` | Hook in first 1-2 seconds |
| `within_3s` | Hook within 3 seconds |
| `delayed` | Hook after setup (5+ seconds) |

---

## 6. Resolution Types (resolution_type)

Choose ONE:

| Value | Description |
|-------|-------------|
| `爽点收尾` | Catharsis ending — protagonist wins |
| `悬念留白` | Cliffhanger ending — unresolved |
| `情感余韵` | Emotional aftermath — bittersweet |
| `循环闭合` | Full circle — returns to opening theme |
| `开放式结局` | Open ending — multiple interpretations |

---

## 7. Genres (genre)

Choose the most specific applicable genre:

| Value | Description |
|-------|-------------|
| `逆袭` | Underdog rises up |
| `身份反转` | Identity reversal drama |
| `重生` | Rebirth / second chance |
| `霸总` | CEO / billionaire romance |
| `家庭伦理` | Family drama |
| `职场` | Workplace drama |
| `玄幻` | Fantasy / supernatural |
| `系统` | System / game-like mechanics |
| `悬疑` | Mystery / thriller |
| `喜剧` | Comedy |
| `悲剧` | Tragedy |
| `甜宠` | Sweet romance |
| `复仇` | Revenge |
| `穿越` | Time travel / transmigration |
| `末日` | Apocalypse / survival |
| `校园` | School / campus |
| `其他` | Other (describe in annotation_notes) |

---

## 8. Tags (tags)

Free-form, but prefer these consistent tags within a genre:

| Category | Tags |
|----------|------|
| Plot devices | `身份反转`, `双重身份`, `隐藏大佬`, `扮猪吃虎`, `先抑后扬` |
| Emotional beats | `爽点`, `虐点`, `泪点`, `笑点`, `燃点` |
| Character dynamics | `主仆`, `师徒`, `青梅竹马`, `死对头`, `盟友` |
| Viral triggers | `反常识`, `情绪共鸣`, `社会痛点`, `阶层焦虑`, `代入感` |

**Rule:** Tags should be from this list. Add new tags only if no existing tag fits, and document the new tag here.
