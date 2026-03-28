# Packaging Quick Start Guide

This guide walks you through building distributable packages for GameArtGenerator on Windows, macOS, and Linux. Use the template files provided in this directory.

**Estimated time to first EXE/AppImage**: 2-3 hours (icon creation is the longest step)

---

## Prerequisites

### All Platforms
```bash
pip install --break-system-packages PyInstaller>=6.0
```

### Windows Only
- Download **Inno Setup** from https://jrsoftware.org/isdl.php

### macOS Only
- Xcode command-line tools: `xcode-select --install`
- Apple Developer account (optional, required for notarization): https://developer.apple.com

### Linux Only
- No additional requirements (AppImage is easiest)
- Optional for DEB: `apt install devscripts ubuntu-dev-tools`

---

## Step 1: Create App Icon (2-3 hours)

All platforms need a 512x512 PNG icon.

### Option A: Commission a Pixel Artist (Best Quality)
- Reach out to freelancer platforms (Fiverr, Upwork)
- Budget: $30-50 USD
- Turnaround: 1-2 days
- Result: Professional-looking icon matching game art theme

### Option B: DIY Using Existing Artwork
- Use one of your generated characters (from quick_test/)
- Upscale to 512x512 using:
  ```bash
  # Using Python
  from PIL import Image
  img = Image.open('my_character.png')
  img = img.resize((512, 512), Image.Resampling.LANCZOS)
  img.save('assets/GameArtGenerator.png')
  ```

### Option C: Use AI Image Generator
- Generate pixel art character on Midjourney/DALL-E with prompt: "512x512 pixel art game icon, pixel art character generator"
- Budget: Free-$15 depending on service
- Turnaround: 5 minutes

### Once you have the PNG:
1. Create `assets/` directory:
   ```bash
   mkdir -p assets
   ```

2. Copy icon to `assets/GameArtGenerator.png` (512x512 PNG)

3. Convert to Windows format:
   ```bash
   # Using ImageMagick (install: brew install imagemagick)
   convert assets/GameArtGenerator.png \
     -define icon:auto-resize=256,128,64,32 \
     assets/GameArtGenerator.ico
   ```

4. Convert to macOS format:
   ```bash
   # Using online tool: https://cloudconvert.com/png-to-icns
   # Or using sips on Mac:
   sips -s format icns assets/GameArtGenerator.png \
     --out assets/GameArtGenerator.icns
   ```

---

## Step 2: Create Configuration Files (30 minutes)

### 2a. Create pyproject.toml
```bash
cp pyproject.toml.template pyproject.toml
# Edit: Change "YOUR_USERNAME" to your GitHub username
nano pyproject.toml
```

### 2b. Create PyInstaller Spec
```bash
cp GameArtGenerator.spec.template GameArtGenerator.spec
# Optional: Uncomment icon line if you have the .ico file
nano GameArtGenerator.spec
```

### 2c. Create Desktop File (Linux only)
```bash
cp GameArtGenerator.desktop.template GameArtGenerator.desktop
```

---

## Step 3: Build Standalone Executable (15 minutes)

### Windows
```bash
# Build standalone EXE (~190MB)
pyinstaller GameArtGenerator.spec --distpath ./dist

# Test it runs
dist\GameArtGenerator.exe
```

Output: `dist/GameArtGenerator.exe`

### macOS
```bash
# Build app bundle
pyinstaller GameArtGenerator.spec --distpath ./dist

# Test it runs
open dist/GameArtGenerator.app

# Optional: Create DMG installer
hdiutil create -volname "GameArtGenerator" \
  -srcfolder dist/GameArtGenerator.app \
  -ov -format UDZO \
  dist/GameArtGenerator.dmg
```

Output: `dist/GameArtGenerator.app` or `dist/GameArtGenerator.dmg`

### Linux
```bash
# Build standalone binary
pyinstaller GameArtGenerator.spec --distpath ./dist

# Test it runs
./dist/GameArtGenerator

# Create AppImage (requires linuxdeploy)
# 1. Download linuxdeploy:
wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy-x86_64.AppImage

# 2. Create AppDir structure:
mkdir -p GameArtGenerator.AppDir/usr/bin
cp dist/GameArtGenerator GameArtGenerator.AppDir/usr/bin/
cp GameArtGenerator.desktop GameArtGenerator.AppDir/
cp assets/GameArtGenerator.png GameArtGenerator.AppDir/

# 3. Build AppImage:
./linuxdeploy-x86_64.AppImage --appdir GameArtGenerator.AppDir --output appimage
```

Output: `dist/GameArtGenerator` (ELF binary) or `GameArtGenerator-2.0.0-x86_64.AppImage` (portable)

---

## Step 4: Create Windows Installer (Optional, 1 hour)

If shipping on Windows, create an installer for better user experience:

### 1. Install Inno Setup
Download from https://jrsoftware.org/isdl.php

### 2. Set Up Installer Config
```bash
cp GameArtGenerator.iss.template GameArtGenerator.iss
# Edit configuration
notepad GameArtGenerator.iss
```

Key edits in `GameArtGenerator.iss`:
- Change `#define MyAppPublisher` to your name/organization
- Change `#define MyAppURL` to your GitHub/website URL
- Optional: Provide `WizardImage.bmp` (600x499) and `WizardSmallImage.bmp` (164x314)

### 3. Build Installer
```bash
# From Windows command line or Inno Setup GUI:
iscc.exe GameArtGenerator.iss
```

Output: `dist/GameArtGenerator-2.0.0-setup.exe`

Users double-click this to install to `C:\Program Files\GameArtGenerator\`

---

## Step 5: Create Linux DEB Package (Optional, 1 hour)

For distribution on Ubuntu/Debian:

### Option A: Using fpm (Simplest)
```bash
# Install fpm
gem install fpm

# Create DEB
fpm -s dir -t deb \
  -n gamearartgenerator \
  -v 2.0.0 \
  -p ./dist/ \
  dist/GameArtGenerator=/usr/bin/ \
  GameArtGenerator.desktop=/usr/share/applications/ \
  assets/GameArtGenerator.png=/usr/share/icons/hicolor/512x512/apps/
```

### Option B: Using stdeb (Python-native)
```bash
python3 setup.py --command-packages=stdeb.command bdist_deb
```

Output: `dist/gamearartgenerator_2.0.0-1_amd64.deb`

Installation:
```bash
sudo dpkg -i dist/gamearartgenerator_2.0.0-1_amd64.deb
```

---

## Step 6: Test Builds

### Windows
```bash
# Test EXE runs
dist\GameArtGenerator.exe

# Test installer creates working shortcut
.\dist\GameArtGenerator-2.0.0-setup.exe
# Follow wizard, click "Run GameArtGenerator" at end
```

### macOS
```bash
# Test app bundle runs
open dist/GameArtGenerator.app

# Check icon appears in dock
# Verify app name shows correctly in menu bar
```

### Linux
```bash
# Test AppImage runs
./GameArtGenerator-2.0.0-x86_64.AppImage

# Test DEB installs
sudo dpkg -i dist/gamearartgenerator_2.0.0-1_amd64.deb
GameArtGenerator  # Should launch from PATH
```

---

## Step 7: Distribute

### GitHub Releases (Recommended)
1. Tag a release:
   ```bash
   git tag -a v2.0.0 -m "Release 2.0.0"
   git push origin v2.0.0
   ```

2. Go to https://github.com/YOUR_USERNAME/swarm-gen-game-art/releases

3. Create release from tag v2.0.0

4. Upload files:
   - Windows: `dist/GameArtGenerator-2.0.0-setup.exe`
   - macOS: `dist/GameArtGenerator.dmg`
   - Linux: `GameArtGenerator-2.0.0-x86_64.AppImage`
   - Linux: `dist/gamearartgenerator_2.0.0-1_amd64.deb`

Users can now download one-click installers!

### PyPI (Optional)
```bash
# Install build tool
pip install build twine

# Build wheel and source dist
python -m build

# Upload to PyPI
twine upload dist/GameArtGenerator-2.0.0-py3-none-any.whl

# Users can now: pip install GameArtGenerator
```

---

## Troubleshooting

### "Icon not found" error
- Ensure `assets/GameArtGenerator.ico` exists (Windows)
- Ensure `assets/GameArtGenerator.icns` exists (macOS)
- Run ImageMagick convert step above

### "PyQt6 plugin not found" error
- Ensure PyInstaller was run with `--collect-all=PyQt6` (it's in the spec)
- Try rebuilding: `pyinstaller --clean GameArtGenerator.spec`

### "Hidden imports" warning
- Normal; all needed imports are in the .spec file
- Safe to ignore

### AppImage won't run
- Ensure FUSE is installed: `apt install libfuse2`
- Run with verbose output: `./GameArtGenerator-2.0.0-x86_64.AppImage --appimage-extract`

### DEB install fails
- Check dpkg: `dpkg -l | grep gamearartgenerator`
- Try: `sudo apt --fix-broken install`

---

## Next Steps: Automation

Once working, automate builds with GitHub Actions:

1. Create `.github/workflows/build.yml` (see template in PACKAGING_AUDIT.md)
2. On each release tag, builds run automatically
3. Binaries upload to GitHub Releases automatically
4. No manual builds needed!

---

## File Summary

After following this guide, you'll have created:

```
GameArtGenerator/
├── assets/
│   ├── GameArtGenerator.png         (512x512 icon)
│   ├── GameArtGenerator.ico         (Windows icon)
│   └── GameArtGenerator.icns        (macOS icon)
├── pyproject.toml                  (Package metadata)
├── GameArtGenerator.spec           (PyInstaller config)
├── GameArtGenerator.desktop        (Linux launcher)
├── GameArtGenerator.iss            (Windows installer config)
├── dist/
│   ├── GameArtGenerator.exe        (Windows standalone)
│   ├── GameArtGenerator-2.0.0-setup.exe   (Windows installer)
│   ├── GameArtGenerator.app/       (macOS app bundle)
│   ├── GameArtGenerator.dmg        (macOS installer)
│   ├── GameArtGenerator            (Linux ELF binary)
│   └── gamearartgenerator_2.0.0-1_amd64.deb (Linux package)
└── GameArtGenerator-2.0.0-x86_64.AppImage  (Linux portable)
```

**You're ready to ship!**

---

## Support & Resources

- PyInstaller docs: https://pyinstaller.org
- Inno Setup docs: https://jrsoftware.org/ishelp/
- fpm: https://fpm.readthedocs.io
- macOS notarization: https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution
- Snap: https://snapcraft.io/docs
- AppImage: https://appimage.org

