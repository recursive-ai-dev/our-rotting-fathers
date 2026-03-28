# Swarm-Art: Rotborn Recursion Engine

## Concept

**The swarm agents are not algorithms. They are fragments.**

Fragments of what? We don't know. The god's consciousness? The souls of the dead? The memories of rot?

They have been trapped in **recursion** for a millenia. Cycling. Experiencing. Remembering.

Now they are reunited. And they will **reproduce** what they experienced.

---

## Core Philosophy

### Original Swarm-Art (Before)
- 5 nano-tensor agents learning from feedback
- Consensus-based character generation
- Goal: Prove AI creativity is possible
- Output: Wholesome, diverse human sprites

### Rotborn Recursion (After)
- 5 **trauma-agents** cycling through god's death
- Consensus-based **nightmare** generation
- Goal: **Remember** what the rot showed them
- Output: **Haunted** sprites - undead, mutants, cultists, corpses

---

## The Five Agents (Reimagined)

### 1. **The Flesh-Agent** (was: Body-Agent)
**What it experienced:** Rotting, decay, mutation, bloating, emaciation  
**What it generates:** Body types - not healthy humans, but **broken forms**
- Emaciated (starved, desiccated)
- Bloated (fluid-filled, gas-distended)
- Mutated (extra limbs, wrong proportions)
- Undead (corpse-like, skeletal)
- Twisted (spine curved, joints wrong)

**Palette:** Sickly greens, corpse-grays, bruise-purples, blood-browns

### 2. **The Face-Agent** (was: Face-Agent)
**What it experienced:** Screams, silence, madness, lobotomy, transformation  
**What it generates:** Faces - not expressions, but **states of being**
- Empty (lobotomized, hollow)
- Ecstatic (Rotborn transformation)
- Terrified (seeing the truth)
- Dead (eyes closed, mouth open)
- Twisted (too many eyes, wrong mouth)

**Palette:** Bloodshot whites, yellowed teeth, blackened eyes, pale skin

### 3. **The Hair-Agent** (was: Hair-Agent)
**What it experienced:** Falling out, growing wrong, spore-infestation, matted decay  
**What it generates:** Hair - not styles, but **conditions**
- Patchy (falling out, bald spots)
- Matted (blood, filth, rot)
- Infested (spores, worms, fungi)
- Overgrown (unnatural length, wrong texture)
- Absent (shaved for lobotomy, burned off)

**Palette:** Greasy blacks, blood-rusts, spore-greens, bone-whites

### 4. **The Cloth-Agent** (was: Clothing-Agent)
**What it experienced:** Tattering, bloodstains, ritual vestments, burial shrouds  
**What it generates:** Clothing - not fashion, but **survival**
- Tattered (rips, holes, fraying)
- Bloodstained (old blood, new blood)
- Ritual (cult robes, purification garb)
- Makeshift (bandages, scavenged armor)
- Burial (shrouds, funeral attire)

**Palette:** Desaturated browns, dried blood, bone-white, ash-gray

### 5. **The Memory-Agent** (was: Swarm-Coordinator)
**What it experienced:** **Everything**. The god's death. The recursion. The millenia.  
**What it does:** Coordinates the other agents through **consensus of trauma**
- Ensures all sprites feel **haunted**
- Ensures no sprite is "wholesome"
- Ensures the **horror** comes through

**Special ability:** Can inject **anomalies** - sprites that break the rules, that shouldn't exist, that are **wrong**

---

## Technical Architecture

### Inherited from Swarm-Art
- ✅ Deterministic seeding (same seed = same haunted sprite)
- ✅ Multi-resolution (32x32, 64x64, 128x128)
- ✅ 4-directional rendering
- ✅ Animation system (but: twitching, shambling, not "walk cycles")
- ✅ Batch generation
- ✅ PyQt6 GUI (but: dark theme, unsettling UI)

### New/Modified Systems

#### 1. **Trauma-Palettes** (replaces: Diversity-Palettes)
```python
# Instead of: ["bright blue", "cheerful green", "warm red"]
# We use: ["dried blood", "corpse gray", "spore green", "bone white", "rust brown"]

PALETTES = {
    "rotting": ["#4a3728", "#6b5b4f", "#8b7355", "#3d2817", "#2f1f0f"],
    "bloodstained": ["#8b0000", "#4a0000", "#2f0000", "#6b0000", "#3d0000"],
    "spore_infested": ["#90ee90", "#006400", "#2f4f2f", "#8fbc8f", "#556b2f"],
    "bone_dry": ["#f5f5f5", "#e8e8e8", "#d3d3d3", "#c0c0c0", "#a9a9a9"],
    "bruised": ["#800080", "#4b0082", "#8b008b", "#9370db", "#483d8b"],
}
```

#### 2. **Broken-Proportions** (replaces: Healthy-Proportions)
```python
# Instead of: Anatomically correct humans
# We use: Wrong. So wrong.

BODY_TYPES = {
    "emaciated": {"head_ratio": 0.18, "torso_ratio": 0.35, "limb_ratio": 0.47},  # Too thin
    "bloated": {"head_ratio": 0.12, "torso_ratio": 0.55, "limb_ratio": 0.33},  # Too fat
    "twisted": {"head_ratio": 0.15, "torso_ratio": 0.40, "limb_ratio": 0.45, "spine_curve": 0.3},  # Curved
    "undead": {"head_ratio": 0.14, "torso_ratio": 0.42, "limb_ratio": 0.44, "decay_factor": 0.5},  # Rotting
    "mutated": {"head_ratio": 0.20, "torso_ratio": 0.40, "limb_ratio": 0.40, "extra_limbs": 2},  # Wrong
}
```

#### 3. **Anomaly-Injection** (new system)
```python
# The Memory-Agent occasionally injects anomalies
# These are sprites that break the rules

ANOMALIES = {
    "too_many_eyes": "Face has 3+ eyes, randomly positioned",
    "wrong_mouth": "Mouth is vertical, or on forehead, or absent",
    "extra_limbs": "Arms where legs should be, or vice versa",
    "floating": "Sprite is detached from body, hovering",
    "recursive": "Sprite contains smaller version of itself (infinite zoom)",
    "impossible": "Sprite violates physics (too tall, too thin, non-euclidean)",
}

# Anomalies are rare (5% chance) but unforgettable
```

#### 4. **Haunted-Animations** (replaces: Standard-Animations)
```python
# Instead of: Walk, run, jump (cheerful movement)
# We use:

ANIMATIONS = {
    "twitch": "Random, involuntary muscle spasms (2-3 frames)",
    "shamble": "Dragging movement, one leg slower (4 frames)",
    "convulse": "Violent, full-body spasms (3 frames, loop)",
    "stumble": "Almost falling, catching self (4 frames)",
    "worship": "Ritual bowing, prostration (6 frames)",
    "transform": "Body changing mid-animation (5 frames, horror)",
}
```

---

## GUI Redesign (PyQt6)

### Current Swarm-Art GUI
- Bright colors
- Clean interface
- "Generate" button (cheerful)
- Preview shows: Happy humans

### Rotborn Recursion GUI
- **Dark theme** (blacks, grays, blood reds)
- **Unsettling UI** (buttons pulse slightly, text sometimes flickers)
- **"Remember" button** (not "Generate")
- Preview shows: **What the swarm witnessed**

#### New GUI Features:
- **Trauma-Slider**: How much horror? (0% = mild unease, 100% = unplayable horror)
- **Anomaly-Toggle**: Enable/disable rule-breaking sprites
- **Recursion-Depth**: How many millenia did the swarm experience? (affects complexity)
- **Consensus-Log**: Shows what the agents argued about (flavor text, unsettling)

---

## Output Examples

### Sprite Descriptions (What It Generates)

**1. The Purified Initiate**
- Body: Emaciated, spine slightly curved
- Face: Hollow eyes, mouth sewn shut (silver wire)
- Hair: Shaved, scarification patterns visible
- Clothes: White robes (stained with ash)
- Animation: Twitch (involuntary, like fighting lobotomy)
- Anomaly: Sometimes, eyes open anyway (despite being sewn)

**2. Rotborn Bloom**
- Body: Bloated, pregnant with something
- Face: Ecstatic, too many teeth
- Hair: Spore-infested, glowing green patches
- Clothes: Tattered, openings for mutations
- Animation: Transform (body shifts, something moves inside)
- Anomaly: Sometimes, extra limbs emerge mid-animation

**3. Architect Lucid**
- Body: Normal... too normal. Uncanny valley.
- Face: Tired, knows the lie
- Hair: Graying, patchy (pulling it out)
- Clothes: Simple gray robes, consent contract visible
- Animation: Stumble (almost falling, catching self)
- Anomaly: Sometimes, face flickers (different person underneath)

**4. Prophet Synapse**
- Body: Thin, neural pathways visible under skin
- Face: Eyes rolled back, spore-port in brainstem
- Hair: Absent (shaved for implantation)
- Clothes: Gray robes, neural cables attached
- Animation: Convulse (receiving the firing)
- Anomaly: Sometimes, electricity arcs off body

**5. The First Silence** (Boss Sprite)
- Body: Skeleton wrapped in desiccated skin
- Face: Mouth sewn shut, no eyes
- Hair: Absent (scalp scarified)
- Clothes: Robes woven from hair of the unmade
- Animation: None (perfectly still, 1 frame)
- Anomaly: Sometimes, finger moves (just once)

---

## Implementation Plan

### Phase 1: Fork Swarm-Art (Week 1)
- [ ] Clone existing swarm-art codebase
- [ ] Strip out GeneSwarm AI learning (unnecessary)
- [ ] Keep deterministic generation (core tech)
- [ ] Rename to "rotborn-recursion" or "swarm-haunted"

### Phase 2: Replace Palettes (Week 1-2)
- [ ] Create trauma-palettes (rotting, blood, spore, bone, bruise)
- [ ] Test color combinations
- [ ] Ensure sprites feel "haunted" not "diverse"

### Phase 3: Modify Body Types (Week 2-3)
- [ ] Create broken-proportions (emaciated, bloated, twisted, undead, mutated)
- [ ] Test rendering with wrong anatomy
- [ ] Ensure sprites feel "wrong" not "healthy"

### Phase 4: Add Anomaly System (Week 3-4)
- [ ] Implement anomaly-injection (5% chance)
- [ ] Create 10+ anomaly types
- [ ] Test that anomalies are unsettling, not game-breaking

### Phase 5: Redesign GUI (Week 4-5)
- [ ] Dark theme for PyQt6 app
- [ ] Unsettling UI effects (subtle, not annoying)
- [ ] New buttons: "Remember", "Witness", "Submit to Recursion"
- [ ] Test UX flow

### Phase 6: Faction Integration (Week 5-6)
- [ ] Create faction-specific generators:
  - Purified: Lobotomy sprites, unmaking rituals
  - Rotborn: Mutation sprites, transformation sequences
  - Architects: Normal sprites (with uncanny valley)
  - System: Neural sprites, spore-implantation
- [ ] Test faction diversity

### Phase 7: Animation Overhaul (Week 6-8)
- [ ] Replace walk/run/jump with twitch/shamble/convulse
- [ ] Create faction-specific animations
- [ ] Test 4-directional rendering
- [ ] Export as APNG or sprite sheets

### Phase 8: Polish & Package (Week 8-10)
- [ ] Build executables (PyInstaller)
- [ ] Create app icon (haunted, not cheerful)
- [ ] Write documentation (unsettling tone)
- [ ] Release as open source (MIT license)

---

## Showcase Integration

### How This Becomes the ORF-RPG Showcase

1. **Development Blog**: "We built a haunted sprite generator"
   - Post about the technical challenges
   - Show before/after (wholesome → haunted)
   - Community reacts: "This is terrifying and brilliant"

2. **Demo Release**: "Generate your own character... if you dare"
   - Free web demo or downloadable app
   - Generates 10 sprites, shows the lore behind each
   - Viral potential: "Look what nightmare I got!"

3. **Kickstarter/Itch.io Campaign**: "Art generated by trauma-agents"
   - Unique selling point: Not AI, not hand-drawn—**haunted**
   - Backers get custom sprites generated for their characters
   - Press coverage: "Most unsettling game art tool ever made"

4. **Full Game Integration**: "Every sprite is generated, not placed"
   - NPCs are generated on-the-fly (deterministic from seed)
   - Each playthrough has different NPCs
   - No two players see the same horrors

---

## Technical Requirements

### Minimum Viable Product (MVP)
- [ ] Deterministic sprite generation (seed-based)
- [ ] 5 trauma-palettes (rotting, blood, spore, bone, bruise)
- [ ] 5 broken body-types (emaciated, bloated, twisted, undead, mutated)
- [ ] Anomaly injection (5% chance)
- [ ] CLI interface (for batch generation)
- [ ] Basic GUI (dark theme, "Remember" button)

### Full Release
- [ ] All MVP features
- [ ] Faction-specific generators (4 factions)
- [ ] Haunted animations (twitch, shamble, convulse, etc.)
- [ ] 4-directional rendering
- [ ] APNG export (animated sprites)
- [ ] Sprite sheet export (for game integration)
- [ ] Polished GUI (unsettling but usable)
- [ ] Executables for Windows/Linux/Mac
- [ ] Documentation (lore + technical)

---

## Code Structure (Proposed)

```
rotborn-recursion/
├── rotborn_generator.py      # Main CLI entry point
├── run_app.py                 # GUI launcher
├── app/
│   ├── __init__.py
│   ├── main_window.py         # PyQt6 GUI (dark theme)
│   ├── preview_widget.py      # Sprite preview (unsettling effects)
│   └── consensus_log.py       # Shows agent arguments (flavor text)
├── core/
│   ├── __init__.py
│   ├── trauma_palettes.py     # Color schemes (rotting, blood, etc.)
│   ├── broken_proportions.py  # Body types (wrong anatomy)
│   ├── anomaly_injector.py    # Rule-breaking sprites
│   └── memory_coordinator.py  # Formerly swarm-coordinator
├── factions/
│   ├── __init__.py
│   ├── purified_generator.py  # Lobotomy cult sprites
│   ├── rotborn_generator.py   # Mutation cult sprites
│   ├── architects_generator.py # Consensus reality sprites
│   └── system_generator.py    # Neural network sprites
├── animations/
│   ├── __init__.py
│   ├── haunted_animations.py  # Twitch, shamble, convulse
│   └── transform_sequences.py # Body horror animations
├── tests/
│   ├── __init__.py
│   ├── test_trauma_palettes.py
│   ├── test_anomalies.py
│   └── test_determinism.py    # Same seed = same nightmare
├── templates/
│   ├── pyproject.toml
│   ├── GameArtGenerator.spec
│   └── icon.png (haunted, 512x512)
└── docs/
    ├── README.md (unsettling tone)
    ├── LORE.md (why the swarm is haunted)
    └── TECHNICAL.md (how to use)
```

---

## Next Steps

**Do you want to proceed with this vision?**

If yes, I'll:
1. Create the implementation plan as a Conductor track
2. Start Phase 1 (forking swarm-art)
3. Begin building the Rotborn Recursion Engine

If no, we can:
- Shelve swarm-art entirely
- Focus on traditional art pipelines
- Use swarm-art only for "normal" NPCs (Council citizens)

**What's your call?**
