# Prompt Package: [TITLE]

---

## Overview

- **Case Study:** [Name]
- **Scene:** [Scene name]
- **Total Shots:** [Number]
- **Target Platform:** [Seedance/Kling/HeyGen]
- **Export Date:** [Date]

---

## Global Constraints

### Style Lock
[Reference to style_lock.md]

### Character Bible
[Reference to character_bible.md]

### Negative Prompts
[Reference to negative_rules.md]

---

## Shot Prompts

### Shot 1
```json
{
  "shot_id": 1,
  "description": "Shot description",
  "character": "Character name",
  "action": "What happens",
  "emotion": "Emotional beat",
  "camera": "Camera direction",
  "style": "Style constraints",
  "negative": "What to avoid",
  "duration": "seconds"
}
```

### Shot 2
```json
{
  "shot_id": 2,
  "description": "",
  "character": "",
  "action": "",
  "emotion": "",
  "camera": "",
  "style": "",
  "negative": "",
  "duration": ""
}
```

---

## Export Format

### prompt_package.json
```json
{
  "title": "Case study title",
  "platform": "target platform",
  "aspect_ratio": "16:9",
  "shots": [
    {
      "id": 1,
      "prompt": "Full prompt text",
      "negative_prompt": "Negative constraints",
      "duration": 3,
      "transition": "cut"
    }
  ]
}
```

---

## Validation Checklist

- [ ] All shots have complete prompts
- [ ] Character consistency maintained
- [ ] Style lock applied to all shots
- [ ] Negative prompts included
- [ ] Duration totals match scene length
- [ ] Export format matches platform requirements
