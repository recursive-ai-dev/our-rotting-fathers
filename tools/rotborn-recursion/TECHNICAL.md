# TECHNICAL.md — API Reference & Integration Guide

---

## Architecture

```
rotborn_generator.py (CLI)
run_app.py (GUI launcher)
    │
    ├── factions/               Faction-specific generators
    │   ├── PurifiedGenerator
    │   ├── RotbornGenerator
    │   ├── ArchitectsGenerator
    │   └── SystemGenerator
    │       └── uses ──▶ generator/pure_generator.py
    │                    generator/broken_proportions.py
    │                    generator/anomaly_injector.py
    │                    generator/rotborn_palettes.py
    │
    ├── generator/              Core generation engine
    │   ├── pure_generator.py   Base sprite renderer (32x32 reference, scales up)
    │   ├── rotborn_palettes.py 5 trauma color palettes
    │   ├── broken_proportions.py 5 broken body types with faction weights
    │   ├── anomaly_injector.py 9 anomaly types at configurable rate
    │   ├── animation_generator.py Frame generation with pose offsets
    │   ├── animation_types.py  Animation definitions (frames, speed, loop)
    │   ├── direction_renderer.py 4-directional rendering
    │   └── mass_generator.py   Batch generation with uniqueness checking
    │
    ├── export/                 Export formats
    │   ├── apng_exporter.py    Animated PNG
    │   ├── sheet_builder.py    RPG Maker sprite sheets
    │   └── individual_exporter.py Individual frame files
    │
    └── app/                    PyQt6 GUI
        ├── dark_theme.py       Stylesheet
        ├── main_window.py      Main window
        ├── models/             Data model
        └── widgets/            UI components
```

---

## Core API

### PureCharacterGenerator

Base sprite renderer. All faction generators delegate to this.

```python
from generator.pure_generator import PureCharacterGenerator

gen = PureCharacterGenerator(
    canvas_size=(32, 32),   # Any square size
    palette="rotting"       # rotting|bloodstained|spore_infested|bone_dry|bruised
)

# Generate single sprite (deterministic)
sprite = gen.generate_character(seed=42)   # PIL.Image RGBA

# Generate with specific direction
from generator.direction_renderer import Direction
sprite = gen._render_character_with_params(params, direction=Direction.LEFT)
```

### Faction Generators

```python
from factions import get_faction_generator, FACTION_GENERATORS

# By name
gen = get_faction_generator("purified", canvas_size=(64, 64))

# Direct instantiation
from factions import PurifiedGenerator, RotbornGenerator, ArchitectsGenerator, SystemGenerator

# Generate single sprite
sprite = gen.generate(seed=42)

# Generate with rank/stage
sprite = PurifiedGenerator().generate(seed=42, rank="hollow")
sprite = RotbornGenerator().generate(seed=42, stage="bloom")
sprite = ArchitectsGenerator().generate(seed=42, role="enforcer")
sprite = SystemGenerator().generate(seed=42, implant_stage="prophet")

# Batch generation
sprites = gen.generate_batch(count=100, seed=1000)  # List[PIL.Image]
```

**Faction ranks/stages:**

| Faction | Parameter | Values |
|---------|-----------|--------|
| Purified | `rank` | `flesh_bound`, `memory_stripped`, `hollow` |
| Rotborn | `stage` | `seed`, `sprout`, `bloom`, `twisted` |
| Architects | `role` | `citizen`, `archivist`, `curator`, `enforcer` |
| System | `implant_stage` | `novice`, `synapse`, `relay`, `prophet` |

### Trauma Palettes

```python
from generator.rotborn_palettes import get_palette, get_palette_names, ALL_PALETTES

names = get_palette_names()
# ['rotting', 'bloodstained', 'spore_infested', 'bone_dry', 'bruised']

palette = get_palette("rotting")
# TraumaPalette(name, description, skin_tones, hair_colors, clothing_colors, eye_colors, accent_colors, mood)

print(palette.mood)
# "The god's flesh remembers being alive. It is wrong."
```

### Broken Proportions

```python
from generator.broken_proportions import (
    get_proportions, choose_proportions, apply_proportions_to_params,
    ALL_PROPORTIONS
)

# Get specific proportions
props = get_proportions("emaciated")
# BodyProportions(name, height_scale, width_scale, head_size, torso_width, ...)

# Choose faction-weighted proportions
props = choose_proportions(faction="purified")   # Favors emaciated/undead
props = choose_proportions(faction="rotborn")    # Favors bloated/mutated

# Apply to character params
params = apply_proportions_to_params(params, props)
# Adds params["body_metrics"]["broken_proportions"] dict
```

**Body types:**

| Type | Height | Width | Notes |
|------|--------|-------|-------|
| `emaciated` | 0.95x | 0.65x | Too thin. Head looks large. |
| `bloated` | 0.90x | 1.35x | Distended. Head pushed up. |
| `twisted` | 0.90x | 0.90x | Curved spine. Asymmetric. |
| `undead` | 1.00x | 0.75x | Desiccated. Hunched. |
| `mutated` | 1.05x | 1.10x | Extra limb chance 30%. |

### Anomaly Injector

```python
from generator.anomaly_injector import maybe_inject_anomaly, ANOMALIES, DEFAULT_ANOMALY_RATE

# DEFAULT_ANOMALY_RATE = 0.05 (5%)

# Standard injection
result, anomaly_name = maybe_inject_anomaly(sprite)
# anomaly_name is None if no anomaly was injected

# Custom rate
result, name = maybe_inject_anomaly(sprite, rate=0.10)

# Deterministic (with RNG)
import random
rng = random.Random(42)
result, name = maybe_inject_anomaly(sprite, rate=0.05, rng=rng)

# Force specific anomaly (for testing)
result, name = maybe_inject_anomaly(sprite, force_anomaly="too_many_eyes")
```

**Anomaly types:** `too_many_eyes`, `wrong_mouth`, `floating_part`, `recursive`, `inverted_region`, `translucent_skin`, `pixel_shift`, `shadow_twin`, `extra_limb`

### Animation Generator

```python
from generator.animation_generator import AnimationGenerator
from generator.animation_types import ANIMATION_DEFS, get_haunted_animation_types

anim_gen = AnimationGenerator(canvas_size=(32, 32))

# Generate frames
frames = anim_gen.generate_animation(params, "twitch")
# List[PIL.Image], length = ANIMATION_DEFS["twitch"].frames (3)

# With direction
from generator.direction_renderer import Direction
frames = anim_gen.generate_animation(params, "shamble", direction=Direction.LEFT)

# Export
anim_gen.create_sprite_sheet(frames, "output.png")   # Horizontal strip
anim_gen.create_gif(frames, "output.gif", duration=80)

# Haunted animation types
haunted = get_haunted_animation_types()
# ['twitch', 'shamble', 'convulse', 'stumble', 'worship', 'transform']
```

**Animation definitions:**

| Name | Frames | Loop | Speed (ms) |
|------|--------|------|------------|
| `twitch` | 3 | yes | 80 |
| `shamble` | 4 | yes | 180 |
| `convulse` | 3 | yes | 60 |
| `stumble` | 4 | no | 140 |
| `worship` | 6 | yes | 220 |
| `transform` | 5 | no | 160 |

### Export

```python
from export.apng_exporter import export_apng
from export.sheet_builder import build_rpg_sheet, build_single_direction_sheet
from export.individual_exporter import export_individual_frames

# APNG
export_apng(frames, "output.png", duration_ms=80)

# RPG Maker sheet (4 rows: down/left/right/up, N columns)
frames_by_dir = {Direction.DOWN: [...], Direction.LEFT: [...], ...}
build_rpg_sheet(frames_by_dir, "rpg_sheet.png")

# Single direction sheet
build_single_direction_sheet(frames, "sheet.png", horizontal=True)

# Individual files
paths = export_individual_frames(frames_by_dir, output_dir, "twitch")
```

---

## Godot Integration

### Import sprites

1. Copy generated PNGs to `game/godot/assets/sprites/characters/`
2. In Godot: Import as `Texture2D`, set filter to `Nearest` (pixel art)
3. For sprite sheets: use `AnimatedSprite2D` with `SpriteFrames` resource

### Sprite sheet layout (RPG Maker format)

```
Row 0: Direction.DOWN  (front-facing)
Row 1: Direction.LEFT
Row 2: Direction.RIGHT
Row 3: Direction.UP    (back-facing)
```

Each row has N frames (N = animation frame count).

### Example GDScript

```gdscript
# Load a generated sprite sheet
var texture = load("res://assets/sprites/characters/rotborn/twitch_sheet.png")
var sprite_frames = SpriteFrames.new()

# Add animation (3 frames, 80ms each = ~12.5 FPS)
sprite_frames.add_animation("twitch")
sprite_frames.set_animation_loop("twitch", true)
sprite_frames.set_animation_speed("twitch", 12.5)

var frame_width = texture.get_width() / 3  # 3 frames
for i in range(3):
    var atlas = AtlasTexture.new()
    atlas.atlas = texture
    atlas.region = Rect2(i * frame_width, 0, frame_width, texture.get_height())
    sprite_frames.add_frame("twitch", atlas)

$AnimatedSprite2D.sprite_frames = sprite_frames
$AnimatedSprite2D.play("twitch")
```

---

## Batch Generation for Game Assets

```python
from factions import get_faction_generator

# Generate 50 sprites per faction for NPC population
for faction in ["purified", "rotborn", "architects", "system"]:
    gen = get_faction_generator(faction, canvas_size=(32, 32))
    sprites = gen.generate_batch(count=50, seed=faction_seeds[faction])
    for i, sprite in enumerate(sprites):
        sprite.save(f"assets/{faction}_{i:03d}.png")
```

For deterministic NPC generation in-game (same seed = same NPC appearance every run):

```python
# NPC ID as seed — always generates the same sprite
npc_id = 12345
gen = get_faction_generator("rotborn")
sprite = gen.generate(seed=npc_id)
```

---

## Configuration

### Anomaly rate

```python
from generator.anomaly_injector import DEFAULT_ANOMALY_RATE
# 0.05 by default — pass rate= to maybe_inject_anomaly() to override
```

### Faction body weights

```python
from generator.broken_proportions import FACTION_BODY_WEIGHTS
# Dict[faction_name, Dict[body_type, weight]]
# Modify to change faction aesthetics
```

### Adding a new palette

```python
from generator.rotborn_palettes import TraumaPalette, ALL_PALETTES

MY_PALETTE = TraumaPalette(
    name="void_touched",
    description="...",
    skin_tones=[(r, g, b), ...],   # At least 5
    hair_colors=[(r, g, b), ...],  # At least 4
    clothing_colors=[(r, g, b), ...],
    eye_colors=[(r, g, b), ...],
    accent_colors=[(r, g, b), ...],
    mood="..."
)
ALL_PALETTES["void_touched"] = MY_PALETTE
```

---

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Specific test files
python -m pytest tests/test_determinism.py -v
python -m pytest tests/test_factions.py -v
python -m pytest tests/test_haunted_animations.py -v

# With coverage
python -m pytest tests/ --cov=generator --cov=factions --cov-report=term-missing
```

Current coverage: 81 tests, all passing.

---

## Performance

Benchmarks on a typical development machine:

| Operation | Count | Time |
|-----------|-------|------|
| Single sprite (32×32) | 1 | ~2ms |
| Batch generation | 100 | ~0.2s |
| Batch generation | 1000 | ~2s |
| Animation (6 frames, 32×32) | 1 | ~12ms |
| Faction sprite (32×32) | 1 | ~3ms |

Bottleneck: PIL drawing operations. No external dependencies beyond Pillow.

---

## Dependencies

```
Pillow >= 10.0.0    # Required — sprite rendering
PyQt6 >= 6.5.0      # Optional — GUI only
pytest >= 7.0.0     # Development — testing
```

No numpy required for core generation.
