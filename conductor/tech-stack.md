# Our Rotting Father RPG - Technology Stack

## Overview
A fully offline-capable, browser-based RPG built with **Godot 4.x** and **GDScript**, targeting Progressive Web App (PWA) deployment with local save files.

---

## Core Technologies

### 1. Game Engine: Godot 4.x

**Rationale**: Full-featured open-source game engine with visual editor, scene system, and GDScript. Provides 2D pixel-art rendering, animation tools, and WebGL export for browser deployment.

#### Version Requirements
- **Godot**: 4.2+
- **Export Template**: WebGL
- **Rendering**: Forward Plus (desktop), Mobile (web)

#### Key Features Used
- **Scene System**: Modular game areas, characters, UI screens
- **2D Engine**: Pixel-perfect rendering for dark pixel art
- **Animation**: Sprite animation, particle effects, camera shake
- **Audio**: Adaptive music system, positional SFX
- **State Machines**: Combat turns, dialogue trees, AI behavior
- **Autoload Singletons**: Global state management (GameState, AudioManager, etc.)

#### Project Structure
```
game/godot/
├── project.godot        # Engine configuration
├── scenes/              # Game scenes (.tscn)
│   ├── game/            # Main game, exploration
│   ├── combat/          # Turn-based combat arena
│   ├── dialogue/        # Conversation system
│   ├── ui/              # HUD, menus, screens
│   └── cutscenes/       # Story cinematics
├── scripts/             # GDScript files
│   ├── autoload/        # Global singletons
│   ├── entities/        # Player, NPCs, enemies
│   ├── systems/         # Combat, sanity, inventory
│   └── utils/           # Helper functions
├── assets/              # Game assets
│   ├── sprites/         # Characters, enemies, environments
│   ├── audio/           # Music, SFX, voice
│   └── fonts/           # Custom typefaces
├── resources/           # Data resources (.tres, .json)
│   ├── items/           # Item definitions
│   ├── quests/          # Quest data
│   └── dialogue/        # Branching dialogue trees
└── data/                # Runtime data
    └── saves/           # Save files (user://)
```

---

### 2. Programming Language: GDScript

**Rationale**: Godot's native scripting language with Python-like syntax, tight engine integration, and optimized performance for game logic.

#### Version Requirements
- **GDScript**: Godot 4.x native

#### Key Benefits
- Native engine API access with no binding overhead
- Type-safe with optional type annotations
- Hot-reload during development
- Integrated with Godot editor (debugging, profiling)

#### Code Structure
```
scripts/
├── autoload/            # Global singletons (always loaded)
│   ├── game_state.gd    # Player stats, inventory, world flags
│   ├── audio_manager.gd # Music, SFX, voice playback
│   ├── save_system.gd   # Save/load operations
│   ├── faction_manager.gd # Faction reputations, quests
│   └── sanity_manager.gd # Psychosis mechanics, hallucinations
├── entities/
│   ├── player.gd        # Player controller
│   ├── npc.gd           # NPC behavior
│   └── enemy.gd         # Enemy AI, combat
├── systems/
│   ├── combat_system.gd # Turn-based combat logic
│   ├── inventory.gd     # Item management
│   └── dialogue_system.gd # Branching conversations
└── utils/
    ├── constants.gd     # Game constants
    └── helpers.gd       # Utility functions
```

#### Version Requirements
- **Godot**: 4.2+
- **Export Template**: WebGL
- **Rendering**: OpenGL ES 3.0 / WebGPU (future)

#### Key Features Used
- **Scene System**: Modular game areas, characters, UI screens
- **2D Engine**: Pixel-perfect rendering for dark pixel art
- **Animation**: Sprite animation, particle effects, camera shake
- **Audio**: Adaptive music system, positional SFX
- **State Machines**: Combat turns, dialogue trees, AI behavior

#### Export Configuration
- **Target Resolution**: 1920x1080 (scaled for smaller screens)
- **Compression**: Brotli/Gzip for web optimization
- **Thread Support**: Enable for better performance (optional)
- **PWA**: Service worker for offline capability

#### Project Structure (Godot)
```
project/
├── scenes/
│   ├── game/        # Main game scene
│   ├── combat/      # Combat encounters
│   ├── dialogue/    # Conversation system
│   └── ui/          # UI screens and HUD
├── scripts/
│   ├── autoload/    # Global singletons (game state, audio)
│   ├── entities/    # Player, NPCs, enemies
│   └── systems/     # Combat, sanity, inventory
├── assets/
│   ├── sprites/     # Character, environment art
│   ├── audio/       # Music, SFX, voice
│   └── fonts/       # Custom typefaces
└── resources/
    ├── items/       # Item definitions (JSON/Resources)
    ├── quests/      # Quest data
    └── dialogue/    # Branching dialogue trees
```

---

### 3. Save System: JSON + Compression

**Rationale**: Godot's built-in file system with JSON serialization and base64 compression for save games.

#### Storage Location
- **Desktop**: `user://saves/` (OS-specific app data directory)
- **Web**: Browser persistent storage (IndexedDB backend)
- **Capacity**: 50-100MB typical browser allocation

#### Save System Features
- Multiple save slots (3 manual + 1 auto-save)
- Metadata for quick preview (location, level, playtime)
- Compression via base64 encoding
- Export/import for sharing saves

#### Save System Architecture
```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  GameState  │────▶│  Serializer  │────▶│  user://     │
│  (Autoload) │     │  (JSON +     │     │  saves/      │
│             │◀────│   base64)    │◀────│  slot_1.save │
└─────────────┘     └──────────────┘     └──────────────┘
```

#### Save Data Structure (GDScript)
```gdscript
var save_data = {
    "save_version": "1.0",
    "timestamp": Time.get_datetime_dict_from_system(),
    "playtime": 3600.5,  # seconds
    "metadata": {
        "location": "withered_hand_start",
        "level": 5,
        "sanity": 0.65,
        "faction": "council"
    },
    "game": {
        "player": { ... },  # GameState.to_dict()
        "world": { ... },
        "quests": { ... },
        "inventory": [ ... ],
        "factions": { ... }
    }
}
```

---

### 4. Deployment: Progressive Web App (PWA)

**Rationale**: Fully offline-capable web application with no backend dependencies, maximizing accessibility and minimizing infrastructure costs.

#### PWA Features
- **Service Worker**: Cache game assets for offline play (Godot web export)
- **Web App Manifest**: Installable on desktop/mobile
- **Persistent Storage**: Browser IndexedDB for save files
- **Background Sync**: Optional cloud save sync (future)

#### Hosting Options
- **GitHub Pages**: Free, simple deployment
- **Netlify**: Automatic builds, CDN, forms (for feedback)
- **Vercel**: Edge deployment, analytics
- **Itch.io**: Game distribution platform (supports HTML5)

#### Performance Optimization
- **Asset Loading**: Lazy load areas, async asset streaming
- **Compression**: Brotli/Gzip for web export
- **Caching Strategy**: Cache-first for assets

---

## Development Tools

### Godot Editor
- **Version**: 4.2+
- **Extensions**: GDScript language server, debugger

### Testing
- **Godot Tests**: Built-in testing framework
- **GUT (Godot Unit Test)**: Comprehensive test suite

### Quality Assurance
- **GDScript Linter**: Custom linting rules
- **Godot Editor**: Built-in warnings, static analysis

### Version Control
- **Git**: Standard version control
- **Git LFS**: Large file storage for art/audio assets
- **.godotignore**: Exclude engine cache files

---

## Technical Requirements

### Browser Support
- **Chrome**: 90+
- **Firefox**: 90+
- **Safari**: 15+
- **Edge**: 90+

### Performance Targets
- **Load Time**: <5s initial, <2s area transitions
- **Frame Rate**: 60 FPS stable
- **Memory**: <500MB RAM
- **Storage**: <200MB total (assets + saves)

### Accessibility
- **Keyboard Controls**: Full game playable without mouse
- **Touch Support**: Optional for tablets
- **Screen Reader**: Basic menu navigation (future)
- **Colorblind Modes**: Alternative visual indicators

---

## Future Considerations

### Phase 2 (Post-MVP)
- **Cloud Saves**: Supabase integration for cross-device sync
- **Mod Support**: JSON-based quest/item definitions
- **Analytics**: Self-hosted analytics for playtesting data
- **Localization**: i18n framework for multiple languages

### Phase 3 (Stretch Goals)
- **Desktop Apps**: Godot native export for Steam release
- **Mobile Apps**: Godot mobile export (iOS/Android)
- **Multiplayer**: Asynchronous features (leaderboards, shared events)

---

## Dependencies Summary

Godot 4.x is self-contained with no external npm/Python dependencies for core game logic.

### Engine Dependencies
- **Godot Engine**: 4.2+ (included in project)
- **GDScript**: Built-in language

### Optional Tools
- **GUT (Godot Unit Test)**: For automated testing
- **gdformat**: Code formatting (via godot-format)

### Content Generation Tools (separate)
- **Python 3.8+**: For Rotborn Recursion sprite generator
- **Pillow**: Image processing
- **PyQt6**: GUI for sprite generator

See `tools/rotborn-recursion/requirements.txt` for Python dependencies.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Godot 4.x Engine                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Scenes     │  │   Scripts    │  │   Assets     │      │
│  │   (.tscn)    │  │   (GDScript) │  │  (sprites,   │      │
│  │              │  │              │  │   audio)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Autoload Singletons                     │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │  │
│  │  │ GameState│ │AudioMgr  │ │SaveSystem│ │Faction │ │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │  │
│  │  ┌──────────┐                                       │  │
│  │  │SanityMgr │                                       │  │
│  │  └──────────┘                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              WebGL Export (PWA)                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Browser Storage Layer                     │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  user://saves/   │  │  Service Worker  │                │
│  │  (JSON + base64) │  │  (Asset Cache)   │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
┌─────────────────────────────────────────────────────────────┐
│              Content Generation Tools                       │
│  ┌──────────────────┐                                       │
│  │  Rotborn         │  Python-based sprite generator        │
│  │  Recursion       │  → Exports to game/assets/sprites/    │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```
