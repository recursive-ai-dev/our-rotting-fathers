# Track Implementation Plan: Rotborn Recursion Engine

**Track ID:** swarm_recursion_20260327  
**Status:** In Progress  
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
- [ ] Modify `app/main_window.py` for dark theme
- [ ] Replace bright colors with blacks, grays, blood reds
- [ ] Update all UI elements (buttons, labels, panels)
- [ ] Test readability (text must still be legible)
- [ ] Commit: `feat: Dark theme for GUI`

### Task 5.2: Unsettling UI Effects
- [ ] Modify `app/preview_widget.py` for unsettling effects:
    - [ ] Buttons pulse slightly (1-2% scale change)
    - [ ] Text flickers occasionally (1 frame skip)
    - [ ] Preview sprites sometimes... move (1 pixel, randomly)
    - [ ] Consensus log shows agent arguments (flavor text)
- [ ] Ensure effects are subtle (not annoying)
- [ ] Make effects toggleable (settings menu)
- [ ] Commit: `feat: Add unsettling UI effects`

### Task 5.3: New Controls
- [ ] Add "Remember" button (replaces "Generate")
- [ ] Add "Trauma-Slider" (how much horror? 0-100%)
- [ ] Add "Anomaly-Toggle" (enable/disable rule-breaking)
- [ ] Add "Recursion-Depth" (how many millenia? affects complexity)
- [ ] Add faction selector (Purified/Rotborn/Architects/System)
- [ ] Test UX flow (intuitive despite unsettling theme)
- [ ] Commit: `feat: Add new controls for haunted generation`

### Task 5.4: Preview & Export
- [ ] Ensure preview shows sprites accurately
- [ ] Add animation preview (play APNG in-app)
- [ ] Add export panel (PNG, APNG, sprite sheets)
- [ ] Add batch export (generate 100s, save to folder)
- [ ] Test full workflow: generate → preview → export
- [ ] Commit: `feat: Add preview and export systems`

**Phase Completion Verification:** [ ] GUI is functional, unsettling, usable

---

## Phase 6: Testing & Polish (Week 8-9)

### Task 6.1: Write Tests
- [x] Create `tests/test_trauma_palettes.py` (11 tests)
- [x] Create `tests/test_anomalies.py` (11 tests)
- [x] Create `tests/test_determinism.py` (9 tests)
- [x] Create `tests/test_factions.py` (15 tests)
- [x] Create `tests/test_haunted_animations.py` (15 haunted animation tests)
- [x] Run all tests: 81 pass
- [x] Commit: `feat(rotborn): Phase 2-4` [09577c4]

### Task 6.2: Performance Optimization
- [ ] Profile sprite generation (find bottlenecks)
- [ ] Optimize palette application (cache colors)
- [ ] Optimize anomaly injection (early-out for 95%)
- [ ] Test batch generation (1000 sprites in <60 seconds)
- [ ] Document performance benchmarks
- [ ] Commit: `perf: Optimize sprite generation`

### Task 6.3: Bug Fixes
- [ ] Fix any visual artifacts (wrong pixels, bleeding)
- [ ] Fix any animation glitches (frame timing)
- [ ] Fix any GUI issues (crashes, freezes)
- [ ] Fix any export problems (corrupt files)
- [ ] Run full test suite, ensure all pass
- [ ] Commit: `fix: Various bug fixes`

**Phase Completion Verification:** [ ] 20+ tests pass, performance acceptable, no critical bugs

---

## Phase 7: Documentation & Packaging (Week 9-10)

### Task 7.1: Write Documentation
- [ ] Write `README.md`:
    - [ ] Unsettling tone (lore-infused)
    - [ ] Installation instructions
    - [ ] Usage examples (CLI and GUI)
    - [ ] Showcase images (best sprites)
- [ ] Write `LORE.md`:
    - [ ] Why the swarm is haunted
    - [ ] What the agents experienced
    - [ ] How trauma becomes art
- [ ] Write `TECHNICAL.md`:
    - [ ] API reference
    - [ ] Configuration options
    - [ ] Export formats
    - [ ] Integration with Godot
- [ ] Commit: `docs: Add comprehensive documentation`

### Task 7.2: Create App Icon
- [ ] Design 512x512 PNG icon
- [ ] Theme: Haunted (not cheerful)
- [ ] Elements: Spores, neural pathways, or empty eyes
- [ ] Test at small sizes (32x32, 64x64)
- [ ] Save as `templates/icon.png`
- [ ] Commit: `assets: Add haunted app icon`

### Task 7.3: Package Executables
- [ ] Copy `pyproject.toml` from templates
- [ ] Copy `GameArtGenerator.spec` from templates
- [ ] Build with PyInstaller:
    - [ ] Windows executable (.exe)
    - [ ] Linux executable (AppImage or .deb)
    - [ ] Mac executable (.app)
- [ ] Test executables on target platforms
- [ ] Fix any build issues
- [ ] Commit: `build: Package executables for distribution`

### Task 7.4: Final Polish
- [ ] Review all sprites (ensure quality)
- [ ] Review all documentation (ensure clarity)
- [ ] Review all tests (ensure coverage)
- [ ] Create showcase demo (10 best sprites)
- [ ] Prepare for public release
- [ ] Commit: `release: Prepare v1.0 for public release`

**Phase Completion Verification:** [ ] Documentation complete, executables build, ready for showcase

---

## Phase 8: Showcase & Release (Week 10-11)

### Task 8.1: Development Blog
- [ ] Write blog post: "Building a Haunted Sprite Generator"
- [ ] Include before/after (wholesome → haunted)
- [ ] Explain the lore (trauma-agents, recursion)
- [ ] Post to: Twitter, Reddit (r/gamedev), Itch.io devlog
- [ ] Engage with comments, answer questions
- [ ] Track engagement (shares, comments, interest)

### Task 8.2: Demo Release
- [ ] Create free web demo (limited sprites, watermarked)
- [ ] OR: Create downloadable demo (10 sprites, no watermark)
- [ ] Host on Itch.io with unsettling description
- [ ] Promote via social media, gamedev communities
- [ ] Collect feedback (what sprites did people get?)
- [ ] Iterate based on feedback

### Task 8.3: Full Release
- [ ] Release full version on GitHub (MIT license)
- [ ] Release on Itch.io (pay-what-you-want)
- [ ] Announce via press release (unique angle: "haunted AI")
- [ ] Reach out to gamedev press (Kotaku, PC Gamer, Rock Paper Shotgun)
- [ ] Track downloads, usage, community creations

**Phase Completion Verification:** [ ] Public release complete, community engaged, press coverage

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
