# Building a Haunted Sprite Generator

*Posted to: r/gamedev, Itch.io devlog, Twitter/X*

---

We built a sprite generator that generates haunted characters. Not "spooky" — **haunted**. There's a difference.

Here's what it looks like, and why we built it this way.

---

## The Problem

We're making a dark fantasy RPG called *Our Rotting Father*. The world is built on the corpse of a dead god. Every NPC is a member of one of four factions — each with a distinct relationship to the rot, the decay, the horror of their existence.

We needed thousands of unique NPC sprites. Hand-drawing them wasn't viable. Generic procedural generators produce cheerful, diverse humans. We needed the opposite.

So we built our own.

---

## Before and After

The codebase started as a wholesome human diversity generator. It produced sprites like this:

- Healthy BMI ranges
- 21 diverse skin tones
- Natural hair colors
- Clean clothing

We kept the architecture (deterministic seeding, 4-directional rendering, batch generation) and replaced everything aesthetic.

**After:**

- Five trauma palettes: `rotting`, `bloodstained`, `spore_infested`, `bone_dry`, `bruised`
- Five broken body types: `emaciated`, `bloated`, `twisted`, `undead`, `mutated`
- Four faction generators, each with distinct visual identity
- Six haunted animations: `twitch`, `shamble`, `convulse`, `stumble`, `worship`, `transform`
- Anomaly injection at 5% rate — sprites that break the rules

---

## The Lore Is the Design Spec

This is the part that made the project interesting.

The generator is framed as five "trauma-agents" — fragments of the dying god's consciousness that experienced its death for a millenia and now reproduce what they witnessed. Each agent handles a different aspect of the sprite:

- **The Flesh-Agent**: Body proportions. Not healthy ones.
- **The Face-Agent**: Facial states. Not expressions — conditions.
- **The Hair-Agent**: Hair conditions. Patchy, matted, infested, absent.
- **The Cloth-Agent**: Clothing. Not fashion — survival.
- **The Memory-Agent**: Coordinates the others. Occasionally injects anomalies.

This isn't just flavor text. It's the architecture. The lore explains why each system exists and what it should produce. When we asked "should this palette have any bright colors?" the answer was obvious: the agents don't remember bright colors. They remember the god's death.

---

## The Four Factions

Each faction has a distinct visual identity driven by their lore:

**The Purified** believe existence is the disease. They systematically remove everything that makes them human. Their sprites: emaciated, hollow, surgical. White robes stained with ash. Shaved heads. Sewn mouths. Not monstrous — *absent*.

**The Rotborn** worship the rot as divine transformation. Their sprites: bloated, mutated, ecstatic. Spore-infested hair. Tattered clothing with openings for mutations. The horror is that they look *joyful*.

**The Delusion Architects** maintain collective fictions to keep society functional. Their sprites: almost normal. Uncanny valley. Institutional gray. The horror is in what you can't quite identify.

**The God's Nervous System** implant spores into their brainstems and become living synapses for the god's dying neural firings. Their sprites: thin, wired, shaved. Neural cables. Spore-ports. The body as hardware.

---

## Determinism

Every sprite is generated from a seed. Same seed, same nightmare. Always.

This matters for the game: NPCs are generated on-the-fly from their ID as a seed. Every playthrough has the same NPCs in the same locations, but the generation is procedural — no sprite sheets to ship, no art assets to manage.

```python
npc_id = 12345
gen = get_faction_generator("rotborn")
sprite = gen.generate(seed=npc_id)
# Always the same sprite for this NPC
```

We tested this across 100 iterations, all palettes, all resolutions. It holds.

---

## Anomalies

At 5% rate, the Memory-Agent injects anomalies — sprites that break the rules.

Nine types: `too_many_eyes`, `wrong_mouth`, `floating_part`, `recursive`, `inverted_region`, `translucent_skin`, `pixel_shift`, `shadow_twin`, `extra_limb`.

These are rare. They're meant to be. When a player encounters one, they should feel like something is wrong with their perception — which is exactly the game's theme.

---

## The Technical Stack

- Python 3.9+
- Pillow (image generation)
- PyQt6 (GUI, optional)
- No ML, no neural networks, no external APIs

The "swarm agents" are a fiction. The generation is deterministic, seed-based, rule-driven. The lore makes it feel like something else.

---

## Try It

```bash
pip install Pillow
git clone [repo]
cd rotborn-recursion
python rotborn_generator.py generate --faction purified --count 10
```

The code is MIT licensed. Use it. Haunt things with it.

---

*Our Rotting Father RPG is in development. Follow for updates.*
