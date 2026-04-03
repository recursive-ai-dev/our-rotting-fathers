#!/usr/bin/env python3
"""
ROTBORN RECURSION ENGINE - CLI Entry Point
==========================================

The swarm remembers. You witness.

Usage:
    python rotborn_generator.py generate --faction purified --count 10
    python rotborn_generator.py generate --faction rotborn --count 50 --size 64
    python rotborn_generator.py generate --palette bloodstained --count 20
    python rotborn_generator.py animate --faction system --animation twitch
    python rotborn_generator.py batch --count 100 --output-dir ./output/
"""

import sys
import os
import argparse
import json
import random
from typing import Optional, List

# Ensure generator modules are importable
sys.path.insert(0, os.path.dirname(__file__))

from generator.pure_generator import PureCharacterGenerator
from generator.mass_generator import MassCharacterGenerator
from generator.animation_generator import AnimationGenerator
from generator.rotborn_palettes import get_palette_names
from generator.animation_types import get_haunted_animation_types, get_all_animation_types
from factions import get_faction_generator, FACTION_GENERATORS


def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        import re
        print(re.sub(r'[^\x00-\x7F]+', '?', text))


def cmd_generate(args: argparse.Namespace) -> int:
    """Generate character sprites."""
    canvas_size = (args.size, args.size)
    output_dir = args.output_dir or f"rotborn_{args.faction or args.palette or 'random'}_{args.size}x{args.size}_{args.count}/"
    os.makedirs(output_dir, exist_ok=True)

    safe_print(f"Rotborn Recursion Engine - Generating {args.count} sprites")
    safe_print(f"  Faction: {args.faction or 'random'}")
    safe_print(f"  Palette: {args.palette or 'auto'}")
    safe_print(f"  Size: {args.size}x{args.size}")
    safe_print(f"  Output: {output_dir}")
    safe_print("")

    generated = 0
    base_seed = args.seed if args.seed is not None else random.randint(0, 2**31)

    for i in range(args.count):
        seed = base_seed + i

        if args.faction:
            gen = get_faction_generator(args.faction, canvas_size=canvas_size)
            sprite = gen.generate(seed=seed)
        else:
            palette = args.palette or "rotting"
            gen = PureCharacterGenerator(canvas_size=canvas_size, palette=palette)
            sprite = gen.generate_character(seed=seed)

        filename = f"rotborn_{i:06d}.png"
        filepath = os.path.join(output_dir, filename)
        sprite.save(filepath, "PNG")
        generated += 1

        if generated % max(1, args.count // 10) == 0 or generated == args.count:
            safe_print(f"  [{generated}/{args.count}] {filename}")

    safe_print(f"\nGenerated {generated} sprites in {output_dir}")
    return 0


def cmd_animate(args: argparse.Namespace) -> int:
    """Generate animated sprite sheets."""
    canvas_size = (args.size, args.size)
    output_dir = args.output_dir or f"rotborn_anim_{args.animation}_{args.size}x{args.size}/"
    os.makedirs(output_dir, exist_ok=True)

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)

    safe_print(f"Rotborn Recursion Engine - Animating ({args.animation})")
    safe_print(f"  Faction: {args.faction or 'random'}")
    safe_print(f"  Animation: {args.animation}")
    safe_print(f"  Size: {args.size}x{args.size}")
    safe_print(f"  Output: {output_dir}")

    # Generate base character params
    if args.faction:
        gen = get_faction_generator(args.faction, canvas_size=canvas_size)
        sprite = gen.generate(seed=seed)
        base_gen = PureCharacterGenerator(canvas_size=canvas_size)
        random.seed(seed)
        params = base_gen._generate_character_params()
    else:
        base_gen = PureCharacterGenerator(canvas_size=canvas_size)
        params = base_gen.generate_character(seed=seed)
        random.seed(seed)
        params = base_gen._generate_character_params()

    # Generate animation
    anim_gen = AnimationGenerator(canvas_size=canvas_size)
    frames = anim_gen.generate_animation(params, args.animation)

    # Save individual frames
    for i, frame in enumerate(frames):
        frame_path = os.path.join(output_dir, f"{args.animation}_frame_{i:02d}.png")
        frame.save(frame_path, "PNG")

    # Save sprite sheet
    sheet_path = os.path.join(output_dir, f"{args.animation}_sheet.png")
    anim_gen.create_sprite_sheet(frames, sheet_path)

    # Save APNG if requested
    if args.apng:
        from export.apng_exporter import export_apng
        from generator.animation_types import ANIMATION_DEFS
        anim_def = ANIMATION_DEFS.get(args.animation)
        duration = anim_def.speed_ms if anim_def else 150
        apng_path = os.path.join(output_dir, f"{args.animation}.png")
        export_apng(frames, apng_path, duration_ms=duration)
        safe_print(f"  APNG: {apng_path}")

    safe_print(f"\nGenerated {len(frames)} frames in {output_dir}")
    safe_print(f"Sprite sheet: {sheet_path}")
    return 0


def cmd_batch(args: argparse.Namespace) -> int:
    """Batch generate using MassCharacterGenerator."""
    canvas_size = (args.size, args.size)
    palette = args.palette or "rotting"
    output_dir = args.output_dir or f"rotborn_batch_{palette}_{args.size}x{args.size}_{args.count}/"

    safe_print(f"Rotborn Recursion Engine - Batch generation")
    safe_print(f"  Count: {args.count}")
    safe_print(f"  Palette: {palette}")
    safe_print(f"  Size: {args.size}x{args.size}")

    gen = MassCharacterGenerator(canvas_size=canvas_size, palette=palette)
    files = gen.generate_massive_batch(args.count, output_dir, save_metadata=not args.no_metadata)
    safe_print(f"\nGenerated {len(files)} sprites in {output_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rotborn_generator",
        description="Rotborn Recursion Engine - Haunted sprite generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rotborn_generator.py generate --faction purified --count 10
  python rotborn_generator.py generate --faction rotborn --count 50 --size 64
  python rotborn_generator.py generate --palette bloodstained --count 20
  python rotborn_generator.py animate --animation twitch --faction system
  python rotborn_generator.py animate --animation convulse --apng
  python rotborn_generator.py batch --count 100 --palette spore_infested
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate
    gen_parser = subparsers.add_parser("generate", help="Generate character sprites")
    gen_parser.add_argument("--faction", choices=list(FACTION_GENERATORS.keys()),
                            default=None, help="Faction (purified/rotborn/architects/system)")
    gen_parser.add_argument("--palette", choices=get_palette_names(),
                            default=None, help="Trauma palette")
    gen_parser.add_argument("--count", type=int, default=10, help="Number of sprites")
    gen_parser.add_argument("--size", type=int, default=32, help="Canvas size (square)")
    gen_parser.add_argument("--seed", type=int, default=None, help="Base seed")
    gen_parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    gen_parser.set_defaults(func=cmd_generate)

    # animate
    anim_parser = subparsers.add_parser("animate", help="Generate animated sprite sheets")
    anim_parser.add_argument("--animation", choices=get_all_animation_types(),
                             default="twitch", help="Animation type")
    anim_parser.add_argument("--faction", choices=list(FACTION_GENERATORS.keys()),
                             default=None, help="Faction")
    anim_parser.add_argument("--size", type=int, default=32, help="Canvas size")
    anim_parser.add_argument("--seed", type=int, default=None, help="Seed")
    anim_parser.add_argument("--apng", action="store_true", help="Also export APNG")
    anim_parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    anim_parser.set_defaults(func=cmd_animate)

    # batch
    batch_parser = subparsers.add_parser("batch", help="Batch generate with uniqueness checking")
    batch_parser.add_argument("--count", type=int, required=True, help="Number of sprites")
    batch_parser.add_argument("--palette", choices=get_palette_names(), default="rotting")
    batch_parser.add_argument("--size", type=int, default=32, help="Canvas size")
    batch_parser.add_argument("--output-dir", type=str, default=None)
    batch_parser.add_argument("--no-metadata", action="store_true")
    batch_parser.set_defaults(func=cmd_batch)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))
