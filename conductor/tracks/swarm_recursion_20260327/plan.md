# Track Implementation Plan: Rotborn Recursion Engine

**Track ID:** swarm_recursion_20260327  
**Status:** New  
**Created:** 2026-03-27

---

## Phase 1: Fork & Audit (Week 1)

### Task 1.1: Clone Swarm-Art
- [ ] Copy swarm-art codebase to `tools/rotborn-recursion/`
- [ ] Verify all files are present (README, app/, tests/, templates/)
- [ ] Run existing tests to confirm baseline functionality
- [ ] Document what works vs. what's broken

### Task 1.2: Audit Existing Code
- [ ] Read all main Python files:
    - [ ] `ai_human_generator.py`
    - [ ] `app/main.py`
    - [ ] `app/main_window.py`
    - [ ] `swarm_generator.py` (if exists)
- [ ] Identify what to keep (deterministic generation, CLI, GUI)
- [ ] Identify what to strip (GeneSwarm AI learning)
- [ ] Identify what to modify (palettes, proportions, animations)
- [ ] Create audit document: `docs/swarm-audit.md`

### Task 1.3: Strip GeneSwarm
- [ ] Remove AI learning components (nano-tensor agents)
- [ ] Keep deterministic generation (seed-based)
- [ ] Simplify swarm-coordinator → memory-coordinator
- [ ] Test that generation still works after stripping
- [ ] Commit: `chore: Strip GeneSwarm AI, keep deterministic core`

**Phase Completion Verification:** [ ] Swarm-art forked, audited, GeneSwarm stripped

---

## Phase 2: Replace Visual Systems (Week 1-3)

### Task 2.1: Create Trauma-Palettes
- [ ] Create `core/trauma_palettes.py`
- [ ] Define 5 core palettes:
    - [ ] `rotting` - Sickly greens, corpse-grays, decay-browns
    - [ ] `bloodstained` - Dried blood, fresh blood, rust
    - [ ] `spore_infested` - Glowing greens, fungal yellows
    - [ ] `bone_dry` - Bone-whites, ash-grays, desaturated
    - [ ] `bruised` - Purples, blues, dark reds
- [ ] Test palette application on sprites
- [ ] Ensure no bright/cheerful colors remain
- [ ] Commit: `feat: Add trauma-palettes for dark fantasy`

### Task 2.2: Create Broken-Proportions
- [ ] Create `core/broken_proportions.py`
- [ ] Define 5 body types:
    - [ ] `emaciated` - Too thin, visible ribs, sunken features
    - [ ] `bloated` - Distended, fluid-filled, gas-swollen
    - [ ] `twisted` - Curved spine, wrong joint angles
    - [ ] `undead` - Decaying, desiccated, skeletal
    - [ ] `mutated` - Extra limbs, wrong proportions
- [ ] Test rendering with wrong anatomy
- [ ] Ensure sprites feel "uncanny" not "healthy"
- [ ] Commit: `feat: Add broken-proportions for wrong anatomy`

### Task 2.3: Create Anomaly-Injector
- [ ] Create `core/anomaly_injector.py`
- [ ] Define 10+ anomaly types:
    - [ ] `too_many_eyes` - 3+ eyes, randomly positioned
    - [ ] `wrong_mouth` - Vertical, on forehead, or absent
    - [ ] `extra_limbs` - Arms where legs should be
    - [ ] `floating` - Detached from body, hovering
    - [ ] `recursive` - Contains smaller version of itself
    - [ ] `impossible` - Non-euclidean geometry
    - [ ] `translucent_skin` - Organs visible
    - [ ] `merged_faces` - Two faces on one head
    - [ ] `inverted_colors` - Negative image effect
    - [ ] `glitching` - Pixels randomly shift (animated only)
- [ ] Implement 5% injection rate (configurable)
- [ ] Test that anomalies are unsettling, not game-breaking
- [ ] Commit: `feat: Add anomaly-injection for rule-breaking sprites`

### Task 2.4: Replace Face/Hair/Cloth Systems
- [ ] Modify `face_generator.py`:
    - [ ] Add haunted expressions (hollow, ecstatic, terrified)
    - [ ] Add dead faces (eyes closed, mouth open)
    - [ ] Add wrong faces (too many eyes, no mouth)
- [ ] Modify `hair_generator.py`:
    - [ ] Add patchy hair (falling out, bald spots)
    - [ ] Add matted hair (blood, filth, rot)
    - [ ] Add infested hair (spores, worms, fungi)
    - [ ] Add absent hair (shaved, burned off)
- [ ] Modify `cloth_generator.py`:
    - [ ] Add tattered clothing (rips, holes, fraying)
    - [ ] Add bloodstained clothing
    - [ ] Add ritual vestments (cult robes)
    - [ ] Add makeshift gear (bandages, scavenged armor)
    - [ ] Add burial shrouds
- [ ] Commit: `feat: Replace face/hair/cloth with horror variants`

**Phase Completion Verification:** [ ] All visual systems replaced, sprites are dark fantasy

---

## Phase 3: Faction Generators (Week 3-5)

### Task 3.1: Purified Generator
- [ ] Create `factions/purified_generator.py`
- [ ] Define Purified-specific features:
    - [ ] Bodies: Emaciated, surgical scars, lobotomy marks
    - [ ] Faces: Hollow, empty, sewn mouths
    - [ ] Hair: Shaved, scarification patterns
    - [ ] Clothes: White robes (ash-stained), bone-steel armor
    - [ ] Colors: White, pale blue, silver, ash-gray
- [ ] Add faction-specific anomalies:
    - [ ] Eyes sewn shut (but still visible)
    - [ ] Missing organs (chest cavity empty)
    - [ ] Bone外露 (flesh peeled back)
- [ ] Test: Generate 100 Purified sprites
- [ ] Commit: `feat: Add Purified faction generator`

### Task 3.2: Rotborn Generator
- [ ] Create `factions/rotborn_generator.py`
- [ ] Define Rotborn-specific features:
    - [ ] Bodies: Bloated, pregnant, mutated
    - [ ] Faces: Ecstatic, too many teeth, spore-breath
    - [ ] Hair: Spore-infested, glowing patches
    - [ ] Clothes: Tattered, openings for mutations
    - [ ] Colors: Flesh-pink, spore-green, blood-red
- [ ] Add faction-specific anomalies:
    - [ ] Extra limbs emerging mid-animation
    - [ ] Visible fetus (moving inside belly)
    - [ ] Multiple mouths (all speaking)
- [ ] Test: Generate 100 Rotborn sprites
- [ ] Commit: `feat: Add Rotborn faction generator`

### Task 3.3: Architects Generator
- [ ] Create `factions/architects_generator.py`
- [ ] Define Architects-specific features:
    - [ ] Bodies: Normal... too normal (uncanny valley)
    - [ ] Faces: Tired, knowing, slightly wrong
    - [ ] Hair: Graying, patchy (from stress)
    - [ ] Clothes: Simple robes, consent contracts visible
    - [ ] Colors: Agreement-gray, memory-blue, fiction-gold
- [ ] Add faction-specific anomalies:
    - [ ] Face flickers (different person underneath)
    - [ ] Text appears on clothing (contracts, lies)
    - [ ] Body slightly out of alignment with itself
- [ ] Test: Generate 100 Architect sprites
- [ ] Commit: `feat: Add Architects faction generator`

### Task 3.4: System Generator
- [ ] Create `factions/system_generator.py`
- [ ] Define System-specific features:
    - [ ] Bodies: Thin, neural pathways visible
    - [ ] Faces: Eyes rolled back, spore-ports
    - [ ] Hair: Absent (shaved for implantation)
    - [ ] Clothes: Gray robes, neural cables attached
    - [ ] Colors: Neural-blue, spore-green, pain-red
- [ ] Add faction-specific anomalies:
    - [ ] Electricity arcs off body
    - [ ] Spores visible in lungs (glowing)
    - [ ] Neural cables move independently
- [ ] Test: Generate 100 System sprites
- [ ] Commit: `feat: Add System faction generator`

**Phase Completion Verification:** [ ] All 4 factions generate distinct, recognizable sprites

---

## Phase 4: Haunted Animations (Week 5-7)

### Task 4.1: Create Haunted Animation System
- [ ] Create `animations/haunted_animations.py`
- [ ] Define 6 animation types:
    - [ ] `twitch` - Involuntary muscle spasms (2-3 frames)
    - [ ] `shamble` - Dragging movement (4 frames)
    - [ ] `convulse` - Violent full-body spasms (3 frames)
    - [ ] `stumble` - Almost falling, catching self (4 frames)
    - [ ] `worship` - Ritual bowing, prostration (6 frames)
    - [ ] `transform` - Body changing mid-animation (5 frames)
- [ ] Implement 4-directional rendering (front/back/left/right)
- [ ] Test animations at 32x32, 64x64, 128x128
- [ ] Commit: `feat: Add haunted animation system`

### Task 4.2: Create Transform Sequences
- [ ] Create `animations/transform_sequences.py`
- [ ] Define body horror transformations:
    - [ ] Limb growth (extra arms emerge)
    - [ ] Face shift (features rearrange)
    - [ ] Bloating (body distends)
    - [ ] Decay (flesh rots mid-animation)
    - [ ] Fusion (two bodies merge)
- [ ] Implement as APNG (animated PNG)
- [ ] Test that transformations are smooth but unsettling
- [ ] Commit: `feat: Add transform sequences for body horror`

### Task 4.3: Export Systems
- [ ] Implement APNG export (animated sprites)
- [ ] Implement sprite sheet export (for game integration)
- [ ] Add batch export (generate 1000s, export as sheets)
- [ ] Test export at all resolutions
- [ ] Verify exports work in Godot (import, animate)
- [ ] Commit: `feat: Add APNG and sprite sheet export`

**Phase Completion Verification:** [ ] Animations work, export to game-ready formats

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
- [ ] Create `tests/test_trauma_palettes.py`:
    - [ ] Test all 5 palettes generate correct colors
    - [ ] Test no bright/cheerful colors appear
- [ ] Create `tests/test_anomalies.py`:
    - [ ] Test anomalies inject at ~5% rate
    - [ ] Test all 10+ anomaly types work
- [ ] Create `tests/test_determinism.py`:
    - [ ] Test same seed = same sprite (100 iterations)
    - [ ] Test different seeds = different sprites
- [ ] Create `tests/test_factions.py`:
    - [ ] Test each faction produces distinct style
    - [ ] Test faction-specific anomalies work
- [ ] Create `tests/test_animations.py`:
    - [ ] Test all 6 animation types render
    - [ ] Test 4-directional rendering works
- [ ] Run all tests, fix failures
- [ ] Commit: `test: Add comprehensive test suite`

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
