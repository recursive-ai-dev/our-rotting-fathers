#!/usr/bin/env python3
"""
Asset Pipeline: Rotborn Recursion → Godot Assets
Exports character sprites and animations to Godot project with metadata JSON files.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

_DEDUP_RETRY_BUDGET = 32

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
        # Single canonical timestamp shared across every metadata file
        # produced in this export session, so batch/animation/master JSONs
        # agree on a single point-in-time and remain diff-stable.
        self._session_timestamp = datetime.now().isoformat()
        # (palette, canvas_size) -> MassCharacterGenerator
        self._generator_cache = {}

    def _get_generator(self, palette, canvas_size):
        """Return a memoized MassCharacterGenerator; palette load is non-trivial."""
        key = (palette, tuple(canvas_size))
        gen = self._generator_cache.get(key)
        if gen is None:
            gen = MassCharacterGenerator(canvas_size=canvas_size, palette=palette)
            self._generator_cache[key] = gen
        return gen

    @staticmethod
    def _param_signature(params):
        """Stable, hashable canonical form for O(1) dedup."""
        return json.dumps(params, sort_keys=True, default=str)

    def _rel_posix(self, path):
        """Relative path normalized to forward slashes (Godot import contract)."""
        return Path(path).relative_to(self.godot_assets_dir).as_posix()

    def _atomic_write_json(self, path, payload):
        """Write JSON via temp + os.replace so a crash never leaves a half-written
        metadata file that downstream Godot importers would reject."""
        path = Path(path)
        tmp = path.with_name(path.name + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(str(tmp), str(path))
    
    def export_character_batch(
        self,
        count: int = 50,
        palette: str = "rotting",
        canvas_size: tuple = (64, 64),
        output_prefix: str = None
    ):
        """Generate and export a batch of characters"""
        print(f"🎨 Generating {count} characters with '{palette}' palette...")

        generator = self._get_generator(palette, canvas_size)

        output_dir = self.sprites_dir / palette
        output_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "export_date": self._session_timestamp,
            "palette": palette,
            "canvas_size": canvas_size,
            "count": count,
            "characters": []
        }

        # Cross-iteration dedup: the per-call generator does not guarantee
        # uniqueness across the batch, so duplicates would otherwise ship
        # under distinct char_ids. Bounded retries avoid infinite loops if
        # the parameter space is exhausted.
        seen = set()
        for i in range(count):
            char_params = generator.generate_unique_character_parameters()
            sig = self._param_signature(char_params)
            attempts = 0
            while sig in seen and attempts < _DEDUP_RETRY_BUDGET:
                char_params = generator.generate_unique_character_parameters()
                sig = self._param_signature(char_params)
                attempts += 1
            seen.add(sig)

            sprite = generator.generate_character_sprite(char_params)

            # Save sprite
            char_id = "{0}_{1:04d}".format(palette, i)
            sprite_path = output_dir / (char_id + ".png")
            sprite.save(sprite_path)

            # Track metadata
            char_meta = {
                "id": char_id,
                "file": self._rel_posix(sprite_path),
                "parameters": char_params,
                "palette": palette
            }
            metadata["characters"].append(char_meta)
            self.exported_assets.append(char_meta)

            if (i + 1) % 10 == 0:
                print(f"  Generated {i + 1}/{count}...")

        # Save metadata JSON
        meta_path = self.metadata_dir / f"{output_prefix or palette}_batch.json"
        self._atomic_write_json(meta_path, metadata)

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

        generator = self._get_generator(palette, canvas_size)
        anim_generator = AnimationGenerator(canvas_size=canvas_size)

        # Generate base character
        char_params = generator.generate_unique_character_parameters()

        output_dir = self.animations_dir / palette
        output_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "export_date": self._session_timestamp,
            "palette": palette,
            "canvas_size": canvas_size,
            "animations": []
        }

        for anim_type in animation_types:
            print(f"  Generating {anim_type} animation...")

            try:
                frames = anim_generator.generate_animation(char_params, anim_type)

                # Save individual frames
                frame_paths = []
                for i, frame in enumerate(frames):
                    frame_path = output_dir / f"{anim_type}_frame_{i:02d}.png"
                    frame.save(frame_path)
                    frame_paths.append(self._rel_posix(frame_path))

                # Save sprite sheet
                sheet_path = output_dir / f"{anim_type}_spritesheet.png"
                anim_generator.create_sprite_sheet(frames, sheet_path)

                anim_meta = {
                    "type": anim_type,
                    "frames": len(frames),
                    "frame_files": frame_paths,
                    "spritesheet": self._rel_posix(sheet_path)
                }
                metadata["animations"].append(anim_meta)

            except Exception as e:
                print(f"    ⚠️  Failed to generate {anim_type}: {e}")

        # Save metadata
        meta_path = self.metadata_dir / f"{palette}_animations.json"
        self._atomic_write_json(meta_path, metadata)

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
            "export_date": self._session_timestamp,
            "palettes": palettes,
            "assets": self.exported_assets
        }

        index_path = self.metadata_dir / "master_index.json"
        self._atomic_write_json(index_path, index)

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
