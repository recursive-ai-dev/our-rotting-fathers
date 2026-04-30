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
import re
import tempfile
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List

# Ensure generator modules are importable
sys.path.insert(0, os.path.dirname(__file__))

from generator.pure_generator import PureCharacterGenerator
from generator.mass_generator import MassCharacterGenerator
from generator.animation_generator import AnimationGenerator
from generator.rotborn_palettes import get_palette_names
from generator.animation_types import get_haunted_animation_types, get_all_animation_types
from factions import get_faction_generator, FACTION_GENERATORS


# Pre-compiled once at import time; avoids per-call `import re` in the
# UnicodeEncodeError fallback path of safe_print().
_NON_ASCII_RE = re.compile(r'[^\x00-\x7F]+')

# PNG encoding (zlib_deflate) releases the GIL inside Pillow, so threads --
# not processes -- can overlap persistence with the deterministic main-thread
# render loop. Capped at 8: empirically the saturation point on commodity SSDs
# beyond which contention dominates throughput gains.
_SAVE_WORKERS = min(8, (os.cpu_count() or 1))


def _positive_int(value: str) -> int:
    """argparse type validator: accepts only strictly positive integers."""
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(
            "expected a positive integer, got %r" % (value,)
        )
    if ivalue < 1:
        raise argparse.ArgumentTypeError(
            "expected a positive integer (>= 1), got %d" % ivalue
        )
    return ivalue


def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        print(_NON_ASCII_RE.sub('?', text))


def _atomic_save(image, filepath: str, fmt: str = "PNG") -> None:
    """Persist `image` such that readers never observe a partial file.

    Renders to a sibling tempfile so os.replace stays on the same filesystem
    (atomic on POSIX, atomic-on-overwrite on NTFS), then renames into place.
    Required for long-running generation runs that may be SIGINT-killed mid
    write -- the prior direct-save path could leave 0-byte / truncated PNGs
    that downstream importers (Godot ResourceLoader, sheet_builder) treat as
    fatal asset corruption.
    """
    target_dir = os.path.dirname(filepath) or "."
    fd, tmp_path = tempfile.mkstemp(prefix=".rotborn-", suffix=".tmp", dir=target_dir)
    try:
        os.close(fd)
        image.save(tmp_path, fmt)
        os.replace(tmp_path, filepath)
    except BaseException:
        # SIGINT / disk-full / encode error -- sweep the orphan tempfile.
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _zero_pad_width(count: int) -> int:
    """Filename pad width: minimum 6 (preserves the legacy `:06d` schema for
    every count <= 1_000_000), expanding only when the run would otherwise
    overflow 6 digits. Guarantees lexicographic sort order over the full
    batch -- prior fixed `:06d` silently broke `ls`-ordered ingestion past
    one million sprites."""
    return max(6, len(str(max(0, count - 1))))


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

    # Use randrange for strict [0, 2**31) seed domain; randint(0, 2**31) is
    # inclusive on the upper bound and can emit 0x80000000, which straddles
    # the int32 signed/unsigned boundary for downstream metadata consumers.
    base_seed = args.seed if args.seed is not None else random.randrange(2**31)
    # Hoist loop-invariant computations out of the hot loop.
    progress_step = max(1, args.count // 10)
    pad_width = _zero_pad_width(args.count)

    # Hoist generator instantiation out of the hot loop. Both the faction
    # wrappers and PureCharacterGenerator re-seed the RNG per call and are
    # stateless across seeds, so a single instance can service the whole run
    # and amortises palette/scale setup (O(N) -> O(1) constructors).
    if args.faction:
        faction_gen = get_faction_generator(args.faction, canvas_size=canvas_size)
        gen_fn = lambda s: faction_gen.generate(seed=s)
    else:
        pure_gen = PureCharacterGenerator(
            canvas_size=canvas_size,
            palette=args.palette or "rotting",
        )
        gen_fn = lambda s: pure_gen.generate_character(seed=s)

    # The faction/pure generators reseed the global RNG per call. Snapshot the
    # caller's RNG state so in-process invocations (pytest harness, GUI host,
    # conductor automation) are not silently mutated by side-effects of this
    # subcommand. Restored unconditionally in the finally clause below.
    rng_state = random.getstate()
    generated = 0
    try:
        with ThreadPoolExecutor(max_workers=_SAVE_WORKERS) as pool:
            inflight: "deque" = deque()
            for i in range(args.count):
                sprite = gen_fn(base_seed + i)

                filename = f"rotborn_{i:0{pad_width}d}.png"
                filepath = os.path.join(output_dir, filename)
                inflight.append((pool.submit(_atomic_save, sprite, filepath), filename))
                generated += 1

                # Bounded backpressure: keeps in-memory sprite/queue depth
                # to O(workers) instead of O(count). Re-raises any save error
                # before we accumulate further work.
                if len(inflight) >= 2 * _SAVE_WORKERS:
                    fut, _name = inflight.popleft()
                    fut.result()

                if generated % progress_step == 0 or generated == args.count:
                    safe_print(f"  [{generated}/{args.count}] {filename}")

            # Drain remaining writes; .result() surfaces any deferred error.
            for fut, _name in inflight:
                fut.result()
    finally:
        random.setstate(rng_state)

    safe_print(f"\nGenerated {generated} sprites in {output_dir}")
    return 0


def cmd_animate(args: argparse.Namespace) -> int:
    """Generate animated sprite sheets."""
    canvas_size = (args.size, args.size)
    output_dir = args.output_dir or f"rotborn_anim_{args.animation}_{args.size}x{args.size}/"
    os.makedirs(output_dir, exist_ok=True)

    seed = args.seed if args.seed is not None else random.randrange(2**31)

    safe_print(f"Rotborn Recursion Engine - Animating ({args.animation})")
    safe_print(f"  Faction: {args.faction or 'random'}")
    safe_print(f"  Animation: {args.animation}")
    safe_print(f"  Size: {args.size}x{args.size}")
    safe_print(f"  Output: {output_dir}")

    # Generate base character params.
    # The prior implementation called gen.generate()/generate_character() and
    # then discarded the rendered sprite, re-seeded RNG, and re-derived params.
    # Since _generate_character_params() is the only output we consume, we seed
    # once and call it directly -- eliminating a full wasted sprite render.
    base_gen = PureCharacterGenerator(canvas_size=canvas_size)

    # Sandbox the global RNG mutation (see cmd_generate for rationale).
    rng_state = random.getstate()
    try:
        random.seed(seed)
        params = base_gen._generate_character_params()

        # Generate animation
        anim_gen = AnimationGenerator(canvas_size=canvas_size)
        frames = anim_gen.generate_animation(params, args.animation)

        # Save individual frames atomically
        for i, frame in enumerate(frames):
            frame_path = os.path.join(output_dir, f"{args.animation}_frame_{i:02d}.png")
            _atomic_save(frame, frame_path)

        # Save sprite sheet (delegated to AnimationGenerator -- contract preserved)
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
    finally:
        random.setstate(rng_state)

    safe_print(f"\nGenerated {len(frames)} frames in {output_dir}")
    safe_print(f"Sprite sheet: {sheet_path}")
    return 0


def cmd_batch(args: argparse.Namespace) -> int:
    """Batch generate using MassCharacterGenerator."""
    canvas_size = (args.size, args.size)
    palette = args.palette or "rotting"
    output_dir = args.output_dir or f"rotborn_batch_{palette}_{args.size}x{args.size}_{args.count}/"
    os.makedirs(output_dir, exist_ok=True)

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
    gen_parser.add_argument("--count", type=_positive_int, default=10, help="Number of sprites")
    gen_parser.add_argument("--size", type=_positive_int, default=32, help="Canvas size (square)")
    gen_parser.add_argument("--seed", type=int, default=None, help="Base seed")
    gen_parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    gen_parser.set_defaults(func=cmd_generate)

    # animate
    anim_parser = subparsers.add_parser("animate", help="Generate animated sprite sheets")
    anim_parser.add_argument("--animation", choices=get_all_animation_types(),
                             default="twitch", help="Animation type")
    anim_parser.add_argument("--faction", choices=list(FACTION_GENERATORS.keys()),
                             default=None, help="Faction")
    anim_parser.add_argument("--size", type=_positive_int, default=32, help="Canvas size")
    anim_parser.add_argument("--seed", type=int, default=None, help="Seed")
    anim_parser.add_argument("--apng", action="store_true", help="Also export APNG")
    anim_parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    anim_parser.set_defaults(func=cmd_animate)

    # batch
    batch_parser = subparsers.add_parser("batch", help="Batch generate with uniqueness checking")
    batch_parser.add_argument("--count", type=_positive_int, required=True, help="Number of sprites")
    batch_parser.add_argument("--palette", choices=get_palette_names(), default="rotting")
    batch_parser.add_argument("--size", type=_positive_int, default=32, help="Canvas size")
    batch_parser.add_argument("--output-dir", type=str, default=None)
    batch_parser.add_argument("--no-metadata", action="store_true")
    batch_parser.set_defaults(func=cmd_batch)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Console-script entry point.

    Declared in pyproject.toml as ``rotborn = "rotborn_generator:main"``.
    Accepts an optional argv list so the module is callable from in-process
    test harnesses (``main(["generate", "--count", "1"])``) without having to
    mutate ``sys.argv``.

    Returns the integer exit code from the dispatched subcommand. Handles
    ``KeyboardInterrupt`` with POSIX exit code 130 and swallows
    ``BrokenPipeError`` (exit 0) so piping output into ``head``/``less`` no
    longer dumps a traceback.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        safe_print("\nInterrupted.")
        return 130
    except BrokenPipeError:
        try:
            sys.stdout.flush()
        except Exception:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
