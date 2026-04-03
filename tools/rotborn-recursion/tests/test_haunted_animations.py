"""Tests for haunted animations - twitch, shamble, convulse, stumble, worship, transform."""

import random
import pytest
from generator.pure_generator import PureCharacterGenerator
from generator.animation_generator import AnimationGenerator
from generator.animation_types import (
    ANIMATION_DEFS, get_haunted_animation_types, HAUNTED_ANIMATIONS,
)


def _make_params():
    random.seed(42)
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    return gen._generate_character_params()


def test_haunted_animation_types_registered():
    haunted = get_haunted_animation_types()
    assert "twitch" in haunted
    assert "shamble" in haunted
    assert "convulse" in haunted
    assert "stumble" in haunted
    assert "worship" in haunted
    assert "transform" in haunted
    assert len(haunted) == 6


def test_haunted_animations_in_main_registry():
    for anim in HAUNTED_ANIMATIONS:
        assert anim in ANIMATION_DEFS, f"{anim} not in ANIMATION_DEFS"


def test_twitch_has_three_frames():
    assert ANIMATION_DEFS["twitch"].frames == 3


def test_shamble_has_four_frames():
    assert ANIMATION_DEFS["shamble"].frames == 4


def test_convulse_has_three_frames():
    assert ANIMATION_DEFS["convulse"].frames == 3


def test_stumble_has_four_frames():
    assert ANIMATION_DEFS["stumble"].frames == 4


def test_worship_has_six_frames():
    assert ANIMATION_DEFS["worship"].frames == 6


def test_transform_has_five_frames():
    assert ANIMATION_DEFS["transform"].frames == 5


def test_all_haunted_animations_generate_correct_frame_count():
    params = _make_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    for anim_type in HAUNTED_ANIMATIONS:
        frames = anim_gen.generate_animation(params, anim_type)
        expected = ANIMATION_DEFS[anim_type].frames
        assert len(frames) == expected, f"{anim_type}: expected {expected} frames, got {len(frames)}"


def test_all_haunted_animation_frames_non_empty():
    params = _make_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    for anim_type in HAUNTED_ANIMATIONS:
        frames = anim_gen.generate_animation(params, anim_type)
        for i, frame in enumerate(frames):
            assert frame.getbbox() is not None, f"{anim_type} frame {i}: empty image"


def test_haunted_animation_offsets_in_valid_range():
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    for anim_type in HAUNTED_ANIMATIONS:
        anim_def = ANIMATION_DEFS[anim_type]
        for frame_idx in range(anim_def.frames):
            offsets = anim_gen._calculate_animation_offsets(anim_type, frame_idx, anim_def.frames)
            for key in ['body_y', 'body_x', 'head_y']:
                assert abs(offsets[key]) <= 32, (
                    f"{anim_type} frame {frame_idx}: {key}={offsets[key]} out of range"
                )


def test_haunted_animations_at_64x64():
    random.seed(42)
    gen = PureCharacterGenerator(canvas_size=(64, 64))
    params = gen._generate_character_params()
    anim_gen = AnimationGenerator(canvas_size=(64, 64))
    for anim_type in HAUNTED_ANIMATIONS:
        frames = anim_gen.generate_animation(params, anim_type)
        assert len(frames) == ANIMATION_DEFS[anim_type].frames
        for f in frames:
            assert f.size == (64, 64)
            assert f.getbbox() is not None


def test_twitch_frames_differ():
    """Twitch frames should not all be identical (the body is moving)."""
    params = _make_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    frames = anim_gen.generate_animation(params, "twitch")
    pixel_hashes = [hash(tuple(f.getdata())) for f in frames]
    assert len(set(pixel_hashes)) > 1, "Twitch frames are all identical — no movement"


def test_convulse_frames_differ():
    """Convulse frames should differ significantly."""
    params = _make_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    frames = anim_gen.generate_animation(params, "convulse")
    pixel_hashes = [hash(tuple(f.getdata())) for f in frames]
    assert len(set(pixel_hashes)) > 1, "Convulse frames are all identical — no movement"


def test_haunted_animation_loop_flags():
    """Looping animations should loop; one-shots should not."""
    assert ANIMATION_DEFS["twitch"].loop is True
    assert ANIMATION_DEFS["shamble"].loop is True
    assert ANIMATION_DEFS["convulse"].loop is True
    assert ANIMATION_DEFS["worship"].loop is True
    assert ANIMATION_DEFS["stumble"].loop is False
    assert ANIMATION_DEFS["transform"].loop is False
