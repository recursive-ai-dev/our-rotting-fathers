# Our Rotting Father RPG - Technology Stack

## Overview
A fully offline-capable, browser-based RPG built with TypeScript and Godot Engine, targeting Progressive Web App (PWA) deployment with local IndexedDB storage.

---

## Core Technologies

### 1. Programming Language: TypeScript

**Rationale**: Type-safe JavaScript ideal for large-scale game projects with complex state management and long-term maintainability.

#### Version Requirements
- **TypeScript**: ^5.0.0
- **Target**: ES2020+
- **Module**: ESNext

#### Key Benefits
- Compile-time type checking prevents runtime errors in complex game logic
- Better IDE support with autocomplete and refactoring tools
- Easier collaboration with clear interfaces for game entities
- Gradual migration path from JavaScript if needed

#### Project Structure
```
src/
├── types/           # Game type definitions
├── entities/        # Player, NPCs, enemies
├── systems/         # Combat, sanity, exploration
├── ui/              # UI components and screens
├── data/            # Game data, items, quests
└── utils/           # Helper functions
```

---

### 2. Game Engine: Godot 4.x (Web Export)

**Rationale**: Full-featured game engine with visual editor, scene system, and GDScript (compatible with TypeScript-like patterns), exporting to WebGL for browser deployment.

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

### 3. State Management: IndexedDB + Redux Pattern

**Rationale**: Robust browser-native storage for save games combined with predictable state management for complex game systems.

#### Storage Layer: IndexedDB
- **Library**: idb-keyval or Dexie.js (recommended for TypeScript)
- **Capacity**: 50-100MB typical browser allocation
- **Use Cases**:
  - Save game data (multiple save slots)
  - Unlockable content tracking
  - Settings and preferences
  - Dialogue history and choices

#### State Layer: Redux Pattern (Manual or Lightweight Library)
- **Approach**: Custom Redux implementation or Zustand for simplicity
- **State Slices**:
  - `playerState`: Stats, inventory, equipment, sanity level
  - `worldState`: Current location, discovered areas, NPC states
  - `questState`: Active/completed quests, objectives
  - `factionState`: Reputation with each faction
  - `gameFlags`: Story progression, key decisions

#### Save System Architecture
```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Game State │────▶│  Serializer  │────▶│  IndexedDB   │
│   (Redux)   │     │  (JSON +     │     │  (Save Slots)│
│             │◀────│   Compress)  │◀────│              │
└─────────────┘     └──────────────┘     └──────────────┘
```

#### Save Data Structure
```typescript
interface SaveData {
  version: string;           // Save format version
  timestamp: number;         // Unix timestamp
  playtime: number;          // Seconds played
  player: PlayerState;
  world: WorldState;
  flags: Record<string, any>;
  metadata: {
    location: string;
    level: number;
    sanityLevel: number;
    faction: string;
  };
}
```

---

### 4. Deployment: Progressive Web App (PWA)

**Rationale**: Fully offline-capable web application with no backend dependencies, maximizing accessibility and minimizing infrastructure costs.

#### PWA Features
- **Service Worker**: Cache game assets for offline play
- **Web App Manifest**: Installable on desktop/mobile
- **IndexedDB**: Local save storage
- **Background Sync**: Optional cloud save sync (future)

#### Hosting Options
- **GitHub Pages**: Free, simple deployment
- **Netlify**: Automatic builds, CDN, forms (for feedback)
- **Vercel**: Edge deployment, analytics
- **Itch.io**: Game distribution platform (supports HTML5)

#### Performance Optimization
- **Asset Loading**: Lazy load areas, async asset streaming
- **Code Splitting**: Separate combat, exploration, UI bundles
- **Compression**: Brotli for text, WebP/AVIF for images
- **Caching Strategy**: Cache-first for assets, network-first for updates

---

## Development Tools

### Build & Bundling
- **Vite**: Fast development server, HMR, production builds
- **ESBuild**: Ultra-fast TypeScript compilation

### Testing
- **Vitest**: Unit tests for game logic, state management
- **Playwright**: E2E tests for critical paths (save/load, combat)

### Quality Assurance
- **ESLint**: Code quality, TypeScript rules
- **Prettier**: Consistent formatting
- **TypeScript Strict Mode**: Maximum type safety

### Version Control
- **Git**: Standard version control
- **Git LFS**: Large file storage for art/audio assets
- **Husky**: Pre-commit hooks for linting, tests

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
- **Mobile Apps**: Wrap PWA in Capacitor for app stores
- **Desktop Apps**: Electron/Tauri for Steam release
- **Multiplayer**: Asynchronous features (leaderboards, shared events)

---

## Dependencies Summary

```json
{
  "dependencies": {
    "godot-web": "^4.2.0",
    "dexie": "^3.2.0",
    "zustand": "^4.5.0",
    "idb-keyval": "^6.2.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0",
    "eslint": "^8.56.0",
    "prettier": "^3.1.0",
    "husky": "^8.0.0"
  }
}
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Godot Engine                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │  Scenes  │  │ Scripts  │  │  Assets  │  │ Export │ │
│  │          │  │(GDScript)│  │          │  │ WebGL  │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  TypeScript Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Types   │  │  State   │  │  Utils   │              │
│  │          │  │ (Zustand)│  │          │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Storage Layer                         │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │    IndexedDB     │  │   Service Worker │            │
│  │   (Save Games)   │  │   (PWA Cache)    │            │
│  └──────────────────┘  └──────────────────┘            │
└─────────────────────────────────────────────────────────┘
```
