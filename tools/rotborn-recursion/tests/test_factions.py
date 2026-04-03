"""Tests for faction generators - each faction must produce distinct sprites."""

import random
import pytest
from PIL import Image

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from factions import (
    PurifiedGenerator, RotbornGenerator, ArchitectsGenerator, SystemGenerator,
    get_faction_generator, FACTION_GENERATORS,
)


def _avg_color(img: Image.Image):
    """Get average RGB of non-transparent pixels."""
    pixels = [(r, g, b) for r, g, b, a in img.getdata() if a > 10]
    if not pixels:
        return (0, 0, 0)
    return tuple(sum(c[i] for c in pixels) // len(pixels) for i in range(3))


def test_all_four_factions_registered():
    assert "purified" in FACTION_GENERATORS
    assert "rotborn" in FACTION_GENERATORS
    assert "architects" in FACTION_GENERATORS
    assert "system" in FACTION_GENERATORS


def test_get_faction_generator_returns_correct_type():
    assert isinstance(get_faction_generator("purified"), PurifiedGenerator)
    assert isinstance(get_faction_generator("rotborn"), RotbornGenerator)
    assert isinstance(get_faction_generator("architects"), ArchitectsGenerator)
    assert isinstance(get_faction_generator("system"), SystemGenerator)


def test_get_faction_generator_unknown_raises():
    with pytest.raises(ValueError):
        get_faction_generator("unknown_faction")


def test_each_faction_generates_valid_sprite():
    for name, GenClass in FACTION_GENERATORS.items():
        gen = GenClass(canvas_size=(32, 32))
        sprite = gen.generate(seed=42)
        assert sprite is not None, f"{name}: generate() returned None"
        assert sprite.size == (32, 32), f"{name}: wrong size {sprite.size}"
        assert sprite.mode == 'RGBA', f"{name}: wrong mode {sprite.mode}"
        assert sprite.getbbox() is not None, f"{name}: empty sprite"


def test_each_faction_generates_at_64x64():
    for name, GenClass in FACTION_GENERATORS.items():
        gen = GenClass(canvas_size=(64, 64))
        sprite = gen.generate(seed=10)
        assert sprite.size == (64, 64), f"{name}: wrong size at 64x64"
        assert sprite.getbbox() is not None, f"{name}: empty sprite at 64x64"


def test_factions_produce_visually_distinct_sprites():
    """Different factions should produce sprites with different average colors."""
    avg_colors = {}
    for name, GenClass in FACTION_GENERATORS.items():
        gen = GenClass(canvas_size=(32, 32))
        # Average over 5 sprites to reduce variance
        sprites = [gen.generate(seed=i) for i in range(5)]
        avg_r = sum(_avg_color(s)[0] for s in sprites) // 5
        avg_g = sum(_avg_color(s)[1] for s in sprites) // 5
        avg_b = sum(_avg_color(s)[2] for s in sprites) // 5
        avg_colors[name] = (avg_r, avg_g, avg_b)

    # At least some factions should differ by >10 in at least one channel
    factions = list(avg_colors.keys())
    found_difference = False
    for i in range(len(factions)):
        for j in range(i + 1, len(factions)):
            c1 = avg_colors[factions[i]]
            c2 = avg_colors[factions[j]]
            diff = max(abs(c1[k] - c2[k]) for k in range(3))
            if diff > 10:
                found_difference = True
                break
    assert found_difference, "All factions produce identical average colors — no visual distinction"


def test_purified_batch_generation():
    gen = PurifiedGenerator(canvas_size=(32, 32))
    sprites = gen.generate_batch(count=10, seed=100)
    assert len(sprites) == 10
    for i, s in enumerate(sprites):
        assert s.size == (32, 32), f"Purified batch[{i}]: wrong size"
        assert s.getbbox() is not None, f"Purified batch[{i}]: empty"


def test_rotborn_batch_generation():
    gen = RotbornGenerator(canvas_size=(32, 32))
    sprites = gen.generate_batch(count=10, seed=200)
    assert len(sprites) == 10
    for s in sprites:
        assert s.getbbox() is not None


def test_architects_batch_generation():
    gen = ArchitectsGenerator(canvas_size=(32, 32))
    sprites = gen.generate_batch(count=10, seed=300)
    assert len(sprites) == 10
    for s in sprites:
        assert s.getbbox() is not None


def test_system_batch_generation():
    gen = SystemGenerator(canvas_size=(32, 32))
    sprites = gen.generate_batch(count=10, seed=400)
    assert len(sprites) == 10
    for s in sprites:
        assert s.getbbox() is not None


def test_purified_ranks_generate():
    gen = PurifiedGenerator(canvas_size=(32, 32))
    for rank in ["flesh_bound", "memory_stripped", "hollow"]:
        sprite = gen.generate(seed=42, rank=rank)
        assert sprite.getbbox() is not None, f"Purified rank {rank}: empty sprite"


def test_rotborn_stages_generate():
    gen = RotbornGenerator(canvas_size=(32, 32))
    for stage in ["seed", "sprout", "bloom", "twisted"]:
        sprite = gen.generate(seed=42, stage=stage)
        assert sprite.getbbox() is not None, f"Rotborn stage {stage}: empty sprite"


def test_system_implant_stages_generate():
    gen = SystemGenerator(canvas_size=(32, 32))
    for stage in ["novice", "synapse", "relay", "prophet"]:
        sprite = gen.generate(seed=42, implant_stage=stage)
        assert sprite.getbbox() is not None, f"System stage {stage}: empty sprite"
