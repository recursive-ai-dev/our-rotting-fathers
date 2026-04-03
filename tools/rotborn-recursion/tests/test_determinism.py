"""Tests for deterministic generation - same seed = same nightmare."""

import random
import pytest
from PIL import Image

from generator.pure_generator import PureCharacterGenerator
from generator.mass_generator import MassCharacterGenerator
from generator.rotborn_palettes import get_palette_names


def _pixels_equal(img1: Image.Image, img2: Image.Image) -> bool:
    """Compare two images pixel by pixel."""
    if img1.size != img2.size:
        return False
    return list(img1.getdata()) == list(img2.getdata())


def test_same_seed_produces_identical_sprite():
    """Core determinism: same seed must produce identical output."""
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    sprite1 = gen.generate_character(seed=42)
    sprite2 = gen.generate_character(seed=42)
    assert _pixels_equal(sprite1, sprite2), "Same seed produced different sprites"


def test_same_seed_produces_identical_sprite_100_iterations():
    """Determinism must hold across 100 iterations."""
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    reference = gen.generate_character(seed=777)
    for i in range(100):
        result = gen.generate_character(seed=777)
        assert _pixels_equal(reference, result), f"Iteration {i}: seed 777 produced different sprite"


def test_seed_zero_works():
    """seed=0 must not be ignored (was a known bug)."""
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    sprite1 = gen.generate_character(seed=0)
    sprite2 = gen.generate_character(seed=0)
    assert _pixels_equal(sprite1, sprite2), "seed=0 produced different sprites"


def test_different_seeds_produce_different_sprites():
    """Different seeds should (almost always) produce different sprites."""
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    sprites = [gen.generate_character(seed=i) for i in range(20)]
    pixel_hashes = [hash(tuple(img.getdata())) for img in sprites]
    unique_hashes = len(set(pixel_hashes))
    assert unique_hashes >= 15, f"Only {unique_hashes}/20 unique sprites from different seeds"


def test_determinism_across_all_palettes():
    """Determinism must hold for every palette."""
    for palette_name in get_palette_names():
        gen = PureCharacterGenerator(canvas_size=(32, 32), palette=palette_name)
        s1 = gen.generate_character(seed=123)
        s2 = gen.generate_character(seed=123)
        assert _pixels_equal(s1, s2), f"Palette {palette_name}: seed 123 not deterministic"


def test_determinism_at_64x64():
    gen = PureCharacterGenerator(canvas_size=(64, 64))
    s1 = gen.generate_character(seed=55)
    s2 = gen.generate_character(seed=55)
    assert _pixels_equal(s1, s2), "64x64: seed 55 not deterministic"


def test_determinism_at_128x128():
    gen = PureCharacterGenerator(canvas_size=(128, 128))
    s1 = gen.generate_character(seed=99)
    s2 = gen.generate_character(seed=99)
    assert _pixels_equal(s1, s2), "128x128: seed 99 not deterministic"


def test_mass_generator_determinism():
    """MassCharacterGenerator must also be deterministic."""
    gen = MassCharacterGenerator(canvas_size=(32, 32))
    random.seed(42)
    params1 = gen.generate_unique_character_parameters()
    random.seed(42)
    params2 = gen.generate_unique_character_parameters()
    assert params1["gender"] == params2["gender"]
    assert params1["actual_age"] == params2["actual_age"]
    assert params1["social_class"] == params2["social_class"]


def test_faction_generators_are_deterministic():
    """Faction generators must be deterministic with same seed."""
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from factions import PurifiedGenerator, RotbornGenerator, ArchitectsGenerator, SystemGenerator

    for GenClass in [PurifiedGenerator, RotbornGenerator, ArchitectsGenerator, SystemGenerator]:
        gen = GenClass(canvas_size=(32, 32))
        s1 = gen.generate(seed=42)
        s2 = gen.generate(seed=42)
        assert _pixels_equal(s1, s2), f"{GenClass.__name__}: seed 42 not deterministic"
