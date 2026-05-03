#!/usr/bin/env python3
"""
Asset Pipeline: Rotborn Recursion → Godot Assets
Exports character sprites and animations to Godot project with metadata JSON files.
"""

import os
import sys
import json
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime

# Add generator to path
sys.path.insert(0, str(Path(__file__).parent / "generator"))

try:
    from generator.mass_generator import MassCharacterGenerator
    from generator.animation_generator import AnimationGenerator
    from generator.rotborn_palettes import get_palette_names
except ImportError as e:
    print(f"❌ Error importing generator modules: {e}")
    print("Make sure you're running from tools/rotborn-recursion directory")
    sys.exit(1)


# Frozen O(1)-lookup set of valid palette identifiers. Computed once at import
# time so per-call validation costs a single hash probe rather than an O(n)
# list scan or a silent fall-through to the default palette.
_VALID_PALETTES = frozenset(get_palette_names())


def _coerce_palette(name: str) -> str:
    """Validate a palette identifier; raise ValueError with a helpful hint."""
    if name not in _VALID_PALETTES:
        valid = ", ".join(sorted(_VALID_PALETTES))
        raise ValueError(
            "Unknown palette '{0}'. Valid palettes: {1}".format(name, valid)
        )
    return name


def _write_json_atomic(path: Path, payload) -> None:
    """Write JSON atomically: temp file in same dir, fsync, then os.replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(payload, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


class GodotAssetExporter:
    """Export Rotborn Recursion assets to Godot project structure"""

    def __init__(self, godot_assets_dir: str = "../../game/godot/assets"):
        self.godot_assets_dir = Path(godot_assets_dir)
        self.sprites_dir = self.godot_assets_dir / "sprites" / "characters"
        self.animations_dir = self.godot_assets_dir / "animations"
        self.metadata_dir = self.godot_assets_dir / "metadata"

        # Create directories
        self.sprites_dir.mkdir(parents=True, exist_ok=True)
        self.animations_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        self.exported_assets = []

    def export_character_batch(
        self,
        count: int = 50,
        palette: str = "rotting",
        canvas_size: tuple = (64, 64),
        output_prefix: str = None
    ):
        """Generate and export a batch of characters"""
        palette = _coerce_palette(palette)
        print(f"🎨 Generating {count} characters with '{palette}' palette...")

        generator = MassCharacterGenerator(
            canvas_size=canvas_size,
            palette=palette
        )

        output_dir = self.sprites_dir / palette
        output_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "export_date": datetime.now().isoformat(),
            "palette": palette,
            "canvas_size": canvas_size,
            "count": count,
            "characters": []
        }

        for i in range(count):
            char_params = generator.generate_unique_character_parameters()
            sprite = generator.generate_character_sprite(char_params)

            # Save sprite
            char_id = f"{palette}_{i:04d}"
            sprite_path = output_dir / f"{char_id}.png"
            sprite.save(sprite_path)

            # Track metadata
            char_meta = {
                "id": char_id,
                "file": str(sprite_path.relative_to(self.godot_assets_dir)),
                "parameters": char_params,
                "palette": palette
            }
            metadata["characters"].append(char_meta)
            self.exported_assets.append(char_meta)

            if (i + 1) % 10 == 0:
                print(f"  Generated {i + 1}/{count}...")

        # Save metadata JSON (atomic write — no half-written files on interrupt)
        meta_path = self.metadata_dir / f"{output_prefix or palette}_batch.json"
        _write_json_atomic(meta_path, metadata)

        print(f"✅ Exported {count} characters to {output_dir}/")
        print(f"📄 Metadata saved to {meta_path}")
        return metadata

    def export_animation(
        self,
        palette: str = "rotting",
        canvas_size: tuple = (64, 64),
        animation_types: list = None
    ):
        """Generate and export animations"""
        palette = _coerce_palette(palette)
        if animation_types is None:
            animation_types = ["idle", "walk", "run", "jump"]

        print(f"🎬 Generating animations: {', '.join(animation_types)}")

        generator = MassCharacterGenerator(
            canvas_size=canvas_size,
            palette=palette
        )
        anim_generator = AnimationGenerator(canvas_size=canvas_size)

        # Generate base character
        char_params = generator.generate_unique_character_parameters()

        output_dir = self.animations_dir / palette
        output_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "export_date": datetime.now().isoformat(),
            "palette": palette,
            "canvas_size": canvas_size,
            "animations": []
        }

        for anim_type in animation_types:
            print(f"  Generating {anim_type} animation...")

            try:
                frames = anim_generator.generate_animation(char_params, anim_type)

                # Parallel frame encode/save. Pillow releases the GIL during
                # PNG zlib compression, so threading delivers near-linear speedup
                # on multi-core hosts without touching the output schema.
                frame_paths = [None] * len(frames)

                def _save(idx_frame):
                    idx, frame = idx_frame
                    fp = output_dir / f"{anim_type}_frame_{idx:02d}.png"
                    frame.save(fp)
                    return idx, str(fp.relative_to(self.godot_assets_dir))

                workers = min(8, (os.cpu_count() or 1), max(1, len(frames)))
                if workers > 1 and len(frames) > 1:
                    with ThreadPoolExecutor(max_workers=workers) as pool:
                        for idx, rel in pool.map(_save, enumerate(frames)):
                            frame_paths[idx] = rel
                else:
                    for idx, rel in map(_save, enumerate(frames)):
                        frame_paths[idx] = rel

                # Save sprite sheet
                sheet_path = output_dir / f"{anim_type}_spritesheet.png"
                anim_generator.create_sprite_sheet(frames, sheet_path)

                anim_meta = {
                    "type": anim_type,
                    "frames": len(frames),
                    "frame_files": frame_paths,
                    "spritesheet": str(sheet_path.relative_to(self.godot_assets_dir))
                }
                metadata["animations"].append(anim_meta)

            except Exception as e:
                print(f"    ⚠️  Failed to generate {anim_type}: {e}")

        # Atomic metadata write
        meta_path = self.metadata_dir / f"{palette}_animations.json"
        _write_json_atomic(meta_path, metadata)

        print(f"✅ Exported animations to {output_dir}/")
        return metadata

    def export_all(self, palettes: list = None):
        """Export all palettes with characters and animations"""
        if palettes is None:
            palettes = get_palette_names()

        # Idempotent ordered dedupe + early validation. dict.fromkeys preserves
        # insertion order while collapsing duplicates; validation surfaces typos
        # before any I/O is performed.
        palettes = list(dict.fromkeys(palettes))
        for p in palettes:
            _coerce_palette(p)

        print(f"🚀 Full export for palettes: {', '.join(palettes)}")

        for palette in palettes:
            self.export_character_batch(count=50, palette=palette)
            self.export_animation(palette=palette)

        # Generate master index
        self._generate_master_index(palettes)

        print(f"\n✅ Full export complete!")
        print(f"📁 Assets: {self.godot_assets_dir}")
        print(f"📊 Total assets: {len(self.exported_assets)}")

    def _generate_master_index(self, palettes: list):
        """Generate master asset index for Godot"""
        index = {
            "version": "1.0",
            "export_date": datetime.now().isoformat(),
            "palettes": palettes,
            "assets": self.exported_assets
        }

        index_path = self.metadata_dir / "master_index.json"
        _write_json_atomic(index_path, index)

        print(f"📄 Master index: {index_path}")


def _positive_int(value):
    """argparse type: strictly positive integer."""
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        import argparse
        raise argparse.ArgumentTypeError(
            "expected a positive integer, got {0!r}".format(value)
        )
    if ivalue <= 0:
        import argparse
        raise argparse.ArgumentTypeError(
            "value must be > 0, got {0}".format(ivalue)
        )
    return ivalue


def _nonneg_int(value):
    """argparse type: non-negative integer (for --batch which accepts 0)."""
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        import argparse
        raise argparse.ArgumentTypeError(
            "expected a non-negative integer, got {0!r}".format(value)
        )
    if ivalue < 0:
        import argparse
        raise argparse.ArgumentTypeError(
            "value must be >= 0, got {0}".format(ivalue)
        )
    return ivalue


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Export Rotborn assets to Godot")
    parser.add_argument(
        "--batch", type=_nonneg_int, default=0,
        help="Generate character batch (specify count)"
    )
    parser.add_argument(
        "--palette", type=str, default="rotting",
        choices=get_palette_names(),
        help="Trauma palette to use"
    )
    parser.add_argument(
        "--animations", action="store_true",
        help="Generate animations"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Export everything (all palettes)"
    )
    parser.add_argument(
        "--size", type=_positive_int, default=64,
        help="Canvas size (default: 64x64)"
    )
    parser.add_argument(
        "--output", type=str, default="../../game/godot/assets",
        help="Output directory"
    )

    args = parser.parse_args()

    exporter = GodotAssetExporter(args.output)

    if args.all:
        exporter.export_all()
    elif args.batch > 0:
        exporter.export_character_batch(
            count=args.batch,
            palette=args.palette,
            canvas_size=(args.size, args.size)
        )
    elif args.animations:
        exporter.export_animation(
            palette=args.palette,
            canvas_size=(args.size, args.size)
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
