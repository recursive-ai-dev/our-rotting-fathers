"""Tests for trauma palettes - the god's last memories."""

import pytest
from generator.rotborn_palettes import (
    ALL_PALETTES, get_palette, get_palette_names,
    ROTTING, BLOODSTAINED, SPORE_INFESTED, BONE_DRY, BRUISED,
    TraumaPalette,
)


def test_all_five_palettes_exist():
    names = get_palette_names()
    assert "rotting" in names
    assert "bloodstained" in names
    assert "spore_infested" in names
    assert "bone_dry" in names
    assert "bruised" in names
    assert len(names) == 5


def test_each_palette_has_required_color_lists():
    for name, palette in ALL_PALETTES.items():
        assert len(palette.skin_tones) >= 5, f"{name}: need >=5 skin tones"
        assert len(palette.hair_colors) >= 4, f"{name}: need >=4 hair colors"
        assert len(palette.clothing_colors) >= 4, f"{name}: need >=4 clothing colors"
        assert len(palette.eye_colors) >= 3, f"{name}: need >=3 eye colors"
        assert len(palette.accent_colors) >= 3, f"{name}: need >=3 accent colors"


def test_no_bright_cheerful_colors():
    """No color should be bright/cheerful (high saturation + high value)."""
    for name, palette in ALL_PALETTES.items():
        all_colors = (
            palette.skin_tones
            + palette.hair_colors
            + palette.clothing_colors
            + palette.eye_colors
        )
        for r, g, b in all_colors:
            # Reject colors that are too bright AND too saturated
            brightness = (r + g + b) / 3
            max_c = max(r, g, b)
            min_c = min(r, g, b)
            saturation = (max_c - min_c) / max_c if max_c > 0 else 0
            assert not (brightness > 200 and saturation > 0.5), (
                f"{name}: color ({r},{g},{b}) is too bright/cheerful "
                f"(brightness={brightness:.0f}, saturation={saturation:.2f})"
            )


def test_get_palette_returns_correct_type():
    for name in get_palette_names():
        p = get_palette(name)
        assert isinstance(p, TraumaPalette)
        assert p.name == name


def test_get_palette_unknown_returns_default():
    p = get_palette("nonexistent_palette")
    assert p is not None
    assert isinstance(p, TraumaPalette)


def test_palette_colors_are_valid_rgb():
    for name, palette in ALL_PALETTES.items():
        all_colors = (
            palette.skin_tones + palette.hair_colors
            + palette.clothing_colors + palette.eye_colors
            + palette.accent_colors
        )
        for color in all_colors:
            assert len(color) == 3, f"{name}: color {color} must be (R,G,B)"
            r, g, b = color
            assert 0 <= r <= 255, f"{name}: R={r} out of range"
            assert 0 <= g <= 255, f"{name}: G={g} out of range"
            assert 0 <= b <= 255, f"{name}: B={b} out of range"


def test_rotting_palette_is_desaturated():
    """Rotting palette should be mostly desaturated (low saturation)."""
    for r, g, b in ROTTING.skin_tones:
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        saturation = (max_c - min_c) / max_c if max_c > 0 else 0
        assert saturation < 0.3, f"Rotting skin ({r},{g},{b}) too saturated: {saturation:.2f}"


def test_bloodstained_palette_has_red_tones():
    """Bloodstained palette should have reddish tones."""
    red_dominant = 0
    for r, g, b in BLOODSTAINED.skin_tones:
        if r > g and r > b:
            red_dominant += 1
    assert red_dominant >= 3, "Bloodstained palette should have mostly red-dominant skin tones"


def test_spore_infested_palette_has_green_tones():
    """Spore infested palette should have greenish tones."""
    green_present = 0
    for r, g, b in SPORE_INFESTED.skin_tones:
        if g >= r and g >= b:
            green_present += 1
    assert green_present >= 3, "Spore infested palette should have green-dominant skin tones"


def test_bone_dry_palette_is_pale():
    """Bone dry palette should be pale (high brightness)."""
    for r, g, b in BONE_DRY.skin_tones:
        brightness = (r + g + b) / 3
        assert brightness > 130, f"Bone dry skin ({r},{g},{b}) should be pale, got brightness={brightness:.0f}"


def test_palette_has_mood_description():
    for name, palette in ALL_PALETTES.items():
        assert palette.mood, f"{name}: palette must have a mood description"
        assert len(palette.mood) > 10, f"{name}: mood description too short"
