# Our Rotting Father RPG - Version 1.0 Development Plan

## V1 Vision: "The Withered Hand - Act 1 Complete"

**Target Scope:** A complete, playable Act 1 that establishes the world, factions, and core mechanics. 2-3 hours of gameplay. Multiple faction paths. Meaningful choices that carry into future acts.

**Release Target:** Q4 2026 (8-10 month development cycle)

---

## Core Features (V1 Scope)

### 1. Character System ✅ (Design Complete)
- **Stats:** Strength, Agility, Intellect, Sanity, Health, Mana
- **Sanity Meter:** Dynamic psychosis level (0-100) affecting dialogue, abilities, NPC reactions
- **Character Creation:**
  - 5 origin stories (Rotborn defector, Purified initiate, Council citizen, Prophet disciple, Orphan)
  - Basic appearance customization (gender-neutral, body type, scars/rot-marks)
  - Starting stat allocation (20 points, min 3, max 8 per stat)
- **Progression:**
  - XP-based leveling (level cap: 10 for V1)
  - Stat allocation on level-up
  - Equipment slots: Weapon, Armor, Accessory (2), Relic

### 2. Combat System 🔄 (In Design)
- **Turn-Based Combat:**
  - Player turn → Enemy turn → Resolution phase
  - Action points system (3 AP per turn)
  - Abilities cost AP + Mana
- **Sanity Integration:**
  - High sanity (>75): Unlock psychosis abilities, special dialogue
  - Low sanity (<25): Hallucinations, stat penalties, NPC fear reactions
- **Enemy Types (V1):**
  - Rot-Spawn (basic enemies, 3 variants)
  - Faction Warriors (Purified, Rotborn, 2 variants each)
  - Bosses: 3 (Tutorial boss, Mid-act boss, Act climax boss)
- **Combat Abilities:**
  - 8 base abilities (available to all)
  - 12 faction-specific abilities (unlockable via reputation)
  - 6 psychosis abilities (high sanity only)

### 3. Dialogue System 🔄 (In Design)
- **Branching Conversations:**
  - 3-5 dialogue options per encounter
  - Faction-gated options (require reputation thresholds)
  - Sanity-gated options (high/low sanity only)
- **Choice Tracking:**
  - Major choices flagged (affect faction reputation, story path)
  - Minor choices tracked (NPC relationships, rewards)
  - Journal log of decisions made
- **Faction Reputation:**
  - 4 factions (Purified, Rotborn Embrace, Delusion Architects, God's Nervous System)
  - Scale: -100 to +100 per faction
  - Reputation unlocks: quests, abilities, vendors, areas

### 4. World Exploration 🔄 (In Design)
- **Act 1 Map: The Withered Hand**
  - Starting settlement: "Last Rest" (Council-controlled)
  - 5 explorable sub-areas:
    1. The Fingerbone Bridge (tutorial area)
    2. The Marrow Markets (hub, all factions present)
    3. The Nail Spire (Purified outpost)
    4. The Rot Gardens (Rotborn territory)
    5. The Whisper Caves (Prophet shrine + dungeon)
  - Fast travel points: 5 (unlocked progressively)
- **Environmental Storytelling:**
  - Visible god anatomy (bone, flesh, organs as landscape)
  - Decay effects (spore clouds, rot zones, mutation pockets)
  - Faction architecture (distinct styles per faction)
- **Secrets:**
  - 10 hidden areas (lore documents, unique items)
  - 5 optional mini-bosses
  - 3 Easter eggs (references, jokes, meta-commentary)

### 5. Quest System 🔄 (In Design)
- **Main Quest Line:** "Act 1: The Withered Hand"
  - 10 major story beats
  - 2-3 hours total playtime
  - Multiple resolution paths (faction-dependent)
- **Faction Quests:**
  - 4 factions × 3 quests each = 12 faction quests
  - Reputation-gated (require +25 or higher)
  - Reward faction abilities, items, reputation
- **Side Quests:**
  - 8 side quests (unlocked through exploration)
  - Mix of combat, dialogue, puzzle-solving
  - Rewards: XP, items, sanity restoration
- **Quest Design:**
  - All quests have multiple solutions
  - Sanity affects available solutions
  - Faction reputation locks/unlocks quests

### 6. Save/Load System ✅ (Design Complete)
- **IndexedDB Storage:**
  - Multiple save slots (5 slots)
  - Auto-save (after major choices, combat, area transitions)
  - Manual save (anytime outside combat)
- **Save Data:**
  - Character state (stats, sanity, equipment)
  - World state (completed quests, unlocked areas)
  - Faction reputation
  - Choice flags (major/minor decisions)
- **PWA Integration:**
  - Offline-capable (service worker caching)
  - Installable on desktop/mobile
  - Local-only (no cloud saves in V1)

---

## Content Deliverables (V1)

### Lore Documents
| Document | Status | Owner | Due Date |
|----------|--------|-------|----------|
| Product Definition | ✅ Complete | User | Done |
| Product Guidelines | ✅ Complete | User | Done |
| Tech Stack | ✅ Complete | User | Done |
| Faction: The Purified | ✅ Complete | AI | Done |
| Faction: Rotborn Embrace | ⏳ Pending | AI | TBD |
| Faction: Delusion Architects | ⏳ Pending | AI | TBD |
| Faction: God's Nervous System | ⏳ Pending | AI | TBD |
| Act 1 Story Beats | ⏳ Pending | AI | TBD |
| Character Lore Bible | ⏳ Pending | AI | TBD |
| World Geography (Act 1) | ⏳ Pending | AI | TBD |
| Magic System | ⏳ Pending | AI | TBD |
| Sanity Mechanics | ⏳ Pending | AI | TBD |

### Game Design Documents
| Document | Status | Owner | Due Date |
|----------|--------|-------|----------|
| Combat System Design | ⏳ Pending | AI | TBD |
| Dialogue System Design | ⏳ Pending | AI | TBD |
| Character Progression | ⏳ Pending | AI | TBD |
| Quest Design Template | ⏳ Pending | AI | TBD |
| Enemy Design Bible | ⏳ Pending | AI | TBD |
| Item Database | ⏳ Pending | AI | TBD |

### Technical Implementation
| System | Status | Owner | Due Date |
|--------|--------|-------|----------|
| Godot Project Setup | ⏳ Pending | AI | TBD |
| TypeScript Integration | ⏳ Pending | AI | TBD |
| Character Controller | ⏳ Pending | AI | TBD |
| Combat Engine | ⏳ Pending | AI | TBD |
| Dialogue System | ⏳ Pending | AI | TBD |
| Save/Load System | ⏳ Pending | AI | TBD |
| UI Framework | ⏳ Pending | AI | TBD |
| Art Pipeline | ⏳ Pending | AI | TBD |

---

## Development Phases (V1)

### Phase 1: Foundation (Months 1-2)
**Goal:** Establish core systems and complete all design documents

**Lore Tasks:**
- [ ] Complete remaining 3 faction documents (Rotborn, Architects, Prophets)
- [ ] Write Act 1 story beats (10 beats, detailed)
- [ ] Create character lore bible (16+ NPCs)
- [ ] Document world geography (5 sub-areas)
- [ ] Design magic system (4 schools, 20+ spells)
- [ ] Finalize sanity mechanics (integration with all systems)

**Technical Tasks:**
- [ ] Initialize Godot 4.x project with TypeScript
- [ ] Set up project structure (folders, naming conventions)
- [ ] Implement character stat system
- [ ] Implement sanity meter (UI + logic)
- [ ] Create save/load system (IndexedDB)
- [ ] Build dialogue system foundation

**Deliverables:**
- All lore documents complete
- All GDDs complete
- Playable prototype (character creation + stat testing)

### Phase 2: Core Systems (Months 3-4)
**Goal:** Implement combat, dialogue, and quest systems

**Combat Tasks:**
- [ ] Turn-based combat engine (AP system, initiative)
- [ ] 8 base abilities (implementation + VFX)
- [ ] Enemy AI (3 rot-spawn variants)
- [ ] Tutorial boss fight
- [ ] Sanity integration (psychosis abilities)

**Dialogue Tasks:**
- [ ] Branching conversation UI
- [ ] Choice tracking system
- [ ] Faction reputation system
- [ ] 3 faction questlines (partial implementation)

**Quest Tasks:**
- [ ] Quest system framework (accept, track, complete)
- [ ] 5 side quests (full implementation)
- [ ] Main quest beats 1-5 (implementation)

**Deliverables:**
- Playable combat demo
- Dialogue system functional
- 50% of Act 1 content playable

### Phase 3: Content (Months 5-7)
**Goal:** Implement all Act 1 content (quests, areas, NPCs)

**World Tasks:**
- [ ] Create 5 sub-areas (level design, encounters, secrets)
- [ ] Implement fast travel system
- [ ] Environmental storytelling (props, lore objects)
- [ ] Lighting, atmosphere, VFX

**NPC Tasks:**
- [ ] 16 NPCs (models, dialogue, AI)
- [ ] 4 faction vendors (inventory, trading)
- [ ] 3 boss NPCs (unique mechanics)

**Quest Tasks:**
- [ ] Main quest beats 6-10 (implementation)
- [ ] 12 faction quests (full implementation)
- [ ] 3 side quests (remaining)
- [ ] Multiple endings (3 variations)

**Deliverables:**
- Complete Act 1 playthrough (2-3 hours)
- All factions functional
- All quests completable

### Phase 4: Polish (Months 8-9)
**Goal:** Refine, optimize, bug-fix

**Polish Tasks:**
- [ ] Balance pass (stats, abilities, difficulty)
- [ ] UI/UX refinement (accessibility, clarity)
- [ ] Performance optimization (load times, frame rate)
- [ ] Bug fixing (QA testing, user feedback)
- [ ] Audio implementation (music, SFX, voice acting if budget allows)

**Content Tasks:**
- [ ] Additional dialogue (player feedback incorporation)
- [ ] Lore document integration (in-game codex)
- [ ] Achievement system (10-15 achievements)
- [ ] New Game+ setup (carries over sanity, unlocks)

**Deliverables:**
- Release candidate
- QA sign-off
- User playtest feedback incorporated

### Phase 5: Release (Month 10)
**Goal:** Launch V1.0

**Release Tasks:**
- [ ] PWA build optimization
- [ ] Browser compatibility testing (Chrome, Firefox, Safari, Edge)
- [ ] Marketing materials (trailer, screenshots, press kit)
- [ ] Itch.io page setup (or other distribution platform)
- [ ] Community management (Discord, social media)

**Deliverables:**
- **V1.0 Released** 🎉
- Post-launch support plan

---

## Risk Assessment

### High Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep (Act 1 too ambitious) | High | High | Strict feature freeze after design. Cut content, not quality. |
| Sanity system too complex | Medium | High | Simplify to 3 tiers (low/med/high) for V1. Expand in V2. |
| Art pipeline bottleneck | High | Medium | Use placeholder art. Focus on functionality. Commission art late Phase 2. |
| Turn-based combat feels slow | Medium | Medium | Aggressive playtesting. Speed options (2x, 3x). Skip animations. |

### Medium Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Faction reputation unbalanced | Medium | Medium | Extensive playtesting. Easy to tweak via config files. |
| Dialogue writing inconsistent | Medium | Low | Establish style guide early. Review all dialogue against guidelines. |
| Save system bugs | Low | High | Over-engineer save system. Extensive testing. Multiple backup slots. |

### Low Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Godot TypeScript integration issues | Low | Medium | Use established plugins. Follow community best practices. |
| Browser performance poor | Low | High | Aggressive optimization. Asset compression. Lazy loading. |

---

## Success Metrics (V1)

### Quantitative
- **Playtime:** 2-3 hours for main quest (telemetry if possible, user surveys otherwise)
- **Completion Rate:** >60% of players finish Act 1
- **Replay Rate:** >30% start second playthrough (different faction path)
- **Performance:** <5s initial load, 60 FPS stable, <500MB RAM
- **Bug Rate:** <5 critical bugs, <20 minor bugs at launch

### Qualitative
- **User Reviews:** >4/5 average rating on Itch.io
- **Community Engagement:** Active Discord, fan art, theory-crafting
- **Press Coverage:** 5+ indie game sites review V1
- **Lore Engagement:** Users discussing factions, debating choices, creating wikis

---

## Post-V1 Roadmap (Future Acts)

### V2: "The Festering Heart" (Act 2)
- New region: The Festering Heart (god's torso)
- Faction wars escalate (open conflict between all 4 factions)
- Magic system expansion (ritual casting, spell crafting)
- Level cap increase (10 → 20)
- Cloud saves (Supabase integration)
- **Target:** Q2 2027

### V3: "The Bone Spires" (Act 3)
- New region: The Bone Spires (Purified homeland)
- Faction endgames begin (player choice determines winners)
- Multiplayer (asynchronous: shared events, leaderboards)
- Modding support (JSON-based quest/item definitions)
- **Target:** Q4 2027

### V4: "The Dreaming Mind" (Act 4 + Finale)
- Final region: The Dreaming Mind (god's head)
- Multiple endings (4 faction endings × 3 sanity endings = 12 variations)
- Secret "true ending" (requires specific choices across all acts)
- Localization (Spanish, French, German, Japanese)
- Desktop release (Steam, via Electron/Tauri)
- **Target:** Q2 2028

---

## Immediate Next Steps (This Week)

1. **Complete Remaining Factions:**
   - [ ] Rotborn Embrace (embrace mutation, worship decay)
   - [ ] Delusion Architects (curate collective hallucinations)
   - [ ] God's Nervous System (spore-infected prophets, god's neural network)

2. **Design Act 1 Story Beats:**
   - [ ] 10 major beats (outline → detailed script)
   - [ ] Key choices and consequences
   - [ ] Boss encounter designs

3. **Technical Setup:**
   - [ ] Initialize Godot project
   - [ ] Set up TypeScript integration
   - [ ] Create folder structure
   - [ ] Version control (Git LFS for assets)

4. **Art Direction:**
   - [ ] Commission concept art (1-2 pieces for marketing)
   - [ ] Establish art style guide (pixel art specs, color palettes)
   - [ ] Create placeholder art pipeline

---

## Notes

- **This is a design-first project.** All lore, all mechanics, all quests documented before implementation.
- **V1 is MVP.** Act 1 only. No cloud saves, no multiplayer, no modding. Those are V2+ features.
- **Quality over speed.** Better to delay than ship broken. But also: better to ship than to perfect.
- **Community matters.** Engage early, listen to feedback, be transparent about development.
- **The lore is the product.** This game lives or dies on the strength of its world-building. Never compromise on the horror.
