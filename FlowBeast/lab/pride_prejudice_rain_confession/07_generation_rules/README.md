# 07_generation_rules/

Define the technical constraints for AI video generation.

## Output Files

| File | Purpose |
|------|---------|
| `style_lock.md` | Visual style constraints (anime, realistic, etc.) |
| `scene_lock.md` | **Scene consistency constraints** (room, furniture, lighting, weather) |
| `negative_prompts.md` | What NOT to include |
| `platform_specs.md` | Target platform requirements (Seedance, Kling, etc.) |

## Focus

- Style lock prevents visual drift across shots
- **Scene lock prevents room/furniture/lighting/weather drift** (the #2 failure point in AI Manju)
- Negative prompts prevent common AI artifacts
- Platform specs ensure compatibility with target tools

## Scene Lock (scene_lock.md)

The scene lock is the scene-level equivalent of the character bible. It ensures:
- Room layout stays identical across all 48 shots
- Furniture doesn't change style or position
- Lighting stays overcast/gray (no sunlight, no candles)
- Weather progression follows the beat pattern
- Props track correctly (book, gloves, wet coat)
- Color temperature stays cool and muted

**Required scene assets:** See `09_assets/scenes/` for the reference images that must exist before shot generation.
