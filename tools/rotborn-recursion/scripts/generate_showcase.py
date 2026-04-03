#!/usr/bin/env python3
"""
SHOWCASE GENERATOR
==================

Generates the best sprites for the Itch.io release page and blog post.

Run from tools/rotborn-recursion/:
    python scripts/generate_showcase.py

Output: showcase/ directory with:
    - faction_comparison.png  (4 factions side by side at 64x64)
    - palette_comparison.png  (5 palettes, same seed)
    - twitch_strip.png        (twitch animation frames)
    - anomaly_examples.png    (forced anomaly examples)
    - batch_preview.png       (grid of 20 random sprites)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from PIL import Image, ImageDraw, ImageFont
from generator.pure_generator import PureCharacterGenerator
from generator.animation_generator import AnimationGenerator
from generator.rotborn_palettes import get_palette_names
from generator.anomaly_injector import maybe_inject_anomaly, ANOMALY_NAMES
from factions import get_faction_generator, FACTION_GENERATORS

OUTPUT_DIR = "showcase"
SPRITE_SIZE = 64
SCALE = 4  # Display at 4x for visibility (256x256 per sprite)


def upscale(img: Image.Image, factor: int = SCALE) -> Image.Image:
    """Nearest-neighbor upscale for pixel art."""
    w, h = img.size
    return img.resize((w * factor, h * factor), Image.NEAREST)


def add_label(img: Image.Image, text: str, bg=(20, 15, 12), fg=(180, 170, 160)) -> Image.Image:
    """Add a text label below an image."""
    label_h = 20
    result = Image.new('RGBA', (img.width, img.height + label_h), bg + (255,))
    result.paste(img, (0, 0))
    draw = ImageDraw.Draw(result)
    # Center text
    try:
        font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
    except Exception:
        tw = len(text) * 6
    x = (img.width - tw) // 2
    draw.text((x, img.height + 2), text, fill=fg)
    return result


def make_grid(images, cols, padding=4, bg=(13, 11, 10)):
    """Arrange images in a grid."""
    rows = (len(images) + cols - 1) // cols
    w = images[0].width
    h = images[0].height
    grid = Image.new('RGBA',
                     (cols * w + (cols + 1) * padding,
                      rows * h + (rows + 1) * padding),
                     bg + (255,))
    for i, img in enumerate(images):
        row, col = divmod(i, cols)
        x = padding + col * (w + padding)
        y = padding + row * (h + padding)
        grid.paste(img, (x, y), img if img.mode == 'RGBA' else None)
    return grid


def generate_faction_comparison():
    """4 factions side by side."""
    print("  Generating faction comparison...")
    images = []
    for faction in ["purified", "rotborn", "architects", "system"]:
        gen = get_faction_generator(faction, canvas_size=(SPRITE_SIZE, SPRITE_SIZE))
        sprite = gen.generate(seed=42)
        scaled = upscale(sprite)
        labeled = add_label(scaled, faction)
        images.append(labeled)

    grid = make_grid(images, cols=4)
    path = os.path.join(OUTPUT_DIR, "faction_comparison.png")
    grid.save(path)
    print(f"    -> {path}")


def generate_palette_comparison():
    """Same seed, all 5 palettes."""
    print("  Generating palette comparison...")
    images = []
    for palette in get_palette_names():
        gen = PureCharacterGenerator(canvas_size=(SPRITE_SIZE, SPRITE_SIZE), palette=palette)
        sprite = gen.generate_character(seed=99)
        scaled = upscale(sprite)
        labeled = add_label(scaled, palette.replace("_", " "))
        images.append(labeled)

    grid = make_grid(images, cols=5)
    path = os.path.join(OUTPUT_DIR, "palette_comparison.png")
    grid.save(path)
    print(f"    -> {path}")


def generate_animation_strip():
    """Twitch animation frames."""
    print("  Generating animation strip (twitch)...")
    gen = PureCharacterGenerator(canvas_size=(SPRITE_SIZE, SPRITE_SIZE), palette="rotting")
    import random
    random.seed(42)
    params = gen._generate_character_params()

    anim_gen = AnimationGenerator(canvas_size=(SPRITE_SIZE, SPRITE_SIZE))
    frames = anim_gen.generate_animation(params, "twitch")

    images = []
    for i, frame in enumerate(frames):
        scaled = upscale(frame)
        labeled = add_label(scaled, f"twitch f{i}")
        images.append(labeled)

    grid = make_grid(images, cols=len(frames))
    path = os.path.join(OUTPUT_DIR, "twitch_strip.png")
    grid.save(path)
    print(f"    -> {path}")


def generate_anomaly_examples():
    """Forced anomaly examples."""
    print("  Generating anomaly examples...")
    gen = PureCharacterGenerator(canvas_size=(SPRITE_SIZE, SPRITE_SIZE), palette="bloodstained")
    import random
    random.seed(77)
    params = gen._generate_character_params()
    base_sprite = gen._render_character_with_params(params)

    # Show 6 anomaly types
    showcase_anomalies = ["too_many_eyes", "wrong_mouth", "recursive",
                          "translucent_skin", "shadow_twin", "extra_limb"]
    images = []
    import random as rng_mod
    for anomaly_name in showcase_anomalies:
        rng = rng_mod.Random(42)
        result, _ = maybe_inject_anomaly(base_sprite, rate=1.0, rng=rng,
                                         force_anomaly=anomaly_name)
        scaled = upscale(result)
        labeled = add_label(scaled, anomaly_name.replace("_", " "))
        images.append(labeled)

    grid = make_grid(images, cols=3)
    path = os.path.join(OUTPUT_DIR, "anomaly_examples.png")
    grid.save(path)
    print(f"    -> {path}")


def generate_batch_preview():
    """Grid of 20 random sprites across factions."""
    print("  Generating batch preview (20 sprites)...")
    factions = list(FACTION_GENERATORS.keys())
    images = []
    for i in range(20):
        faction = factions[i % len(factions)]
        gen = get_faction_generator(faction, canvas_size=(SPRITE_SIZE, SPRITE_SIZE))
        sprite = gen.generate(seed=i * 7 + 13)
        scaled = upscale(sprite)
        images.append(scaled)

    grid = make_grid(images, cols=5)
    path = os.path.join(OUTPUT_DIR, "batch_preview.png")
    grid.save(path)
    print(f"    -> {path}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Rotborn Recursion Engine — Showcase Generator")
    print(f"Output: {OUTPUT_DIR}/")
    print()

    generate_faction_comparison()
    generate_palette_comparison()
    generate_animation_strip()
    generate_anomaly_examples()
    generate_batch_preview()

    print()
    print(f"Done. {len(os.listdir(OUTPUT_DIR))} files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
