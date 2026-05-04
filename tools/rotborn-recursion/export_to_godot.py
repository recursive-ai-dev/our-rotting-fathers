#!/usr/bin/env python3
"""
Asset Pipeline: Rotborn Recursion → Godot Assets
Exports character sprites and animations to Godot project with metadata JSON files.
"""

import os
import sys
import json
import random
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
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


# Cap I/O parallelism conservatively: PNG encode is CPU+I/O hybrid and Pillow
# image instances are independent, but we never starve the main loop.
_IO_WORKERS = min(8, (os.cpu_count() or 2) * 2)


def _atomic_write_json(path: Path, payload: dict) -> None:
    """Write JSON via temp-file + os.replace so partial writes never surface.

    A SIGINT, OOM, or full-disk during json.dump previously left the metadata
    file half-serialized, which Godot's importer treats as a hard failure.
    Writing to a sibling temp file in the same directory guarantees the rename
    is atomic on POSIX and Windows alike.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
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

        # Generate sprites serially (PIL draw pipeline is single-threaded by
        # design), then dispatch PNG encode/save to a worker pool. Metadata
        # ordering remains deterministic because we index by `i` not by
        # completion order.
        save_jobs = []
        with ThreadPoolExecutor(max_workers=_IO_WORKERS) as pool:
            for i in range(count):
                char_params = generator.generate_unique_character_parameters()
                sprite = generator.generate_character_sprite(char_params)

                char_id = f"{palette}_{i:04d}"
                sprite_path = output_dir / f"{char_id}.png"
                save_jobs.append(pool.submit(sprite.save, sprite_path))

                rel_file = sprite_path.relative_to(self.godot_assets_dir).as_posix()
                char_meta = {
                    "id": char_id,
                    "file": rel_file,
                    "parameters": char_params,
                    "palette": palette
                }
                metadata["characters"].append(char_meta)
                self.exported_assets.append(char_meta)

                if (i + 1) % 10 == 0:
                    print(f"  Generated {i + 1}/{count}...")

            # Surface any encoder failures rather than letting them vanish.
            for fut in as_completed(save_jobs):
                fut.result()

        meta_path = self.metadata_dir / f"{output_prefix or palette}_batch.json"
        _atomic_write_json(meta_path, metadata)

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

                # Parallel frame persistence; spritesheet build stays serial.
                frame_paths = [None] * len(frames)
                with ThreadPoolExecutor(max_workers=_IO_WORKERS) as pool:
                    futures = {}
                    for i, frame in enumerate(frames):
                        frame_path = output_dir / f"{anim_type}_frame_{i:02d}.png"
                        frame_paths[i] = frame_path.relative_to(
                            self.godot_assets_dir
                        ).as_posix()
                        futures[pool.submit(frame.save, frame_path)] = i
                    for fut in as_completed(futures):
                        fut.result()

                sheet_path = output_dir / f"{anim_type}_spritesheet.png"
                anim_generator.create_sprite_sheet(frames, sheet_path)

                anim_meta = {
                    "type": anim_type,
                    "frames": len(frames),
                    "frame_files": frame_paths,
                    "spritesheet": sheet_path.relative_to(
                        self.godot_assets_dir
                    ).as_posix()
                }
                metadata["animations"].append(anim_meta)

            except Exception as e:
                print(f"    ⚠️  Failed to generate {anim_type}: {e}")

        meta_path = self.metadata_dir / f"{palette}_animations.json"
        _atomic_write_json(meta_path, metadata)

        print(f"✅ Exported animations to {output_dir}/")
        return metadata

    def export_all(self, palettes: list = None, canvas_size: tuple = (64, 64)):
        """Export all palettes with characters and animations"""
        if palettes is None:
            palettes = get_palette_names()

        # Order-preserving dedupe — guards against repeated palettes silently
        # double-writing the same batch and inflating the master index.
        palettes = list(dict.fromkeys(palettes))

        print(f"🚀 Full export for palettes: {', '.join(palettes)}")

        for palette in palettes:
            self.export_character_batch(
                count=50, palette=palette, canvas_size=canvas_size
            )
            self.export_animation(palette=palette, canvas_size=canvas_size)

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


def _resolve_seed(cli_seed):
    """Pick seed from CLI flag, else ROTBORN_SEED env var, else None."""
    if cli_seed is not None:
        return cli_seed
    raw = os.environ.get("ROTBORN_SEED")
    if raw is None or raw == "":
        return None
    try:
        return int(raw)
    except ValueError:
        print(f"⚠️  Ignoring non-integer ROTBORN_SEED={raw!r}")
        return None


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
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Optional RNG seed for reproducible exports "
             "(also honors ROTBORN_SEED env var)"
    )

    args = parser.parse_args()

    seed = _resolve_seed(args.seed)
    if seed is not None:
        random.seed(seed)
        os.environ.setdefault("PYTHONHASHSEED", str(seed))
        print(f"🎲 Seeded RNG with {seed}")

    exporter = GodotAssetExporter(args.output)
    canvas = (args.size, args.size)

    if args.all:
        exporter.export_all(canvas_size=canvas)
    elif args.batch > 0:
        exporter.export_character_batch(
            count=args.batch,
            palette=args.palette,
            canvas_size=canvas
        )
    elif args.animations:
        exporter.export_animation(
            palette=args.palette,
            canvas_size=canvas
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
