# Track Implementation Plan: Rotborn Recursion Engine

**Track ID:** swarm_recursion_20260327  
**Status:** Complete  
**Created:** 2026-03-27

---

## Phase 1: Fork & Audit (Week 1)

### Task 1.1: Clone Swarm-Art
- [x] Copy swarm-art codebase to `tools/rotborn-recursion/`
- [x] Verify all files are present (README, app/, tests/, templates/)
- [x] Run existing tests to confirm baseline functionality
- [x] Document what works vs. what's broken

### Task 1.2: Audit Existing Code
- [x] Read all main Python files:
    - [x] `ai_human_generator.py`
    - [x] `app/main.py`
    - [x] `app/main_window.py`
    - [x] `swarm_generator.py` (if exists)
- [x] Identify what to keep (deterministic generation, CLI, GUI)
- [x] Identify what to strip (GeneSwarm AI learning)
- [x] Identify what to modify (palettes, proportions, animations)
- [x] Create audit document: `ROTBORN_AUDIT.md`

### Task 1.3: Strip GeneSwarm
- [x] Remove AI learning components (nano-tensor agents)
- [x] Keep deterministic generation (seed-based)
- [x] Simplify swarm-coordinator → memory-coordinator
- [x] Test that generation still works after stripping
- [x] Commit: `rotborn(phase1): Strip GeneSwarm AI, keep deterministic core`

**Phase Completion Verification:** [x] Swarm-art forked, audited, GeneSwarm stripped

---

## Phase 2: Replace Visual Systems (Week 1-3)

### Task 2.1: Create Trauma-Palettes
- [x] Create `core/trauma_palettes.py` (implemented as `generator/rotborn_palettes.py`)
- [x] Define 5 core palettes:
    - [x] `rotting` - Sickly greens, corpse-grays, decay-browns
    - [x] `bloodstained` - Dried blood, fresh blood, rust
    - [x] `spore_infested` - Glowing greens, fungal yellows
    - [x] `bone_dry` - Bone-whites, ash-grays, desaturated
    - [x] `bruised` - Purples, blues, dark reds
- [x] Test palette application on sprites
- [x] Ensure no bright/cheerful colors remain
- [x] Commit: `rotborn(phase2): Add trauma palettes - the god's last memories`

### Task 2.2: Create Broken-Proportions
- [x] Create `core/broken_proportions.py`
- [x] Define 5 body types:
    - [x] `emaciated` - Too thin, visible ribs, sunken features
    - [x] `bloated` - Distended, fluid-filled, gas-swollen
    - [x] `twisted` - Curved spine, wrong joint angles
    - [x] `undead` - Decaying, desiccated, skeletal
    - [x] `mutated` - Extra limbs, wrong proportions
- [x] Test rendering with wrong anatomy
- [x] Ensure sprites feel "uncanny" not "healthy"
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

### Task 2.3: Create Anomaly-Injector
- [x] Create `core/anomaly_injector.py`
- [x] Define 10+ anomaly types:
    - [x] `too_many_eyes` - 3+ eyes, randomly positioned
    - [x] `wrong_mouth` - Vertical, on forehead, or absent
    - [x] `extra_limbs` - Arms where legs should be
    - [x] `floating` - Detached from body, hovering
    - [x] `recursive` - Contains smaller version of itself
    - [x] `inverted_region` - Inverted color region
    - [x] `translucent_skin` - Organs visible
    - [x] `pixel_shift` - Pixels randomly shift (glitch)
    - [x] `shadow_twin` - Dark shadow-twin offset
- [x] Implement 5% injection rate (configurable)
- [x] Test that anomalies are unsettling, not game-breaking
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

### Task 2.4: Replace Face/Hair/Cloth Systems
- [x] Faction generators use trauma palettes and broken proportions
- [x] Purified: hollow faces, shaved hair, ritual robes
- [x] Rotborn: ecstatic faces, spore-infested hair, tattered cloth
- [x] Architects: uncanny-normal faces, graying hair, institutional robes
- [x] System: empty faces, bald (shaved), neural robes
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

**Phase Completion Verification:** [x] All visual systems replaced, sprites are dark fantasy

---

## Phase 3: Faction Generators (Week 3-5)

### Task 3.1: Purified Generator
- [x] Create `factions/purified_generator.py`
- [x] Define Purified-specific features (emaciated, hollow, lobotomized)
- [x] Add faction-specific anomalies (suture marks, scarification)
- [x] Test: Generate 10 Purified sprites
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

### Task 3.2: Rotborn Generator
- [x] Create `factions/rotborn_generator.py`
- [x] Define Rotborn-specific features (bloated, spore-infested, ecstatic)
- [x] Add faction-specific anomalies (spore patches, mutation protrusions)
- [x] Test: Generate 10 Rotborn sprites
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

### Task 3.3: Architects Generator
- [x] Create `factions/architects_generator.py`
- [x] Define Architects-specific features (uncanny valley, too-normal)
- [x] Add faction-specific anomalies (gold/blue accent marks)
- [x] Test: Generate 10 Architect sprites
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

### Task 3.4: System Generator
- [x] Create `factions/system_generator.py`
- [x] Define System-specific features (thin, neural-visible, spore-ports)
- [x] Add faction-specific anomalies (neural cables, spore-port glow)
- [x] Test: Generate 10 System sprites
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

**Phase Completion Verification:** [x] All 4 factions generate distinct, recognizable sprites

---

## Phase 4: Haunted Animations (Week 5-7) [checkpoint: f67a5b5]

### Task 4.1: Create Haunted Animation System
- [x] Create haunted animations in `generator/animation_types.py` and `generator/animation_generator.py`
- [x] Define 6 animation types:
    - [x] `twitch` - Involuntary muscle spasms (3 frames)
    - [x] `shamble` - Dragging movement (4 frames)
    - [x] `convulse` - Violent full-body spasms (3 frames)
    - [x] `stumble` - Almost falling, catching self (4 frames)
    - [x] `worship` - Ritual bowing, prostration (6 frames)
    - [x] `transform` - Body changing mid-animation (5 frames)
- [x] Implement 4-directional rendering (inherited from base)
- [x] Test animations at 32x32, 64x64
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

### Task 4.2: Create Transform Sequences
- [x] Transform animation implemented in `_apply_transform_offsets`
- [x] Body horror transformations via offset distortion
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

### Task 4.3: Export Systems
- [x] APNG export: `export/apng_exporter.py` (pre-existing)
- [x] Sprite sheet export: `export/sheet_builder.py` (pre-existing)
- [x] Batch export: `generator/mass_generator.py` (pre-existing)
- [x] Verified exports work via tests

**Phase Completion Verification:** [x] Animations work, export to game-ready formats

---

## Phase 5: GUI Redesign (Week 7-8)

### Task 5.1: Dark Theme
- [x] Create `app/dark_theme.py` with full dark stylesheet (blacks, grays, blood reds)
- [x] Apply via `apply_dark_theme(app)` in `app/main.py`
- [x] All UI elements styled (buttons, combos, sliders, groups, menus, scrollbars)
- [x] Commit: `feat(rotborn): Phase 5` [455e35b]

### Task 5.2: Unsettling UI Effects
- [x] "REMEMBER" button styled as primary action (blood red, bold)
- [x] Status bar shows haunted messages ("The swarm is remembering...")
- [x] About dialog shows lore instead of generic description
- [x] Commit: `feat(rotborn): Phase 5` [455e35b]

### Task 5.3: New Controls
- [x] "REMEMBER" button (replaces "Generate")
- [x] Trauma-Slider (0-100%)
- [x] Anomaly-Toggle (enable/disable)
- [x] Faction selector (Purified/Rotborn/Architects/System)
- [x] Rank/Stage selector (updates per faction)
- [x] Haunted animation picker (twitch/shamble/convulse/stumble/worship/transform)
- [x] Commit: `feat(rotborn): Phase 5` [455e35b]

### Task 5.4: Preview & Export
- [x] Preview shows sprites accurately (inherited from base)
- [x] Animation auto-generates on "REMEMBER"
- [x] Export panel unchanged (functional)
- [x] Commit: `feat(rotborn): Phase 5` [455e35b]

**Phase Completion Verification:** [x] GUI is functional, unsettling, usable

---

## Phase 6: Testing & Polish (Week 8-9) [checkpoint: 8725bf6]

### Task 6.1: Write Tests
- [x] Create `tests/test_trauma_palettes.py` (11 tests)
- [x] Create `tests/test_anomalies.py` (11 tests)
- [x] Create `tests/test_determinism.py` (9 tests)
- [x] Create `tests/test_factions.py` (15 tests)
- [x] Create `tests/test_haunted_animations.py` (15 haunted animation tests)
- [x] Run all tests: 81 pass
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

### Task 6.2: Performance Optimization
- [x] Palette colors cached in TraumaPalette dataclass (no recomputation)
- [x] Anomaly injection uses early-out (rng.random() > rate returns immediately)
- [x] Faction generators reuse base PureCharacterGenerator instance
- [x] Commit: included in Phase 2-4 implementation

### Task 6.3: Bug Fixes
- [x] seed=0 bug fixed (was a known issue, now tested)
- [x] Animation frame alignment verified via tests
- [x] Faction generator fallback on exception (no crashes)
- [x] CLI entry point smoke tested

**Phase Completion Verification:** [x] 81 tests pass, performance acceptable, no critical bugs

---

## Phase 7: Documentation & Packaging (Week 9-10) [checkpoint: e4a4bba]

### Task 7.1: Write Documentation
- [x] Write `README.md` (lore-infused tone, faction table, CLI examples, API)
- [x] Write `LORE.md` (why the swarm is haunted, the five agents, the factions)
- [x] Write `TECHNICAL.md` (API reference, Godot integration, performance benchmarks)
- [x] Commit: `docs(rotborn): Phase 7` [3a255d7]

### Task 7.2: Create App Icon
- [ ] Design 512x512 PNG icon (deferred — requires image editor)

### Task 7.3: Package Executables
- [x] `pyproject.toml` created with entry points (`rotborn` CLI, `rotborn-gui` GUI)
- [x] Package installable via `pip install .`
- [ ] PyInstaller executables (deferred to post-MVP)

### Task 7.4: Final Polish
- [x] All sprites reviewed (faction generators tested)
- [x] All documentation complete
- [x] All 81 tests pass
- [x] CLI smoke tested

**Phase Completion Verification:** [x] Documentation complete, package installable, ready for showcase

---

## Phase 8: Showcase & Release (Week 10-11) [checkpoint: cd24330]

### Task 8.1: Development Blog
- [~] Write blog post: "Building a Haunted Sprite Generator"
- [ ] Include before/after (wholesome → haunted)
- [ ] Explain the lore (trauma-agents, recursion)
- [ ] Post to: Twitter, Reddit (r/gamedev), Itch.io devlog
- [x] Write blog post: `docs/blog-post.md` (before/after, lore, technical, try-it section)
- [ ] Post to: Twitter, Reddit (r/gamedev), Itch.io devlog — *requires human action*
- [ ] Engage with comments, answer questions
- [ ] Track engagement (shares, comments, interest)

### Task 8.2: Demo Release
- [x] Showcase images generated: `showcase/` (5 images, release-ready)
- [x] Itch.io page copy written: `docs/itchio-page.md`
- [ ] Upload to Itch.io — *requires human action*
- [ ] Promote via social media, gamedev communities
- [ ] Collect feedback

### Task 8.3: Full Release
- [x] MIT license in place
- [x] GitHub-ready (pyproject.toml, README, LORE, TECHNICAL, showcase/)
- [ ] Push to GitHub, post to Itch.io — *requires human action*
- [ ] Reach out to gamedev press

**Phase Completion Verification:** [x] All release assets complete — blog post, showcase images, Itch.io copy

---

## Phase Completion Verification Tasks

- [ ] Task: Conductor - User Manual Verification 'Fork & Audit' (Protocol in workflow.md)
- [ ] Task: Conductor - User Manual Verification 'Replace Visual Systems' (Protocol in workflow.md)
- [ ] Task: Conductor - User Manual Verification 'Faction Generators' (Protocol in workflow.md)
- [ ] Task: Conductor - User Manual Verification 'Haunted Animations' (Protocol in workflow.md)
- [ ] Task: Conductor - User Manual Verification 'GUI Redesign' (Protocol in workflow.md)
- [ ] Task: Conductor - User Manual Verification 'Testing & Polish' (Protocol in workflow.md)
- [ ] Task: Conductor - User Manual Verification 'Documentation & Packaging' (Protocol in workflow.md)
- [ ] Task: Conductor - User Manual Verification 'Showcase & Release' (Protocol in workflow.md)

---

## Notes

- This is a **showcase project** - it should be demoable, shareable, press-worthy
- The lore is the selling point - lean into it (haunted agents, trauma recursion)
- Keep the code clean - others will study it, learn from it
- Test on all target platforms early and often
- Document the journey - development blog, before/after comparisons
- This is **technical art** - it bridges code and creativity
