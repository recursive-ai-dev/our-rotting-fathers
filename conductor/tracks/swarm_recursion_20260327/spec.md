# Track Specification: Rotborn Recursion Engine

## Track Overview

**Track ID:** swarm_recursion_20260327  
**Type:** Feature/Technical  
**Status:** New  
**Priority:** High (Showcase for ORF-RPG)

---

## Objectives

Repurpose the existing swarm-art codebase into a **haunted sprite generator** that produces dark fantasy character sprites for "Our Rotting Father RPG". The swarm agents are reimagined as trauma-fragments that experienced the god's death for a millenia and now reproduce what they witnessed.

### Primary Goals

1. **Fork swarm-art** - Clone existing codebase, strip GeneSwarm AI, keep deterministic generation
2. **Replace all visual systems** - Trauma-palettes, broken-proportions, anomaly-injection
3. **Create faction generators** - Purified, Rotborn, Architects, System-specific sprites
4. **Build haunted animations** - Twitch, shamble, convulse (not walk/run/jump)
5. **Redesign GUI** - Dark theme, unsettling UI, "Remember" button
6. **Package for distribution** - Executables for Windows/Linux/Mac, documentation

---

## Deliverables

### 1. Core Engine
- [ ] `rotborn_generator.py` - Main CLI entry point
- [ ] `core/trauma_palettes.py` - Color schemes (rotting, blood, spore, bone, bruise)
- [ ] `core/broken_proportions.py` - Body types (wrong anatomy)
- [ ] `core/anomaly_injector.py` - Rule-breaking sprites (5% chance)
- [ ] `core/memory_coordinator.py` - Trauma consensus system

### 2. Faction Generators
- [ ] `factions/purified_generator.py` - Lobotomy cult sprites (unmaking, hollow)
- [ ] `factions/rotborn_generator.py` - Mutation cult sprites (transformation, bloated)
- [ ] `factions/architects_generator.py` - Consensus reality sprites (uncanny valley)
- [ ] `factions/system_generator.py` - Neural network sprites (spore-implanted, firing)

### 3. Animation System
- [ ] `animations/haunted_animations.py` - Twitch, shamble, convulse, stumble
- [ ] `animations/transform_sequences.py` - Body horror transformation animations
- [ ] 4-directional rendering (front/back/left/right)
- [ ] APNG export (animated sprites)
- [ ] Sprite sheet export (for game integration)

### 4. GUI Application
- [ ] `app/main_window.py` - PyQt6 GUI (dark theme)
- [ ] `app/preview_widget.py` - Sprite preview (unsettling effects)
- [ ] `app/consensus_log.py` - Agent arguments (flavor text)
- [ ] Dark theme (blacks, grays, blood reds)
- [ ] Unsettling UI effects (subtle pulse, flicker)

### 5. Testing & Quality
- [ ] `tests/test_trauma_palettes.py` - Color accuracy
- [ ] `tests/test_anomalies.py` - Anomaly injection works
- [ ] `tests/test_determinism.py` - Same seed = same nightmare
- [ ] `tests/test_factions.py` - Each faction distinct
- [ ] 20+ passing tests

### 6. Documentation & Packaging
- [ ] `README.md` - Unsettling tone, usage instructions
- [ ] `LORE.md` - Why the swarm is haunted
- [ ] `TECHNICAL.md` - How to use, API reference
- [ ] `pyproject.toml` - Python package configuration
- [ ] `GameArtGenerator.spec` - PyInstaller configuration
- [ ] `icon.png` - Haunted 512x512 app icon
- [ ] Executables for Windows/Linux/Mac

---

## Acceptance Criteria

This track is complete when:

- [ ] CLI generates sprites with `python rotborn_generator.py generate --faction purifed --count 10`
- [ ] GUI launches with `python run_app.py`, shows dark theme, generates sprites
- [ ] Sprites are visibly dark fantasy (not wholesome humans)
- [ ] Anomalies occur at ~5% rate (unsettling, not game-breaking)
- [ ] Same seed produces identical sprites (deterministic)
- [ ] All 4 factions produce distinct visual styles
- [ ] Animations work (twitch, shamble, convulse)
- [ ] APNG export produces animated sprites
- [ ] Sprite sheets export correctly (for game integration)
- [ ] Executables build successfully (PyInstaller)
- [ ] All tests pass (20+ tests)
- [ ] Documentation is complete (lore + technical)
- [ ] User has reviewed and approved sprites

---

## Out of Scope

The following are explicitly NOT part of this track:

- Monster/boss sprites (only humanoid characters)
- Environmental tiles (buildings, terrain, props)
- Item/equipment sprites (weapons, armor, consumables)
- UI sprites for the game itself (buttons, icons, cursors)
- Music/sound effects (visual only)
- Web-based generator (desktop app only)

These will be addressed in subsequent tracks.

---

## Technical Requirements

### Inherited from Swarm-Art
- ✅ Deterministic seeding (same seed = same output)
- ✅ Multi-resolution (32x32, 64x64, 128x128, custom)
- ✅ 4-directional rendering
- ✅ Animation system (but reimagined)
- ✅ Batch generation
- ✅ PyQt6 GUI framework

### New/Modified Systems
- **Trauma-Palettes**: Replace diversity-palettes with horror themes
- **Broken-Proportions**: Replace healthy anatomy with wrong anatomy
- **Anomaly-Injection**: New system for rule-breaking sprites
- **Haunted-Animations**: Replace walk/run/jump with twitch/shamble/convulse
- **Faction-Specific Logic**: Each faction has unique generation rules

### Dependencies
```python
# Core
Python >= 3.9
Pillow >= 9.0  # Image generation
PyQt6 >= 6.4   # GUI

# Development
pytest >= 7.0  # Testing
black >= 23.0  # Code formatting
flake8 >= 6.0  # Linting

# Packaging
pyinstaller >= 5.0  # Executables
build >= 0.10       # Package building
```

---

## Success Metrics

- **Completeness:** All 6 deliverables complete
- **Quality:** 20+ passing tests, no critical bugs
- **Aesthetic:** Sprites are visibly dark fantasy (user approval)
- **Performance:** Generates 100 sprites in <10 seconds
- **Determinism:** Same seed always produces identical output
- **Usability:** GUI is usable (unsettling but not broken)
- **Distribution:** Executables build and run on target platforms
- **Showcase Value:** Can be demoed publicly, viral potential

---

## Dependencies

This track has no dependencies and is a prerequisite for:
- ORF-RPG Art Asset Generation Track
- ORF-RPG Character Implementation Track
- ORF-RPG Enemy Implementation Track

---

## Notes

- This is a **technical showcase** - it should be demoable, shareable, press-worthy
- The lore is the selling point - "sprites generated by trauma-agents"
- Keep the code clean - others may study it, learn from it
- Test on all target platforms early and often
- Document the journey - development blog, before/after comparisons
