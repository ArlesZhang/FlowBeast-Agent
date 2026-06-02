# Raw Corpus Directory

Raw viral content samples for reverse engineering into FP3.

## Structure

```
raw/
└── corpus_batch/           ← All samples go here
    ├── script_001/
    ├── script_002/
    ├── sample_template/
    └── ... (new samples)
```

## Workflow

1. **Collect**: Add new sample to `corpus_batch/NNN_title/`
2. **Reverse engineer**: Run `reverse_engineer.py --dir raw/corpus_batch/`
3. **Output**: Structured JSON goes to `reverse_engineered/cases/`

See `corpus_batch/README.md` for collection guidelines.
