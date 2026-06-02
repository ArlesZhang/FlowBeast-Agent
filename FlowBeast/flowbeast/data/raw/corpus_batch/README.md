# Corpus Collection Batch

This is your working directory for collecting viral content samples.

## Current Samples

- `001_short_drama_sample/` — Video/drama content template (ready to fill)
- `002_text_post_sample/` — Text post (Xiaohongshu/Weibo) template (ready to fill)
- `sample_template/` — Complete reference template (copy for new samples)

## Adding New Samples

Create a new directory for each sample:

```
corpus_batch/
├── 003_starbucks_ai_image/
├── 004_emotional_naming_post/
├── 005_ceo_revenge_drama/
└── ...
```

## Required Files Per Sample

Each sample directory must contain:

1. **`source_url.txt`** — Link to the original content
2. **`transcript.txt`** — Text/dialogue transcript (for video/text content)
3. **`notes.md`** — Your observations:
   - What went viral and why
   - Key emotional moments
   - Audience reaction patterns
   - Your hypothesis about the mechanism

## Additional Files (Highly Recommended)

- `metrics.md` — View counts, likes, shares, comments, completion rate
- `comments.md` — Representative audience comments (10-20 with sentiment/emotion tags)
- `screenshot.png` — Key visual moments (content, comments, metrics)
- `audio.txt` — Audio/music description (for video content)

## Sample Structure

```
003_new_sample/
├── source_url.txt      ← Required
├── transcript.txt      ← Required
├── notes.md           ← Required
├── metrics.md         ← Recommended (performance data)
├── comments.md        ← Recommended (audience reactions)
└── screenshot.png     ← Recommended (visual reference)
```

## Quality Standards

Focus on **evidence** over speculation:

✅ Good: "Comments show repeated phrases like '太爽了', '终于扬眉吐气' — suggests vindication reward"

❌ Bad: "This uses the status_inversion operator" (premature labeling)

## Next Steps

After collecting 10-30 samples:
1. Run reverse engineering to extract structured patterns
2. Let operator vocabulary emerge from the data
3. Validate patterns across multiple samples
4. Build evidence-based taxonomy

See `reverse_engineered/VALIDATION_ROADMAP.md` for the full process.
