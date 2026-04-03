# Itch.io Page Copy — Rotborn Recursion Engine

**Title:** Rotborn Recursion Engine — Haunted Sprite Generator

**Tagline:** *The swarm agents experienced the god's death for a millenia. Now they reproduce what they witnessed.*

---

## Short Description (140 chars)

Procedural dark fantasy sprite generator. 4 factions, 5 trauma palettes, haunted animations. Deterministic. MIT licensed.

---

## Full Description

The Rotborn Recursion Engine generates haunted character sprites for dark fantasy RPGs.

Not wholesome humans. **Haunted ones.**

---

### What It Generates

**The Purified** — Lobotomy cult. Systematic unmaking. Emaciated bodies, hollow faces, ash-white robes. Not monstrous. Absent.

**The Rotborn** — Mutation worship. Bloated, spore-infested, ecstatic. The horror is that they look joyful.

**The Delusion Architects** — Consensus reality. Almost normal. Uncanny valley. The horror is in what you can't identify.

**The God's Nervous System** — Neural implants. Thin, wired, shaved. The body as hardware.

---

### Features

- **4 faction generators** — each with distinct visual identity, ranks, and stages
- **5 trauma palettes** — rotting, bloodstained, spore-infested, bone-dry, bruised
- **5 broken body types** — emaciated, bloated, twisted, undead, mutated
- **6 haunted animations** — twitch, shamble, convulse, stumble, worship, transform
- **Anomaly injection** — 5% chance of rule-breaking sprites (too many eyes, wrong mouth, recursive self...)
- **Deterministic** — same seed, same nightmare, always
- **4-directional rendering** — front/back/left/right
- **Multiple resolutions** — 32×32, 64×64, 128×128, or any square size
- **Export formats** — PNG, sprite sheets, APNG, RPG Maker compatible
- **Dark GUI** — PyQt6 app with "REMEMBER" button instead of "Generate"
- **CLI** — `python rotborn_generator.py generate --faction purified --count 10`

---

### For Game Developers

Every sprite is generated from a seed. Use your NPC's ID as the seed — same NPC, same appearance, every run. No sprite sheets to ship.

```python
from factions import get_faction_generator
gen = get_faction_generator("rotborn")
sprite = gen.generate(seed=npc_id)
```

Godot integration guide included.

---

### Technical

- Python 3.9+
- Pillow (required), PyQt6 (optional, for GUI)
- No ML, no neural networks, no external APIs
- MIT licensed — use it, modify it, haunt things with it

---

**Price:** Pay what you want (source on GitHub)

**Tags:** sprite-generator, pixel-art, dark-fantasy, procedural, game-dev, horror, python, open-source

---

## Screenshots Needed

1. Side-by-side: 4 faction sprites (purified/rotborn/architects/system) at 64×64
2. Palette comparison: same character in all 5 palettes
3. Animation strip: twitch animation (3 frames)
4. GUI screenshot: dark theme with REMEMBER button
5. Anomaly example: sprite with too_many_eyes or wrong_mouth
