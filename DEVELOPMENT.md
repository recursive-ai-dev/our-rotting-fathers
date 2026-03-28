# Our Rotting Father RPG - Development Setup

**2026 Build System**: Modern tooling for seamless Godot + Python development

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Godot 4.2+           # Game engine
- Python 3.8+          # Content generation tools
- Node.js 18+          # Build orchestration (optional)

# Recommended
- just                 # Command runner (https://just.systems)
- VS Code              # Editor with Godot tools extension
```

### Install Dependencies

**1. Install `just` (command runner):**
```bash
# macOS
brew install just

# Linux
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin

# Windows (winget)
winget install just

# Or via cargo
cargo install just
```

**2. Setup project:**
```bash
# Clone repository
git clone https://github.com/recursive-ai-dev/our-rotting-fathers.git
cd our-rotting-fathers

# Install all dependencies (Python venv + npm packages)
just setup

# Or manually:
cd tools/rotborn-recursion
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ../..
npm install
```

---

## 📋 Available Commands

Run `just --list` to see all available commands.

### Development

```bash
just godot          # Open Godot editor
just run            # Run game in debug mode
just dev            # Full dev workflow (clean + generate + run)
just dev-quick      # Quick run (no regeneration)
```

### Content Generation

```bash
just generate-sprites         # Generate 100 character sprites
just generate-sprites-palette PALETTE="bloodstained"  # Specific palette
just generate-animations      # Generate animation sprite sheets
just generate-all             # Generate everything
```

### Build & Export

```bash
just build-web        # Build HTML5/PWA
just build-linux      # Build Linux executable
just build-windows    # Build Windows executable
just build-macos      # Build macOS app
just build-all        # Build all platforms
```

### Testing & Quality

```bash
just test             # Run all tests
just test-python      # Run Python tests only
just test-godot       # Run Godot tests
just lint             # Lint all code
just format-python    # Format Python code
```

### npm Scripts (Alternative)

If you prefer npm over `just`:

```bash
npm run dev           # Run game
npm run build:web     # Build web
npm run generate      # Generate assets
npm run test          # Run tests
npm run godot         # Open Godot
```

---

## 🎮 Development Workflow

### Typical Day

```bash
# 1. Start development session
just dev

# 2. Make changes in Godot editor
#    - Edit scenes
#    - Write GDScript
#    - Test in real-time

# 3. Generate new sprites (if needed)
just generate-sprites-palette PALETTE="spore_infested"

# 4. Run tests before committing
just test

# 5. Commit changes
git add .
git commit -m "feat: Add new feature"
```

### Content Creation Pipeline

```bash
# Generate character sprites for all trauma palettes
just generate-all

# This creates:
# game/godot/assets/sprites/characters/
# ├── rotting/
# ├── bloodstained/
# ├── spore_infested/
# ├── bone_dry/
# └── bruised/

# game/godot/assets/metadata/
# ├── master_index.json
# ├── rotting_batch.json
# └── *_animations.json
```

---

## 🏗️ Build System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         justfile                            │
│  Central command runner - orchestrates all build tasks      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐  ┌────────────────┐  ┌─────────────────┐
│  Godot 4.2+   │  │  Python 3.8+   │  │   Node.js 18+   │
│  Game Engine  │  │  Asset Tools   │  │  Build Scripts  │
└───────────────┘  └────────────────┘  └─────────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    game/godot/                              │
│  Main game project - scenes, scripts, assets                │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                   build/                                    │
│  Exported builds: web/, linux/, windows/, macos/            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 CI/CD Pipeline

GitHub Actions automatically:

1. **On Push to master:**
   - Run Python tests
   - Lint code
   - Build web export
   - Deploy to GitHub Pages

2. **On Pull Request:**
   - Run all tests
   - Build all platforms
   - Report build status

### Manual Deployment

```bash
# Deploy web build to GitHub Pages
just deploy-web

# Or via GitHub Actions UI:
# 1. Go to Actions → Build & Deploy
# 2. Click "Run workflow"
# 3. Check "Deploy to GitHub Pages"
# 4. Click "Run workflow"
```

---

## 📁 Project Structure

```
our-rotting-father-rpg/
├── justfile                  # Build commands
├── package.json              # npm scripts
├── .github/workflows/        # CI/CD
├── game/godot/               # Godot project
│   ├── project.godot
│   ├── scenes/
│   ├── scripts/
│   └── assets/
├── tools/rotborn-recursion/  # Content generation
│   ├── ai_human_generator.py
│   ├── generator/
│   ├── export_to_godot.py    # Asset pipeline
│   └── tests/
└── build/                    # Generated builds
```

---

## 🐛 Troubleshooting

### Godot export fails
```bash
# Ensure export presets are configured
just godot
# Editor → Export → Add "Web", "Linux", "Windows", "macOS"
```

### Python import errors
```bash
# Activate virtual environment
cd tools/rotborn-recursion
source venv/bin/activate
pip install -r requirements.txt
```

### Permission denied on Linux
```bash
# Make scripts executable
chmod +x tools/rotborn-recursion/*.py
```

---

## 🎯 Next Steps

1. **First Time Setup:**
   ```bash
   just setup
   just godot  # Configure export presets
   ```

2. **Generate Test Assets:**
   ```bash
   just generate-sprites
   ```

3. **Start Development:**
   ```bash
   just dev
   ```

4. **Build for Web:**
   ```bash
   just build-web
   ```

---

**Welcome to 2026 game development! 🎮**
