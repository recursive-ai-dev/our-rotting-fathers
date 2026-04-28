#!/usr/bin/env python3
"""
Asset Pipeline: Rotborn Recursion → Godot Assets
Exports character sprites and animations to Godot project with metadata JSON files.
"""

import os
import sys
import json
import shutil
import time
import hashlib
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

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


# Bounded I/O concurrency: PIL releases the GIL during PNG compression,
# so threads (not processes) provide net wall-clock speedup without
# perturbing the generator's PRNG state, which must stay sequential.
_IO_WORKERS = min(8, (os.cpu_count() or 4))


def _atomic_write_json(path: Path, payload) -> None:
    """Crash-safe JSON write: temp file in the same directory, fsync, rename.

    os.replace() is atomic on POSIX and Windows for files on the same
    filesystem, guaranteeing readers never observe a half-written manifest.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.flush()
        try:
            os.fsync(f.fileno())
        except (OSError, AttributeError):
            pass
    os.replace(tmp, path)


def _params_fingerprint(params) -> str:
    """Stable, order-independent digest of a character's parameter dict."""
    canonical = json.dumps(params, sort_keys=True, default=str)
    return hashlib.sha1(canonical.encode("utf-8")).hexdigest()


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
        # O(1) id-keyed ledger that backs the master index, eliminating
        # duplicate rows when export_all() is invoked across overlapping
        # palette sets.
        self._seen_ids = set()

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

        # Set-based dedup ledger: even with the generator's internal
        # uniqueness pass, cross-call collisions can leak through. A
        # bounded retry on a hashed parameter fingerprint guarantees
        # the emitted batch is set-distinct without changing the
        # external schema.
        seen_fingerprints = set()
        save_jobs = []
        start = time.monotonic()

        with ThreadPoolExecutor(max_workers=_IO_WORKERS) as pool:
            for i in range(count):
                char_params = generator.generate_unique_character_parameters()
                fp = _params_fingerprint(char_params)
                retries = 0
                while fp in seen_fingerprints and retries < 8:
                    char_params = generator.generate_unique_character_parameters()
                    fp = _params_fingerprint(char_params)
                    retries += 1
                seen_fingerprints.add(fp)

                sprite = generator.generate_character_sprite(char_params)

                char_id = f"{palette}_{i:04d}"
                sprite_path = output_dir / f"{char_id}.png"
                # Parallel disk write — PIL.Image.save releases the GIL
                # during compression so threads yield real speedup here.
                save_jobs.append(pool.submit(sprite.save, sprite_path))

                char_meta = {
                    "id": char_id,
                    "file": str(sprite_path.relative_to(self.godot_assets_dir)),
                    "parameters": char_params,
                    "palette": palette
                }
                metadata["characters"].append(char_meta)
                if char_id not in self._seen_ids:
                    self._seen_ids.add(char_id)
                    self.exported_assets.append(char_meta)

                if (i + 1) % 10 == 0:
                    elapsed = time.monotonic() - start
                    rate = (i + 1) / elapsed if elapsed > 0 else 0.0
                    eta = (count - (i + 1)) / rate if rate > 0 else 0.0
                    print(f"  Generated {i + 1}/{count}... ({rate:.1f}/s, ETA {eta:.1f}s)")

            # Surface any save errors instead of swallowing them silently.
            for fut in as_completed(save_jobs):
                fut.result()

        # Save metadata JSON
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

                # Parallel frame persistence — same GIL-release rationale
                # as the character batch, with strict path ordering preserved.
                frame_paths = [None] * len(frames)
                with ThreadPoolExecutor(max_workers=_IO_WORKERS) as pool:
                    futures = {}
                    for i, frame in enumerate(frames):
                        frame_path = output_dir / f"{anim_type}_frame_{i:02d}.png"
                        frame_paths[i] = str(frame_path.relative_to(self.godot_assets_dir))
                        futures[pool.submit(frame.save, frame_path)] = i
                    for fut in as_completed(futures):
                        fut.result()

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

        # Save metadata
        meta_path = self.metadata_dir / f"{palette}_animations.json"
        _atomic_write_json(meta_path, metadata)

        print(f"✅ Exported animations to {output_dir}/")
        return metadata

    def export_all(self, palettes: list = None):
        """Export all palettes with characters and animations"""
        if palettes is None:
            palettes = get_palette_names()

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
