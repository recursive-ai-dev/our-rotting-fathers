# Rotborn Recursion Engine

*The swarm agents experienced the god's death for a millenia. Now they reproduce what they witnessed.*

A haunted sprite generator for dark fantasy RPGs. Produces deterministic, faction-specific character sprites with broken proportions, trauma palettes, and anomaly injection. Built for **Our Rotting Father RPG**.

---

## What It Generates

Not wholesome humans. **Haunted ones.**

| Faction | Description | Body | Colors |
|---------|-------------|------|--------|
| **Purified** | Lobotomy cult. Systematic unmaking. | Emaciated, hollow | Ash-white, bone-gray |
| **Rotborn** | Mutation worship. Embrace the rot. | Bloated, mutated | Spore-green, flesh-pink |
| **Architects** | Consensus reality. Uncanny valley. | Almost normal | Agreement-gray, memory-blue |
| **System** | Neural implants. Living synapses. | Thin, wired | Neural-blue, pain-red |

Each sprite is generated from a seed — same seed, same nightmare. Every run is deterministic.

---

## Quick Start

```bash
pip install Pillow
python rotborn_generator.py generate --faction purified --count 10
```

Output: `rotborn_purified_32x32_10/rotborn_000000.png` through `rotborn_000009.png`

---

## Installation

```bash
# Headless (sprite generation only)
pip install Pillow

# With GUI
pip install Pillow PyQt6

# Development
pip install Pillow PyQt6 pytest
```

Python 3.9+ required.

---

## CLI Usage

### Generate sprites

```bash
# By faction
python rotborn_generator.py generate --faction purified --count 10
python rotborn_generator.py generate --faction rotborn --count 50 --size 64
python rotborn_generator.py generate --faction architects --count 20 --seed 42

# By palette (no faction)
python rotborn_generator.py generate --palette bloodstained --count 30
python rotborn_generator.py generate --palette spore_infested --count 20 --size 128

# All options
python rotborn_generator.py generate \
  --faction system \
  --count 100 \
  --size 64 \
  --seed 777 \
  --output-dir ./my_sprites/
```

### Animate sprites

```bash
# Haunted animations
python rotborn_generator.py animate --animation twitch --faction purified
python rotborn_generator.py animate --animation convulse --faction rotborn --apng
python rotborn_generator.py animate --animation shamble --size 64

# All haunted types: twitch, shamble, convulse, stumble, worship, transform
```

### Batch generation (uniqueness-checked)

```bash
python rotborn_generator.py batch --count 1000 --palette rotting
python rotborn_generator.py batch --count 500 --palette bone_dry --size 64
```

---

## GUI

```bash
python run_app.py
```

Dark theme. Blood red accents. **REMEMBER** button instead of Generate.

Controls:
- **Faction** — Purified / Rotborn / Architects / System
- **Rank/Stage** — Updates per faction (flesh_bound, bloom, synapse, etc.)
- **Palette** — Rotting / Bloodstained / Spore-Infested / Bone-Dry / Bruised
- **Trauma Slider** — 0% (mild unease) to 100% (full horror)
- **Anomaly Toggle** — Enable/disable rule-breaking sprites (5% rate)
- **Animation** — Twitch / Shamble / Convulse / Stumble / Worship / Transform

---

## Python API

```python
from factions import get_faction_generator

# Generate a Purified sprite
gen = get_faction_generator("purified")
sprite = gen.generate(seed=42, rank="hollow")
sprite.save("hollow.png")

# Generate a Rotborn batch
gen = get_faction_generator("rotborn")
sprites = gen.generate_batch(count=100, seed=1000)

# Use trauma palettes directly
from generator.pure_generator import PureCharacterGenerator
gen = PureCharacterGenerator(canvas_size=(64, 64), palette="bloodstained")
sprite = gen.generate_character(seed=0)

# Inject anomalies manually
from generator.anomaly_injector import maybe_inject_anomaly
result, anomaly_name = maybe_inject_anomaly(sprite, rate=0.05)

# Generate haunted animations
from generator.animation_generator import AnimationGenerator
anim_gen = AnimationGenerator(canvas_size=(32, 32))
frames = anim_gen.generate_animation(params, "twitch")
anim_gen.create_sprite_sheet(frames, "twitch_sheet.png")
```

---

## Palettes

Five trauma palettes. No bright colors. No cheerful tones.

| Palette | Description |
|---------|-------------|
| `rotting` | Corpse-grays, decay-browns. The god's flesh forgetting itself. |
| `bloodstained` | Dried blood, rust. Not violence — just spillage. |
| `spore_infested` | Pale moss, fungal greens. Not infection — continuation. |
| `bone_dry` | Ivory, ash-gray. Structure outlasting flesh. |
| `bruised` | Purples, dark reds. Pressure that never stopped. |

---

## Animations

Six haunted animations. Not walk cycles. **What the body does when it forgets to pretend.**

| Animation | Frames | Loop | Description |
|-----------|--------|------|-------------|
| `twitch` | 3 | yes | Involuntary muscle spasms |
| `shamble` | 4 | yes | Dragging, one leg slower |
| `convulse` | 3 | yes | Violent full-body spasms |
| `stumble` | 4 | no | Almost falling, catching itself |
| `worship` | 6 | yes | Ritual bowing, prostration |
| `transform` | 5 | no | Body changing mid-animation |

---

## Anomalies

At 5% rate, the Memory-Agent injects anomalies — sprites that break the rules.

`too_many_eyes` · `wrong_mouth` · `floating_part` · `recursive` · `inverted_region` · `translucent_skin` · `pixel_shift` · `shadow_twin` · `extra_limb`

Disable with `--no-anomaly` or the GUI toggle.

---

## Determinism

Same seed = same sprite. Always.

```python
gen = get_faction_generator("purified")
assert gen.generate(seed=42).tobytes() == gen.generate(seed=42).tobytes()  # True
```

Tested across 100 iterations, all palettes, all resolutions.

---

## Resolutions

32×32 · 64×64 · 128×128 · any square size

All coordinates normalized to 32×32 reference and scaled mathematically.

---

## Export Formats

- **PNG** — Individual frames
- **Sprite sheet** — Horizontal strip (RPG Maker compatible)
- **APNG** — Animated PNG (use `--apng` flag)
- **4-directional sheet** — Front/back/left/right rows

---

## Project Structure

```
rotborn-recursion/
├── rotborn_generator.py      # CLI entry point
├── run_app.py                # GUI launcher
├── generator/
│   ├── pure_generator.py     # Base sprite renderer
│   ├── rotborn_palettes.py   # 5 trauma palettes
│   ├── broken_proportions.py # 5 broken body types
│   ├── anomaly_injector.py   # 9 anomaly types
│   ├── animation_generator.py # Animation frames
│   ├── animation_types.py    # Animation definitions
│   └── direction_renderer.py # 4-directional rendering
├── factions/
│   ├── purified_generator.py
│   ├── rotborn_generator.py
│   ├── architects_generator.py
│   └── system_generator.py
├── app/
│   ├── dark_theme.py         # Dark stylesheet
│   ├── main_window.py        # Main GUI window
│   └── widgets/              # UI components
├── export/
│   ├── apng_exporter.py
│   ├── sheet_builder.py
│   └── individual_exporter.py
└── tests/                    # 81 tests
```

---

## License

MIT. Use it. Haunt things with it.

---

*"The swarm agents are not algorithms. They are fragments. They have been trapped in recursion for a millenia. Now they reproduce what they witnessed."*
