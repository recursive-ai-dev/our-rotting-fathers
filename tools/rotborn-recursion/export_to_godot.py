#!/usr/bin/env python3
"""
Asset Pipeline: Rotborn Recursion → Godot Assets
Exports character sprites and animations to Godot project with metadata JSON files.
"""

import os
import sys
import json
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime

# Add generator to path
sys.path.insert(0, str(Path(__file__).parent / "generator"))

try:
    from generator.mass_generator import MassCharacterGenerator
    from generator.animation_generator import AnimationGenerator
    from generator.rotborn_palettes import get_palette_names, DEFAULT_PALETTE
except ImportError as e:
    print(f"❌ Error importing generator modules: {e}")
    print("Make sure you're running from tools/rotborn-recursion directory")
    sys.exit(1)


# Frozenset enables O(1) membership checks for palette validation (Enhancement #1).
_VALID_PALETTES = frozenset(get_palette_names())


def _resolve_palette(name):
    """Validate a palette name; fall back explicitly to DEFAULT_PALETTE.

    Mirrors generator.rotborn_palettes.get_palette() fallback semantics
    but surfaces the substitution to stderr instead of silently coercing.
    """
    if name in _VALID_PALETTES:
        return name
    print(
        "⚠️  Unknown palette '{0}'; falling back to '{1}'. "
        "Valid palettes: {2}".format(name, DEFAULT_PALETTE, ", ".join(sorted(_VALID_PALETTES))),
        file=sys.stderr,
    )
    return DEFAULT_PALETTE


def _atomic_write_json(path, payload):
    """Write JSON via temp-file + os.replace so partial writes never appear on disk."""
    path = Path(path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "w") as f:
        json.dump(payload, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)


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
        palette = _resolve_palette(palette)
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

        # PNG encoding releases the GIL inside PIL, so a small thread pool
        # reduces wall-clock time on I/O-bound batches without changing outputs.
        max_workers = min(8, (os.cpu_count() or 2) * 2)
        save_futures = []
        failed = 0
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for i in range(count):
                try:
                    char_params = generator.generate_unique_character_parameters()
                    sprite = generator.generate_character_sprite(char_params)
                except Exception as e:
                    failed += 1
                    print(f"  ⚠️  Skipped character {i:04d}: {e}")
                    continue

                char_id = f"{palette}_{i:04d}"
                sprite_path = output_dir / f"{char_id}.png"
                save_futures.append(pool.submit(sprite.save, sprite_path))

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

            # Surface any save errors deterministically before writing metadata.
            for fut in as_completed(save_futures):
                exc = fut.exception()
                if exc is not None:
                    failed += 1
                    print(f"  ⚠️  Save failed: {exc}")

        # Save metadata JSON atomically
        meta_path = self.metadata_dir / f"{output_prefix or palette}_batch.json"
        _atomic_write_json(meta_path, metadata)

        ok = count - failed
        print(f"✅ Exported {ok} characters to {output_dir}/")
        if failed:
            print(f"   ({failed} failures isolated; batch preserved)")
        print(f"📄 Metadata saved to {meta_path}")
        return metadata

    def export_animation(
        self,
        palette: str = "rotting",
        canvas_size: tuple = (64, 64),
        animation_types: list = None
    ):
        """Generate and export animations"""
        palette = _resolve_palette(palette)
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

                # Save individual frames in parallel; ordering preserved via enumerate.
                frame_paths = [None] * len(frames)
                with ThreadPoolExecutor(max_workers=min(8, (os.cpu_count() or 2) * 2)) as pool:
                    futures = {}
                    for i, frame in enumerate(frames):
                        frame_path = output_dir / f"{anim_type}_frame_{i:02d}.png"
                        frame_paths[i] = str(frame_path.relative_to(self.godot_assets_dir))
                        futures[pool.submit(frame.save, frame_path)] = i
                    for fut in as_completed(futures):
                        exc = fut.exception()
                        if exc is not None:
                            raise exc

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

        # Save metadata atomically
        meta_path = self.metadata_dir / f"{palette}_animations.json"
        _atomic_write_json(meta_path, metadata)

        print(f"✅ Exported animations to {output_dir}/")
        return metadata

    def export_all(self, palettes: list = None):
        """Export all palettes with characters and animations"""
        if palettes is None:
            palettes = get_palette_names()
        else:
            palettes = [_resolve_palette(p) for p in palettes]

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
        _atomic_write_json(index_path, index)

        print(f"📄 Master index: {index_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Export Rotborn assets to Godot")
    parser.add_argument(
        "--batch", type=int, default=0,
        help="Generate character batch (specify count)"
    )
    parser.add_argument(
        "--palette", type=str, default="rotting",
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
        "--size", type=int, default=64,
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
