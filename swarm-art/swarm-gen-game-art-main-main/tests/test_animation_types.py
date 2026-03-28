"""Tests for animation types and frame generation."""

import random
from generator.pure_generator import PureCharacterGenerator
from generator.animation_generator import AnimationGenerator
from generator.direction_renderer import Direction
from generator.animation_types import ANIMATION_DEFS, get_animation_def, get_all_animation_types


def _make_params():
    random.seed(42)
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    return gen._generate_character_params()


def test_frame_counts_match_definitions():
    params = _make_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    for anim_type, anim_def in ANIMATION_DEFS.items():
        frames = anim_gen.generate_animation(params, anim_type)
        assert len(frames) == anim_def.frames, \
            f"{anim_type}: expected {anim_def.frames} frames, got {len(frames)}"


def test_all_frames_non_empty():
    params = _make_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    for anim_type in ANIMATION_DEFS:
        frames = anim_gen.generate_animation(params, anim_type)
        for i, frame in enumerate(frames):
            assert frame.getbbox() is not None, \
                f"{anim_type} frame {i}: empty image"


def test_offsets_in_valid_range():
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    for anim_type, anim_def in ANIMATION_DEFS.items():
        for frame_idx in range(anim_def.frames):
            offsets = anim_gen._calculate_animation_offsets(
                anim_type, frame_idx, anim_def.frames)
            # Body offsets should not exceed canvas size
            for key in ['body_y', 'body_x', 'head_y']:
                assert abs(offsets[key]) <= 32, \
                    f"{anim_type} frame {frame_idx}: {key}={offsets[key]} out of range"


def test_animation_with_all_directions():
    params = _make_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    for d in Direction:
        frames = anim_gen.generate_animation(params, 'walk', direction=d)
        assert len(frames) == ANIMATION_DEFS['walk'].frames
        for f in frames:
            assert f.getbbox() is not None


def test_get_all_animation_types():
    types = get_all_animation_types()
    assert 'idle' in types
    assert 'attack' in types
    assert 'pickup' in types
    assert 'run_alt1' in types
    assert len(types) == 9


def test_attack_animation_frames():
    params = _make_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    frames = anim_gen.generate_animation(params, 'attack')
    assert len(frames) == 6


def test_pickup_animation_frames():
    params = _make_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    frames = anim_gen.generate_animation(params, 'pickup')
    assert len(frames) == 5
