# Rotborn Recursion Engine - Codebase Audit

**Audit Date:** 2026-03-27  
**Source:** swarm-art/swarm-gen-game-art-main-main  
**Target:** tools/rotborn-recursion/

---

## Executive Summary

The existing codebase is a **solid foundation** for the Rotborn Recursion Engine:

**Strengths:**
- Mature, tested sprite generation (~2,000 lines of working code)
- Scalable architecture (32x32 → any size)
- Deterministic seeding for reproducibility
- Batch generation with uniqueness verification
- Full animation pipeline
- 4-directional rendering

**What stands between current state and Rotborn:**
1. Strip ~2,500 lines of GeneSwarm AI/ML complexity
2. Replace palettes (inclusive → trauma/horror)
3. Modify proportions (healthy → broken/distorted)
4. Add trauma system (scars, bandages, mutations)
5. Haunt animations (natural → unnatural movement)

**Estimated total effort: 12-18 hours** for a complete transformation.

---

## File Structure

### Keep (Core Engine)

| File | Purpose | Lines |
|------|---------|-------|
| `generator/pure_generator.py` | Base sprite rendering | 1,166 |
| `generator/mass_generator.py` | Batch generation | 577 |
| `generator/animation_generator.py` | Animation frames | 646 |
| `generator/animation_types.py` | Animation definitions | 50 |
| `generator/direction_renderer.py` | 4-directional rendering | 450 |
| `ai_human_generator.py` | CLI entry point | 673 |
| `run_app.py` | GUI launcher | 12 |
| `app/` (6 files) | PyQt6 GUI | ~1,500 |

### Strip (GeneSwarm AI)

| File | Purpose | Lines |
|------|---------|-------|
| `generator/swarm/` (4 files) | AI agent system | 1,920 |
| `generator/swarm_generator.py` | Swarm integration | 430 |
| `SWARM_README.md` | Swarm docs | - |
| Swarm CLI commands | `generate-swarm`, etc. | ~150 |

**Total to strip: ~2,500 lines**

---

## Core Systems

### Sprite Generation Pipeline

```
pure_generator.py (base)
    │
    ├── _create_inclusive_palette() → ColorPalette dataclass
    │   ├── skin_tones: 21 RGB tuples
    │   ├── hair_colors: 8 RGB tuples
    │   ├── clothing_colors: 10 RGB tuples
    │   └── eye_colors: 7 RGB tuples
    │
    ├── _generate_character_params() → Dict
    │   ├── gender, social_class, age_category
    │   ├── skin_color, hair_color, eye_color
    │   ├── clothing, hair_style, face_style
    │   └── body_metrics (BMI, height, weight)
    │
    ├── _render_character_with_params() → PIL.Image
    │   ├── _draw_legs()
    │   ├── _draw_torso()
    │   ├── _draw_arms()
    │   ├── _draw_head()
    │   ├── _draw_hair()
    │   ├── _draw_face()
    │   └── _draw_accessories()
    │
    └── direction_renderer.py (non-front views)
        ├── render_back() → UP direction
        ├── render_left() → LEFT direction
        └── render_right() → RIGHT (mirrored)
```

### Scaling System

Uses **reference 32x32 coordinate system** that scales mathematically:

```python
self.base_size = 32
self.scale = min(self.width / self.base_size, self.height / self.base_size)

def _s(self, value: float) -> int:
    return int(value * self.scale)
```

**Supported:** 32x32, 64x64, 128x128, or any custom square size.

---

## What to Modify

### 1. Palettes: Inclusive → Trauma/Haunted

**Current:** Healthy, diverse skin tones (21 shades), natural hair colors

**Rotborn needs:**
- Deathly pale, ashen, gray pallor
- Sickly green tints (decay)
- Bruised, mottled, bloodstained
- Matted hair (filthy, greasy, ash-gray)
- Clothing: grimy, moldy, rotten dark

### 2. Proportions: Healthy BMI → Broken/Distorted

**Current:** Medically accurate BMI (13-40), 9 body types

**Rotborn needs:**
- Hunched (spine curved)
- Twisted (asymmetric)
- Elongated (limbs too long)
- Shrunken (overall 0.7x scale)
- Swollen (torso distended)
- Emaciated extreme (width 0.4x)
- Mutated (extra protrusions)

### 3. Animations: Natural → Haunted

**Current:** Smooth sine/cosine cycles (breathing, walking, running)

**Rotborn needs:**
- Twitch (erratic jitter, not breathing)
- Broken walk (limping, dragging)
- Convulse (violent, fast)
- Lurch (slow, asymmetric)
- Collapse (one-shot, not looped)

### 4. Social Class → Corruption Source

**Current:** poor, working, middle, upper, rich

**Rotborn needs:**
- Ritual corruption (cult victim)
- Swarm infestation (nano-swarm host)
- Memory fracture (reality break survivor)
- Flesh architecture (alien geometry)
- Recursive decay (time-loop degradation)
- Void exposure (stared into swarm-rot)

---

## Implementation Order

### Phase 1: Strip GeneSwarm (2 hours)
1. Delete `generator/swarm/` directory
2. Delete `swarm_generator.py`
3. Remove swarm imports from `ai_human_generator.py`
4. Remove `generate-swarm` CLI command
5. Update `requirements.txt`

### Phase 2: Modify Core Palettes (3 hours)
1. Create `rotborn_palettes.py`
2. Replace `_create_inclusive_palette()`
3. Test single character generation

### Phase 3: Add Trauma System (4 hours)
1. Create `trauma_markers.py`
2. Add `_generate_trauma_params()`
3. Add `_draw_trauma_markers()`
4. Update `direction_renderer.py`

### Phase 4: Haunted Animations (4 hours)
1. Create `haunted_animations.py`
2. Add new animation types
3. Modify existing animations
4. Test sprite sheets

### Phase 5: CLI & Docs (3 hours)
1. Rename CLI commands
2. Update help text
3. Rewrite README.md
4. Create quick-start guide

### Phase 6: Testing (2 hours)
1. Batch generation tests
2. Verify deterministic seeding
3. Test all animations
4. Verify 4-directional rendering

---

## Dependencies

**Minimal (headless):**
```
Pillow>=10.0.0
numpy>=1.20.0
```

**With GUI:**
```
Pillow>=10.0.0
numpy>=1.20.0
PyQt6>=6.5.0
```

**Development:**
```
pytest>=7.0.0
ruff>=0.1.0
```

---

## Known Bugs (from PLAN.md)

| Bug | File | Severity |
|-----|------|----------|
| Missing `import time` | `swarm_generator.py` | CRASH (but we're stripping this) |
| `if seed:` should be `if seed is not None:` | `pure_generator.py` | Seed=0 ignored |
| Animated hair/face don't follow head offsets | `animation_generator.py` | Visual glitch |

---

## Next Steps

1. **Strip GeneSwarm** (this commit)
2. **Create trauma palettes** (next commit)
3. **Add trauma markers** (scars, bandages, mutations)
4. **Haunt animations** (twitch, shamble, convulse)
5. **Test & polish**

---

## Notes

- The deterministic generation core is **exactly** what's needed
- Only the aesthetic layer requires significant modification
- GeneSwarm AI is completely unnecessary for our use case
- GUI is optional (can be kept for visual editor, stripped for headless)
- Total transformation: ~12-18 hours of work
