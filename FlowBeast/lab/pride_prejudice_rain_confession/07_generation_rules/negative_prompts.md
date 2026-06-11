# Negative Prompts: Darcy's Rain Confession
**Purpose:** Prevent common AI generation errors and maintain visual consistency

---

## Global Negative Prompts (Include in EVERY Prompt)

### Modern Elements (FORBIDDEN)
```
modern clothing, modern hairstyles, modern makeup, modern accessories,
smartphone, laptop, tablet, contemporary furniture, electric lights,
modern buildings, cars, modern technology, modern appliances,
contemporary art, modern decorations, modern jewelry, modern watches
```

### Anachronisms (FORBIDDEN)
```
wrong period costume, Victorian clothing, medieval clothing, Renaissance clothing,
wrong hairstyle, wrong hat, wrong shoes, wrong accessories,
electric lights, gas lamps, modern plumbing, modern heating,
modern windows, modern doors, modern furniture, modern materials
```

### Visual Noise (FORBIDDEN)
```
text, watermark, signature, logo, UI elements, subtitles,
credits, timestamps, channel names, website URLs,
border, frame, vignette, lens flare, chromatic aberration
```

### Style Violations (FORBIDDEN)
```
cartoon, anime (too stylized), photorealistic (too flat),
3D render, CGI, low-poly, pixel art, watercolor, oil painting,
sketch, line art, black and white, sepia, vintage filter
```

### Lighting Violations (FORBIDDEN)
```
sunlight, direct sun, warm lighting, golden hour, sunset, sunrise,
candles, fire in fireplace, torches, lanterns, electric lights,
neon lights, colored lighting, dramatic lighting, high contrast
```

### Weather Violations (FORBIDDEN)
```
clear sky, sunny, no rain, dry, snow, fog, mist, hail,
rainbow, storm (too severe), tornado, hurricane
```

### Character Violations (FORBIDDEN)
```
face changes, different face, morphing face, inconsistent face,
wrong eye color, wrong hair color, wrong skin tone, wrong age,
costume changes, different outfit, wrong period clothing,
extra fingers, deformed hands, deformed face, blurry face
```

### Quality Issues (FORBIDDEN)
```
low quality, blurry, out of focus, pixelated, low resolution,
artifacts, noise, grain, compression artifacts, jpeg artifacts,
oversaturated, undersaturated, too bright, too dark
```

---

## Elizabeth-Specific Negative Prompts

### Face and Hair (FORBIDDEN)
```
blonde hair, light brown hair, red hair, black hair,
blue eyes, green eyes, gray eyes, light eyes,
heavy makeup, lipstick, eyeshadow, modern makeup,
short hair, straight hair, curly hair (must be wavy),
modern hairstyle, ponytail, bun (must be partially down)
```

### Costume (FORBIDDEN)
```
Victorian dress, medieval dress, modern dress, casual clothing,
silk dress (must be cotton/wool), elaborate gown, ball gown,
bright colors (must be muted blue-gray), red dress, pink dress,
low neckline (must be modest), sleeveless (must have sleeves),
modern jewelry, elaborate jewelry, tiara, crown
```

### Body and Posture (FORBIDDEN)
```
tall (must be 5'4"), overweight, underweight, muscular,
slouching (until Beat 5), poor posture, modern body language,
sexy pose, seductive expression, modern gestures
```

---

## Darcy-Specific Negative Prompts

### Face and Hair (FORBIDDEN)
```
blonde hair, light brown hair, red hair, gray hair,
light eyes, blue eyes, green eyes, gray eyes,
beard, mustache, facial hair, long hair,
modern hairstyle, messy hair (must be controlled, slightly tousled)
```

### Costume (FORBIDDEN)
```
Victorian clothing, medieval clothing, modern clothing, casual clothing,
bright colors (must be dark), casual coat, modern suit,
no coat (must wear tailcoat), dry coat (must be wet),
modern boots, sneakers, casual shoes,
no cravat (must wear cravat), modern tie
```

### Body and Posture (FORBIDDEN)
```
short (must be 6'0"), overweight, underweight, weak build,
slouching, poor posture, casual body language,
modern gestures, relaxed pose (must be rigid, controlled)
```

### Wetness (CRITICAL — FORBIDDEN)
```
dry coat, dry hair, dry boots, dry clothing,
umbrella, raincoat, hood, hat (must be bareheaded, wet)
```

---

## Scene-Specific Negative Prompts

### Location (FORBIDDEN)
```
grand ballroom, palace, castle, mansion, modern apartment,
outdoor scene, garden, street, different room,
large room (must be small, modest), bright room (must be dim)
```

### Furniture and Props (FORBIDDEN)
```
modern furniture, electric appliances, television, computer,
grand piano, elaborate decorations, modern art,
fireplace with fire (must be unlit), candles (must not be lit),
books everywhere (must be modest, few books)
```

### Weather and Lighting (FORBIDDEN)
```
clear sky, sunny, no rain, dry windows,
sunlight, direct sun, warm lighting, golden hour,
candles, fire, electric lights,
snow, fog, mist, hail, rainbow
```

### Atmosphere (FORBIDDEN)
```
cheerful, happy, bright, colorful, festive,
dark and gloomy (must be melancholic, not depressing),
horror, scary, threatening, violent
```

---

## Emotional State Negative Prompts

### Beat 1 (Arrival) — FORBIDDEN
```
happy, cheerful, relaxed, comfortable,
angry, furious, hostile, aggressive
```

### Beat 2 (Confession) — FORBIDDEN
```
happy, cheerful, relaxed, confident,
angry, furious, hostile, aggressive
```

### Beat 3 (Obstacles) — FORBIDDEN
```
happy, cheerful, relaxed, humble,
crying, sobbing, weak, defeated
```

### Beat 4 (Accusations) — FORBIDDEN
```
happy, cheerful, relaxed, calm,
weak, defeated, crying, sobbing
```

### Beat 5 (Departure) — FORBIDDEN
```
happy, cheerful, relaxed, comfortable,
angry, furious, hostile, aggressive
```

---

## Composition Negative Prompts

### Framing (FORBIDDEN)
```
extreme wide shot (too distant), extreme close-up (too tight),
Dutch angle, tilted frame, upside down,
split screen, multiple panels, collage
```

### Camera (FORBIDDEN)
```
handheld shake, fast zoom, whip pan, 360° spin,
crane shot, aerial shot, drone shot,
fisheye lens, wide-angle distortion, telephoto compression
```

### Depth of Field (FORBIDDEN)
```
everything sharp (must have some blur), everything blurry (must be sharp on subject),
tilt-shift effect, miniature effect, lens blur
```

---

## Technical Negative Prompts

### Quality (FORBIDDEN)
```
low resolution, low quality, blurry, out of focus,
pixelated, jpeg artifacts, compression artifacts,
noise, grain, film grain, vintage filter
```

### Rendering (FORBIDDEN)
```
3D render, CGI, low-poly, wireframe,
sketch, line art, pencil drawing, charcoal,
watercolor, oil painting, acrylic painting
```

### Post-Processing (FORBIDDEN)
```
HDR, tone mapping, bloom, lens flare,
chromatic aberration, vignette, film grain,
color grading, LUT, filter, preset
```

---

## Negative Prompt Templates

### Template 1: Elizabeth Shot
```
modern clothing, modern hairstyles, modern makeup, modern accessories,
blonde hair, light brown hair, red hair, black hair,
blue eyes, green eyes, gray eyes, light eyes,
Victorian dress, medieval dress, modern dress, casual clothing,
silk dress, elaborate gown, ball gown, bright colors,
heavy makeup, lipstick, eyeshadow, modern jewelry,
smartphone, laptop, contemporary furniture, electric lights,
wrong period costume, wrong hairstyle, wrong accessories,
face changes, different face, morphing face, inconsistent face,
extra fingers, deformed hands, deformed face, blurry face,
text, watermark, signature, logo, UI elements,
sunlight, direct sun, warm lighting, candles, fire in fireplace,
clear sky, sunny, no rain, dry, snow, fog,
low quality, blurry, out of focus, pixelated, artifacts
```

### Template 2: Darcy Shot
```
modern clothing, modern hairstyles, modern accessories,
blonde hair, light brown hair, red hair, gray hair,
blue eyes, green eyes, gray eyes, light eyes,
beard, mustache, facial hair, long hair,
Victorian clothing, medieval clothing, modern clothing, casual clothing,
bright colors, casual coat, modern suit,
dry coat, dry hair, dry boots, dry clothing,
umbrella, raincoat, hood, hat,
smartphone, laptop, contemporary furniture, electric lights,
wrong period costume, wrong hairstyle, wrong accessories,
face changes, different face, morphing face, inconsistent face,
extra fingers, deformed hands, deformed face, blurry face,
text, watermark, signature, logo, UI elements,
sunlight, direct sun, warm lighting, candles, fire in fireplace,
clear sky, sunny, no rain, dry, snow, fog,
low quality, blurry, out of focus, pixelated, artifacts
```

### Template 3: Both Characters Shot
```
modern clothing, modern hairstyles, modern makeup, modern accessories,
blonde hair, light brown hair, red hair, black hair, gray hair,
blue eyes, green eyes, gray eyes, light eyes,
Victorian clothing, medieval clothing, modern clothing, casual clothing,
silk dress, elaborate gown, ball gown, bright colors,
dry coat, dry hair, dry boots, dry clothing,
heavy makeup, lipstick, eyeshadow, modern jewelry,
beard, mustache, facial hair, long hair,
smartphone, laptop, contemporary furniture, electric lights,
wrong period costume, wrong hairstyle, wrong accessories,
face changes, different face, morphing face, inconsistent face,
extra fingers, deformed hands, deformed face, blurry face,
text, watermark, signature, logo, UI elements,
sunlight, direct sun, warm lighting, candles, fire in fireplace,
clear sky, sunny, no rain, dry, snow, fog,
low quality, blurry, out of focus, pixelated, artifacts,
different faces, inconsistent characters, costume changes
```

### Template 4: Wide Shot (Room)
```
modern furniture, electric appliances, television, computer,
grand piano, elaborate decorations, modern art,
fireplace with fire, candles, electric lights,
sunlight, direct sun, warm lighting, golden hour,
clear sky, sunny, no rain, dry windows,
grand ballroom, palace, castle, mansion, modern apartment,
outdoor scene, garden, street, different room,
large room, bright room, cheerful room,
text, watermark, signature, logo, UI elements,
low quality, blurry, out of focus, pixelated, artifacts
```

---

## How to Use Negative Prompts

### Basic Usage
1. **Copy the appropriate template** (Elizabeth, Darcy, Both, or Room)
2. **Paste into negative prompt field** in AI generation tool
3. **Add shot-specific negatives** (if needed)
4. **Generate and review** for consistency

### Shot-Specific Additions

**For emotional beats:**
- Add emotional state negatives (e.g., "happy, cheerful" for Beat 4)

**For specific actions:**
- Add action negatives (e.g., "sitting" for standing shots)

**For specific framing:**
- Add framing negatives (e.g., "extreme close-up" for medium shots)

### Quality Control

**After generation, check:**
- [ ] No modern elements visible
- [ ] No anachronisms visible
- [ ] No visual noise (text, watermarks)
- [ ] Style is consistent (semi-realistic anime)
- [ ] Lighting is correct (overcast, gray, diffused)
- [ ] Weather is correct (rain, varying intensity)
- [ ] Characters are consistent (face, costume, hair)
- [ ] Emotions match beat (not happy in Beat 4)

**If issues found:**
- Regenerate with stronger negative prompts
- Increase negative prompt weight
- Add more specific negatives
- Use reference images

---

## Troubleshooting Common Issues

### Issue: Modern Elements Appear
**Solution:** Strengthen modern element negatives, add "no modern [specific element]"

### Issue: Wrong Period Costume
**Solution:** Add "wrong period costume" to negatives, include "Regency era" in positive prompt

### Issue: Face Changes
**Solution:** Add "face changes, different face" to negatives, use face reference image

### Issue: Dry Coat (Darcy)
**Solution:** Add "dry coat, dry hair, dry boots" to negatives, emphasize "wet coat" in positive prompt

### Issue: Wrong Lighting
**Solution:** Add "sunlight, warm lighting, candles" to negatives, emphasize "overcast, gray" in positive prompt

### Issue: No Rain
**Solution:** Add "clear sky, sunny, no rain, dry" to negatives, emphasize "rain, storm" in positive prompt

---

## Summary

**Always include in negative prompts:**
1. Modern elements
2. Anachronisms
3. Visual noise
4. Style violations
5. Lighting violations
6. Weather violations
7. Character violations
8. Quality issues

**Customize for:**
- Elizabeth (face, hair, costume)
- Darcy (face, hair, costume, wetness)
- Both characters (consistency)
- Room (furniture, props, lighting)
- Emotional beat (appropriate emotions)

**Quality control:**
- Review every shot
- Regenerate if issues found
- Strengthen negatives if needed

---

## Next Steps

With negative prompts complete, the next phase is:
- **Prompt Package** (compile everything into final AI-ready format)
