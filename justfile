# Our Rotting Father RPG - Build System
# Requires: just (https://just.systems), Godot 4.2+, Python 3.8+
# Install just: brew install just / winget install just

# Default target - shows all available commands
default:
  @just --list

# =============================================================================
# SETUP
# =============================================================================

# Install all dependencies (Python + npm)
setup:
  echo "🔧 Setting up project dependencies..."
  cd tools/rotborn-recursion && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt && pip install pytest black flake8
  npm install
  echo "✅ Setup complete!"

# =============================================================================
# GODOT DEVELOPMENT
# =============================================================================

# Open project in Godot editor
godot:
  echo "🎮 Opening Godot editor..."
  godot --path game/godot/project.godot

# Run game in debug mode (windowed)
run:
  echo "🎮 Running game in debug mode..."
  godot --path game/godot/project.godot --debug

# Run game in fullscreen
run-fullscreen:
  godot --path game/godot/project.godot --fullscreen

# Run with debug collision visible
run-collision:
  godot --path game/godot/project.godot --debug-collisions

# =============================================================================
# BUILD & EXPORT
# =============================================================================

# Build web export (HTML5/PWA)
build-web:
  echo "🌐 Building web export..."
  godot --path game/godot/project.godot --export-release "Web" build/web/index.html
  echo "✅ Web build complete in build/web/"

# Build desktop (Linux)
build-linux:
  echo "🐧 Building Linux executable..."
  godot --path game/godot/project.godot --export-release "Linux" build/linux/our-rotting-father.x86_64
  echo "✅ Linux build complete!"

# Build desktop (Windows)
build-windows:
  echo "🪟 Building Windows executable..."
  godot --path game/godot/project.godot --export-release "Windows" build/windows/our-rotting-father.exe
  echo "✅ Windows build complete!"

# Build desktop (macOS)
build-macos:
  echo "🍎 Building macOS app..."
  godot --path game/godot/project.godot --export-release "macOS" build/macos/our-rotting-father.app
  echo "✅ macOS build complete!"

# Build all platforms
build-all: build-web build-linux build-windows build-macos
  echo "✅ All builds complete!"

# =============================================================================
# CONTENT GENERATION (Rotborn Recursion)
# =============================================================================

# Generate character sprites for game
generate-sprites:
  echo "🎨 Generating character sprites..."
  cd tools/rotborn-recursion && . venv/bin/activate && python3 ai_human_generator.py generate-batch --count 100 --output-dir ../../game/godot/assets/sprites/characters/
  echo "✅ Sprites generated!"

# Generate sprites with specific trauma palette
generate-sprites-palette PALETTE="rotting":
  echo "🎨 Generating sprites with {{PALETTE}} palette..."
  cd tools/rotborn-recursion && . venv/bin/activate && python3 ai_human_generator.py generate-batch --count 50 --palette {{PALETTE}} --output-dir ../../game/godot/assets/sprites/characters/{{PALETTE}}/
  echo "✅ Sprites generated!"

# Generate animation sprite sheets
generate-animations:
  echo "🎬 Generating animation sprite sheets..."
  cd tools/rotborn-recursion && . venv/bin/activate && python3 ai_human_generator.py generate-animation --output ../../game/godot/assets/animations/
  echo "✅ Animations generated!"

# Generate all content (sprites + animations)
generate-all: generate-sprites generate-animations
  echo "✅ All content generated!"

# =============================================================================
# TESTING
# =============================================================================

# Run Python tests (Rotborn tools)
test-python:
  echo "🧪 Running Python tests..."
  cd tools/rotborn-recursion && . venv/bin/activate && pytest tests/ -v

# Run Godot tests (requires GUT)
test-godot:
  echo "🎮 Running Godot tests..."
  godot --path game/godot/project.godot --headless --test

# Run all tests
test: test-python test-godot
  echo "✅ All tests complete!"

# =============================================================================
# CODE QUALITY
# =============================================================================

# Format Python code
format-python:
  echo "📝 Formatting Python code..."
  cd tools/rotborn-recursion && . venv/bin/activate && black generator/ app/ tests/ && isort generator/ app/ tests/

# Lint Python code
lint-python:
  echo "🔍 Linting Python code..."
  cd tools/rotborn-recursion && . venv/bin/activate && flake8 generator/ app/ tests/ && mypy generator/ app/

# Format and lint all
lint: lint-python
  echo "✅ Linting complete!"

# =============================================================================
# CLEAN
# =============================================================================

# Clean build artifacts
clean:
  echo "🧹 Cleaning build artifacts..."
  rm -rf build/web/* build/linux/* build/windows/* build/macos/*
  echo "✅ Clean complete!"

# Clean Python cache
clean-python:
  echo "🧹 Cleaning Python cache..."
  find . -type d -name __pycache__ -exec rm -rf {} +
  find . -type f -name "*.pyc" -delete
  find . -type f -name "*.pyo" -delete
  echo "✅ Python cache cleaned!"

# Clean Godot cache
clean-godot:
  echo "🧹 Cleaning Godot cache..."
  rm -rf game/godot/.godot/
  rm -rf game/godot/.import/
  echo "✅ Godot cache cleaned!"

# Clean everything
clean-all: clean clean-python clean-godot
  echo "✅ Everything cleaned!"

# =============================================================================
# DEPLOYMENT
# =============================================================================

# Deploy web build to GitHub Pages
deploy-web: build-web
  echo "🚀 Deploying to GitHub Pages..."
  cd build/web && git init && git add . && git commit -m "Deploy web build" && git push git@github.com:recursive-ai-dev/our-rotting-fathers.git gh-pages --force
  echo "✅ Deployed to GitHub Pages!"

# =============================================================================
# DEVELOPMENT WORKFLOW
# =============================================================================

# Full dev workflow: clean, generate, run
dev: clean-godot generate-sprites run
  echo "🎮 Development mode started!"

# Quick iteration: just run (no regeneration)
dev-quick: run
  echo "🎮 Quick dev mode!"

# Watch mode: regenerate sprites on changes (requires watchmedo)
dev-watch:
  echo "👁️  Watching for changes..."
  cd tools/rotborn-recursion && watchmedo shell-command --patterns="*.py" --recursive --command="just generate-sprites && just run" .
