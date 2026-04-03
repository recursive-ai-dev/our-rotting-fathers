#!/usr/bin/env python3
"""
ANOMALY INJECTOR - THE MEMORY-AGENT'S SPECIAL ABILITY
======================================================

The Memory-Agent occasionally injects anomalies.
These are sprites that break the rules. That shouldn't exist.
That are **wrong**.

Not wrong like a bug. Wrong like a dream that knows it's a dream
and decides to do something about it.

Anomalies occur at ~5% rate. They are rare. They are unforgettable.
"""

import random
from dataclasses import dataclass
from typing import Optional, Tuple, List
from PIL import Image, ImageDraw


# Default injection rate: 5%
DEFAULT_ANOMALY_RATE = 0.05


@dataclass
class Anomaly:
    """A single anomaly type."""
    name: str
    description: str
    apply: callable  # fn(image: Image, rng: random.Random) -> Image


def _too_many_eyes(image: Image.Image, rng: random.Random) -> Image.Image:
    """Add 1-2 extra eyes in wrong places."""
    img = image.copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # Extra eyes: small dots in unexpected positions
    num_extra = rng.randint(1, 2)
    for _ in range(num_extra):
        # Place in upper half, away from center face area
        ex = rng.randint(2, w - 3)
        ey = rng.randint(2, h // 2)
        eye_size = max(1, w // 16)

        # White of eye
        draw.ellipse([ex - eye_size, ey - eye_size, ex + eye_size, ey + eye_size],
                     fill=(200, 190, 180, 255))
        # Pupil — dark, slightly off-center
        draw.ellipse([ex - 1, ey - 1, ex + 1, ey + 1], fill=(20, 15, 10, 255))

    return img


def _wrong_mouth(image: Image.Image, rng: random.Random) -> Image.Image:
    """Add a mouth in the wrong place (forehead, cheek, or vertical)."""
    img = image.copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    placement = rng.choice(["forehead", "cheek", "vertical"])
    mouth_color = (80, 40, 40, 255)
    tooth_color = (210, 200, 190, 255)

    if placement == "forehead":
        mx = w // 2
        my = h // 5
        # Horizontal mouth on forehead
        draw.line([(mx - w // 8, my), (mx + w // 8, my)], fill=mouth_color, width=1)
        # One tooth
        draw.rectangle([mx - 1, my, mx + 1, my + 2], fill=tooth_color)

    elif placement == "cheek":
        side = rng.choice([-1, 1])
        mx = w // 2 + side * (w // 4)
        my = h // 3
        draw.line([(mx - w // 10, my), (mx + w // 10, my)], fill=mouth_color, width=1)

    elif placement == "vertical":
        # Vertical mouth on face
        mx = w // 2 + rng.randint(-2, 2)
        my = h // 3
        draw.line([(mx, my - h // 10), (mx, my + h // 10)], fill=mouth_color, width=1)
        # Teeth along the vertical
        for ty in range(my - h // 12, my + h // 12, 3):
            draw.rectangle([mx - 1, ty, mx + 1, ty + 1], fill=tooth_color)

    return img


def _floating_part(image: Image.Image, rng: random.Random) -> Image.Image:
    """Detach a small body part and float it nearby."""
    img = image.copy()
    w, h = img.size

    # Sample a small region from the sprite
    region_size = max(3, w // 8)
    sx = rng.randint(w // 4, 3 * w // 4 - region_size)
    sy = rng.randint(h // 4, 3 * h // 4 - region_size)

    region = img.crop((sx, sy, sx + region_size, sy + region_size))

    # Erase original region with transparency
    draw = ImageDraw.Draw(img)
    draw.rectangle([sx, sy, sx + region_size, sy + region_size], fill=(0, 0, 0, 0))

    # Paste region in a slightly different position
    offset_x = rng.randint(-w // 6, w // 6)
    offset_y = rng.randint(-h // 6, h // 6)
    new_x = max(0, min(w - region_size, sx + offset_x))
    new_y = max(0, min(h - region_size, sy + offset_y))

    img.paste(region, (new_x, new_y), region if region.mode == 'RGBA' else None)
    return img


def _recursive_self(image: Image.Image, rng: random.Random) -> Image.Image:
    """Embed a tiny version of the sprite within itself."""
    img = image.copy()
    w, h = img.size

    # Scale down to 1/4 size
    small_w = max(4, w // 4)
    small_h = max(4, h // 4)
    small = image.resize((small_w, small_h), Image.NEAREST)

    # Place in a corner or center
    positions = [
        (0, 0),
        (w - small_w, 0),
        (0, h - small_h),
        (w - small_w, h - small_h),
        ((w - small_w) // 2, (h - small_h) // 2),
    ]
    px, py = rng.choice(positions)

    if small.mode == 'RGBA':
        img.paste(small, (px, py), small)
    else:
        img.paste(small, (px, py))

    return img


def _inverted_region(image: Image.Image, rng: random.Random) -> Image.Image:
    """Invert colors in a small region of the sprite."""
    img = image.copy()
    w, h = img.size

    # Pick a region
    rw = rng.randint(w // 6, w // 3)
    rh = rng.randint(h // 6, h // 3)
    rx = rng.randint(0, w - rw)
    ry = rng.randint(0, h - rh)

    region = img.crop((rx, ry, rx + rw, ry + rh))

    # Invert non-transparent pixels
    pixels = region.load()
    for x in range(rw):
        for y in range(rh):
            r, g, b, a = pixels[x, y]
            if a > 10:  # Only invert visible pixels
                pixels[x, y] = (255 - r, 255 - g, 255 - b, a)

    img.paste(region, (rx, ry))
    return img


def _translucent_patch(image: Image.Image, rng: random.Random) -> Image.Image:
    """Make a patch of skin semi-transparent (organs showing through)."""
    img = image.copy()
    w, h = img.size

    # Pick a torso-area region
    rw = rng.randint(w // 5, w // 3)
    rh = rng.randint(h // 5, h // 3)
    rx = rng.randint(w // 4, 3 * w // 4 - rw)
    ry = rng.randint(h // 3, 2 * h // 3 - rh)

    region = img.crop((rx, ry, rx + rw, ry + rh))
    pixels = region.load()

    # Reduce alpha of skin-colored pixels
    for x in range(rw):
        for y in range(rh):
            r, g, b, a = pixels[x, y]
            if a > 10:
                # Make semi-transparent and add a slight reddish tint
                new_a = max(60, a - 120)
                pixels[x, y] = (min(255, r + 20), max(0, g - 10), max(0, b - 10), new_a)

    img.paste(region, (rx, ry))
    return img


def _pixel_shift(image: Image.Image, rng: random.Random) -> Image.Image:
    """Randomly shift a few pixels to create a glitch effect."""
    img = image.copy()
    w, h = img.size
    pixels = img.load()

    # Shift 3-8 random pixels
    num_shifts = rng.randint(3, 8)
    for _ in range(num_shifts):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        # Move pixel to a nearby location
        nx = max(0, min(w - 1, x + rng.randint(-3, 3)))
        ny = max(0, min(h - 1, y + rng.randint(-3, 3)))
        # Swap
        pixels[x, y], pixels[nx, ny] = pixels[nx, ny], pixels[x, y]

    return img


def _merged_shadow(image: Image.Image, rng: random.Random) -> Image.Image:
    """Add a dark shadow-twin slightly offset from the sprite."""
    img = image.copy()
    w, h = img.size

    # Create dark version of sprite
    shadow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    shadow_pixels = shadow.load()
    src_pixels = image.load()

    for x in range(w):
        for y in range(h):
            r, g, b, a = src_pixels[x, y]
            if a > 10:
                shadow_pixels[x, y] = (20, 10, 15, min(180, a // 2))

    # Offset the shadow
    ox = rng.randint(-3, 3)
    oy = rng.randint(-3, 3)

    result = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    # Paste shadow first (behind)
    sx = max(0, ox)
    sy = max(0, oy)
    result.paste(shadow, (sx, sy), shadow)
    # Paste original on top
    result.paste(img, (0, 0), img)

    return result


def _extra_limb_stub(image: Image.Image, rng: random.Random) -> Image.Image:
    """Add a small limb stub emerging from the torso."""
    img = image.copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # Sample a skin color from the image
    skin_color = (142, 128, 118, 255)  # fallback
    pixels = img.load()
    for x in range(w // 3, 2 * w // 3):
        for y in range(h // 4, 3 * h // 4):
            r, g, b, a = pixels[x, y]
            if a > 100 and r > 80:
                skin_color = (r, g, b, 255)
                break

    # Draw a small stub from the torso side
    side = rng.choice([-1, 1])
    start_x = w // 2 + side * (w // 4)
    start_y = rng.randint(h // 3, 2 * h // 3)
    end_x = start_x + side * rng.randint(3, 6)
    end_y = start_y + rng.randint(-2, 4)

    draw.line([(start_x, start_y), (end_x, end_y)],
              fill=skin_color[:3] + (200,), width=max(1, w // 16))

    return img


# ============================================================================
# ANOMALY REGISTRY
# ============================================================================

ANOMALIES: List[Anomaly] = [
    Anomaly(
        name="too_many_eyes",
        description="Face has 1-2 extra eyes, randomly positioned",
        apply=_too_many_eyes,
    ),
    Anomaly(
        name="wrong_mouth",
        description="Mouth is vertical, on forehead, or on cheek",
        apply=_wrong_mouth,
    ),
    Anomaly(
        name="floating_part",
        description="A body part detaches and hovers nearby",
        apply=_floating_part,
    ),
    Anomaly(
        name="recursive",
        description="Sprite contains a smaller version of itself",
        apply=_recursive_self,
    ),
    Anomaly(
        name="inverted_region",
        description="A region of the sprite has inverted colors",
        apply=_inverted_region,
    ),
    Anomaly(
        name="translucent_skin",
        description="A patch of skin becomes semi-transparent",
        apply=_translucent_patch,
    ),
    Anomaly(
        name="pixel_shift",
        description="Random pixels shift position (glitch effect)",
        apply=_pixel_shift,
    ),
    Anomaly(
        name="shadow_twin",
        description="A dark shadow-twin appears offset from the sprite",
        apply=_merged_shadow,
    ),
    Anomaly(
        name="extra_limb",
        description="A small limb stub emerges from the torso",
        apply=_extra_limb_stub,
    ),
]

ANOMALY_NAMES = [a.name for a in ANOMALIES]


def maybe_inject_anomaly(
    image: Image.Image,
    rate: float = DEFAULT_ANOMALY_RATE,
    rng: Optional[random.Random] = None,
    force_anomaly: Optional[str] = None,
) -> Tuple[Image.Image, Optional[str]]:
    """Possibly inject an anomaly into a sprite.

    Args:
        image: The source sprite (RGBA PIL Image)
        rate: Probability of injection (default 0.05 = 5%)
        rng: Optional Random instance for deterministic behavior
        force_anomaly: Force a specific anomaly by name (for testing)

    Returns:
        Tuple of (possibly-modified image, anomaly name or None)
    """
    if rng is None:
        rng = random

    if force_anomaly:
        anomaly = next((a for a in ANOMALIES if a.name == force_anomaly), None)
        if anomaly:
            return anomaly.apply(image, rng), anomaly.name
        return image, None

    if rng.random() > rate:
        return image, None  # No anomaly this time

    anomaly = rng.choice(ANOMALIES)
    try:
        result = anomaly.apply(image, rng)
        return result, anomaly.name
    except Exception:
        # Never crash on anomaly injection — just skip it
        return image, None


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("ROTBORN RECURSION ENGINE - Anomaly Injector")
    print("=" * 50)
    print()
    print(f"Registered anomalies: {len(ANOMALIES)}")
    print()
    for anomaly in ANOMALIES:
        print(f"  {anomaly.name}: {anomaly.description}")
    print()
    print(f"Default injection rate: {DEFAULT_ANOMALY_RATE * 100:.0f}%")
    print()

    # Quick test: inject each anomaly into a test image
    test_img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(test_img)
    draw.ellipse([8, 4, 24, 20], fill=(142, 128, 118, 255))  # head
    draw.rectangle([10, 20, 22, 28], fill=(88, 82, 72, 255))  # torso

    rng = random.Random(42)
    for anomaly in ANOMALIES:
        result, name = maybe_inject_anomaly(test_img, rate=1.0, rng=rng, force_anomaly=anomaly.name)
        print(f"  {name}: {'OK' if result is not None else 'FAILED'}")
