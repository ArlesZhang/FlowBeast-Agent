# FlowBeast Documentation Directory

This directory contains technical documentation, architecture decisions, and project planning materials.

## Directory Structure

```
flowbeast/docs/
├── README.md              # This file
├── decisions/             # Architecture Decision Records (ADRs)
│   └── 0001-template.md   # ADR template
├── ideas/                 # Working notes and brain dumps (non-permanent)
├── meetings/              # Technical meeting notes
└── technical_reports/     # Experiment reports and analysis
```

## File Guidelines

### Architecture Decision Records (ADRs) - `decisions/`

**Purpose**: Capture important architectural decisions with context and trade-offs.

**When to create**:

- Adding/removing major components
- Changing core patterns (e.g., switching from sync to async)
- Selecting technologies with production impact
- Modifying data flows or API contracts

**Format**: See `decisions/0001-template.md`

### Working Notes - `ideas/`

**Purpose**: Temporary storage for unpolished thoughts, experiments, and exploratory ideas.

**Characteristics**:

- May contain incomplete thoughts
- May be deleted after implementation
- Not reviewed in PRs unless referenced

**When to move to decisions/**: When an idea becomes a concrete plan with documented trade-offs.

### Meeting Notes - `meetings/`

**Purpose**: Record technical discussions that impact the codebase.

**Include**:

- Decision made
- Alternative considered (and why rejected)
- Action items with owners

### Technical Reports - `technical_reports/`

**Purpose**: Document experiments, performance analyses, and research findings.

**Include**:

- Problem statement
- Methodology
- Results and conclusions
- Next steps

## Comparison: Code Comments vs Documentation


| Aspect    | Code Comments                          | Documentation Files                 |
| --------- | -------------------------------------- | ----------------------------------- |
| Scope     | Local (function/file)                  | Global (project/system)             |
| Audience  | Future readers of code                 | Team/decision-makers                |
| Lifecycle | Co-owned with code                     | Separate, longer-lived              |
| Format    | Free-form, minimal                     | Structured, reviewable              |
| Example   | `# TODO(arles,Stub #1): Support async` | `decisions/0002-async-embedding.md` |


## Tools We Use

- **Version Control**: Git (all docs are code-reviewed)
- **Search**: `rg` (ripgrep) for text search across docs
- **Linking**: Markdown links between related documents

