# FlowBeast Content Factory — Cursor Rules

Welcome to FlowBeast's AI-assisted content production rules.

```
.cursor/
└── rules/
    ├── 01-project.md          # Core philosophy (Updated for Phase 2)
    ├── 03-coding-style.md     # Code quality (Keep)
    └── 08-git-workflow.md     # Git conventions (Keep)
```

**Archived rules** (infrastructure-specific, in main/develop branches):
- `02-architecture.md` — FP3/Corpus architecture
- `04-testing.md` — Infrastructure testing
- `05-python.md` — General Python conventions
- `06-ai-agent.md` — Agent framework design
- `07-docker-devcontainer.md` — Docker setup

## Current Focus

**Phase 2: Video Production** (Case Study #001 Complete)

- **Immediate Goal:** Generate 48 shots from `prompt_package.json` using Jimeng AI (即梦)
- **Quality Focus:** Character consistency, style lock adherence, emotional accuracy
- **Next Milestone:** Assemble 2-minute video and publish for feedback

**Phase 3: Template Refinement** (After video generation)

- Review Case Study #001 learnings
- Update templates in `lab/_templates/`
- Prepare for Case Study #002

## Project Priorities

1. **Production over perfection** — Ship the video, gather real feedback
2. **Character consistency is king** — Regenerate shots if faces/costumes drift
3. **Fast iteration** — Test with 30-second clip before full assembly
4. **Document learnings** — Retrospective informs Case Study #002
5. **Reusable workflow** — 9-skill process proven, apply to next case

## Philosophy

This is NOT about "restricting AI". It's about **stabilizing AI's long-term output quality**.

For this video production phase:
- Focus on **visual consistency**, not infrastructure
- Maintain character and style consistency across all 48 shots
- Prioritize emotional impact over technical perfection
- Iterate based on real viewer feedback
- Build reusable methodology for future case studies

## What This Branch Is

**A content production workspace**, not a Python project.

- ✅ Case Study #001 complete (all 9 skills executed)
- ✅ Prompt package ready for AI video tools
- ⏳ Video generation in progress
- ⏳ Publication and feedback gathering
- ⏳ Retrospective and template refinement

**The goal:** Turn the engineering package into a real video that people can watch, evaluate, and share.
