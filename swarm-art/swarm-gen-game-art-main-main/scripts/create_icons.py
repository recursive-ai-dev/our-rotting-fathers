#!/usr/bin/env python3
"""
Helper script to convert a 512x512 PNG icon to platform-specific formats.

Usage:
    python3 scripts/create_icons.py assets/GameArtGenerator.png

Requirements:
    pip install Pillow

Generates:
    - assets/GameArtGenerator.ico      (Windows icon with multiple sizes)
    - assets/GameArtGenerator.icns     (macOS icon - manual conversion needed)
    - assets/GameArtGenerator-128.png  (Standard Linux icon)
"""

import sys
from pathlib import Path
from PIL import Image


def create_windows_icon(source_png: Path, output_ico: Path) -> None:
    """Create Windows .ico file with multiple embedded sizes."""
    img = Image.open(source_png)

    # Ensure square
    if img.size[0] != img.size[1]:
        raise ValueError(f"Icon must be square, got {img.size}")

    # Windows icon standard sizes (largest first)
    sizes = [256, 128, 64, 48, 32, 16]

    # Create resized versions
    icon_sizes = []
    for size in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        icon_sizes.append(resized)

    # Save as .ico (PyInstaller compatibility)
    icon_sizes[0].save(output_ico, "ICO", sizes=[(size, size) for size in sizes])
    print(f"✓ Created Windows icon: {output_ico}")


def create_linux_icon(source_png: Path, output_png: Path, size: int = 128) -> None:
    """Create standard Linux icon (typically 128x128)."""
    img = Image.open(source_png)
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(output_png, "PNG")
    print(f"✓ Created Linux icon ({size}x{size}): {output_png}")


def create_macos_icon_instructions(source_png: Path) -> None:
    """Print instructions for creating macOS .icns file."""
    print(f"\n⚠️  macOS icon (.icns) requires manual conversion:")
    print(f"   Option 1 (Online): Use https://cloudconvert.com/png-to-icns")
    print(f"                      Upload {source_png.name} → download .icns file")
    print(f"   Option 2 (Mac):    sips -s format icns {source_png} --out assets/GameArtGenerator.icns")
    print(f"   Option 3 (Linux):  Use ImageMagick:")
    print(f"                      convert {source_png} -define icon:auto-resize=512,256,128,64,32 assets/GameArtGenerator.icns")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/create_icons.py <source_png>")
        print("Example: python3 scripts/create_icons.py assets/GameArtGenerator.png")
        sys.exit(1)

    source_png = Path(sys.argv[1])

    if not source_png.exists():
        print(f"Error: File not found: {source_png}", file=sys.stderr)
        sys.exit(1)

    if source_png.suffix.lower() != ".png":
        print(f"Error: File must be PNG format, got {source_png.suffix}", file=sys.stderr)
        sys.exit(1)

    # Ensure assets directory exists
    assets_dir = source_png.parent
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Create Windows icon
    ico_path = assets_dir / source_png.stem + ".ico"
    try:
        create_windows_icon(source_png, ico_path)
    except Exception as e:
        print(f"✗ Failed to create Windows icon: {e}", file=sys.stderr)
        sys.exit(1)

    # Create Linux icon
    linux_icon_path = assets_dir / (source_png.stem + "-128.png")
    try:
        create_linux_icon(source_png, linux_icon_path, size=128)
    except Exception as e:
        print(f"✗ Failed to create Linux icon: {e}", file=sys.stderr)
        sys.exit(1)

    # Print macOS instructions
    create_macos_icon_instructions(source_png)

    print(f"\n✓ Icon conversion complete!")
    print(f"  Windows: {ico_path}")
    print(f"  Linux:   {linux_icon_path}")


if __name__ == "__main__":
    main()
