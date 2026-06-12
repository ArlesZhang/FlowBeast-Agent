# Scene Lock: [TITLE]
**Purpose:** Ensure AI-generated scenes remain visually consistent across all shots  
**Status:** LOCKED — No scene elements may change without updating this document  
**Location:** [Primary location name and type]  
**Time:** [Time of day, weather, season, era]

---

## Why Scene Lock Matters

Scene inconsistency is the **second biggest failure point** in AI visual storytelling (after character inconsistency). Without a locked scene reference:

- Furniture changes style between shots
- Room size expands or shrinks
- Lighting shifts unexpectedly
- Weather disappears or changes
- Props vanish or appear randomly
- Color temperature drifts

**Every shot must look like it was filmed in the SAME location, at the SAME time, in the SAME conditions.**

---

## Location Layout (FIXED)

### Dimensions and Shape
- **Location type:** [e.g., Small sitting room, grand ballroom, outdoor garden]
- **Size:** [Approximate dimensions]
- **Shape:** [Rectangular, circular, open, etc.]
- **Feel:** [Cozy, grand, oppressive, intimate, etc.]

### Fixed Elements (Cannot Change)
- **Element 1:** [Description, position, material]
- **Element 2:** [Description, position, material]
- **Element 3:** [Description, position, material]

### Surface Treatment
- **Walls:** [Material, color, condition, decoration]
- **Floor:** [Material, color, condition, rugs/carpets]
- **Ceiling:** [Height, material, visible features]

---

## Furniture (FIXED — Same in Every Shot)

### [Furniture Piece 1]
- **Type:** [Chair, table, desk, etc.]
- **Style:** [Period-accurate description]
- **Color/Material:** [Wood type, fabric, etc.]
- **Position:** [Where in the room]
- **State:** [How it appears throughout]

### [Furniture Piece 2]
- **Type:**
- **Style:**
- **Color/Material:**
- **Position:**
- **State:**

---

## Props (FIXED State — Track Changes)

### [Prop 1]
- **What:** [Description]
- **Where:** [Position in scene]
- **When:** [Which shots it appears in]
- **State changes:** [If any, mapped per beat]

### [Prop 2]
- **What:**
- **Where:**
- **When:**
- **State changes:**

---

## Lighting (FIXED — Same in Every Shot)

### Primary Light Source
- **Source:** [Window, fire, candles, sun, etc.]
- **Direction:** [Where light comes from]
- **Quality:** [Hard, soft, diffused, etc.]
- **Intensity:** [Bright, moderate, dim]
- **Color temperature:** [Warm, cool, neutral — with K range]

### Secondary Light
- **Source:** [Ambient bounce, fill, etc.]
- **Quality:** [Description]

### What Does NOT Exist
- **No [specific light source]:** [Reason]
- **No [specific light source]:** [Reason]

### Shadow Rules
- **Direction:** [Where shadows fall]
- **Quality:** [Hard, soft, diffused]
- **Depth:** [Light, moderate, deep]

---

## Color Temperature (FIXED)

### Dominant Palette
- [Color 1] (where it appears)
- [Color 2] (where it appears)
- [Color 3] (where it appears)

### What Does NOT Appear
- [Excluded color 1] (reason)
- [Excluded color 2] (reason)

---

## Weather / Atmosphere Progression

### Weather by Beat

| Beat | Shots | Weather State | Visual Cues |
|------|-------|--------------|-------------|
| 1 | S01-Sxx | [Description] | [What to see] |
| 2 | Sxx-Sxx | [Description] | [What to see] |
| 3 | Sxx-Sxx | [Description] | [What to see] |

### Constant Elements
- [What stays the same throughout]

### What Does NOT Happen
- [Excluded weather/atmosphere elements]

---

## Spatial Dynamics (Per Beat)

### Character Positions by Beat

| Beat | Character A | Character B | Distance | Facing |
|------|------------|------------|----------|--------|
| 1 | [Position] | [Position] | [Distance] | [Direction] |
| 2 | [Position] | [Position] | [Distance] | [Direction] |

### Movement Rules
- [How characters move through space]
- [No teleporting, logical movement]

---

## Scene-Specific Negative Prompts

### ALWAYS Include These
```
[list of elements to exclude from every prompt]
```

### NEVER Include These
- [Specific exclusions with reasons]

---

## Scene Consistency Checklist

### Before Generating Each Shot
- [ ] Location matches reference images
- [ ] Lighting is consistent
- [ ] Weather/atmosphere matches current beat
- [ ] Furniture positions are correct
- [ ] Props are in correct state
- [ ] Color temperature is consistent
- [ ] Character positions match beat progression

### After Generating Each Shot
- [ ] Location looks the same as previous shot
- [ ] No unexpected lighting changes
- [ ] Weather/atmosphere is consistent
- [ ] No furniture style changes
- [ ] Props are consistent
- [ ] No anachronistic elements

### Side-by-Side Review (After All Shots)
- [ ] Location is identical across all shots
- [ ] Lighting is consistent throughout
- [ ] Weather progression follows beat pattern
- [ ] Furniture hasn't morphed
- [ ] Props track correctly

---

## Required Scene Assets

**Before generating shots, these reference images must exist in `09_assets/scenes/`:**

### Location References (Minimum 4)
1. **Wide establishing shot** — [Full location view]
2. **[Area 1]** — [Description and purpose]
3. **[Area 2]** — [Description and purpose]
4. **[Area 3]** — [Description and purpose]

### Lighting Reference (Minimum 1)
5. **[Lighting condition]** — [Description]

### Weather/Atmosphere References (Minimum 1 per state)
6. **[Weather state 1]** — [Description]
7. **[Weather state 2]** — [Description]

**Total minimum scene assets: [N] images**

---

## Troubleshooting

### Issue: Location Looks Different Between Shots
**Solution:** [Specific fix]

### Issue: Lighting Shifts
**Solution:** [Specific fix]

### Issue: Weather/Atmosphere Inconsistency
**Solution:** [Specific fix]

### Issue: Furniture Changes
**Solution:** [Specific fix]

### Issue: Props Disappear or Move
**Solution:** [Specific fix]
