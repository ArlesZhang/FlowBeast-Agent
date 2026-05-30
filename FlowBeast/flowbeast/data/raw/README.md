# Raw Samples Directory

This directory contains raw viral short-drama samples before reverse engineering.

## Structure

Each sample gets its own directory:

```
raw/
├── 001_ceos_secret_wife/
│   ├── source_url.txt          # URL to the original video
│   ├── notes.md                # Human curator notes + quality judgment
│   ├── screenshot.png          # (Optional) Key visual or thumbnail
│   └── transcript.txt          # (Optional) Dialogue transcript
│
├── 002_reborn_as_daughter/
│   ├── source_url.txt
│   ├── notes.md
│   └── ...
│
└── ...
```

## Workflow

1. **Human** watches viral drama → creates `raw/NNN_title/` directory
2. **Human** fills in `source_url.txt`, `notes.md`, (optional) `transcript.txt`
3. **Agent** runs `reverse_engineer.py --dir raw/` → produces `reverse_engineered/*.json`
4. **Agent** validates output → injects into FP3

## Naming Convention

- `NNN_title/` where NNN is zero-padded (001, 002, 003...)
- Title should be descriptive but short (2-4 words, lowercase, underscores)
- Example: `001_ceos_secret_wife`, `042_reborn_as_daughter`

## Quality Judgment

In `notes.md`, the curator MUST assign a quality_label:
- **viral**: High views/likes, strong hook, replay value
- **average**: Moderate metrics, some interesting elements but not exceptional
- **failed**: Low metrics, or interesting premise but poor execution

This judgment is critical for FP3 boundary learning.
