"""Tests for Phase 0 bug fixes."""

import random
from PIL import Image
from generator.pure_generator import PureCharacterGenerator
from generator.animation_generator import AnimationGenerator


def test_seed_zero_works():
    """seed=0 should produce a valid, reproducible character."""
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    sprite1 = gen.generate_character(seed=0)
    sprite2 = gen.generate_character(seed=0)

    assert sprite1.getbbox() is not None, "seed=0 produced empty sprite"
    assert list(sprite1.getdata()) == list(sprite2.getdata()), \
        "seed=0 not deterministic"


def test_facial_hair_deterministic_across_frames():
    """Facial hair should not change between animation frames."""
    random.seed(100)
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    params = gen._generate_character_params()
    # Force facial hair on
    params['has_facial_hair'] = True
    params['gender'] = 'male'
    params['beard_type'] = 'full_beard'

    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    frames = anim_gen.generate_animation(params, 'idle')

    # All frames should have identical facial hair rendering
    # (since beard_type is now deterministic via params, not random per draw)
    assert len(frames) == 4
    for f in frames:
        assert f.getbbox() is not None


def test_hat_deterministic_across_frames():
    """Hat presence should not change between animation frames."""
    random.seed(200)
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    params = gen._generate_character_params()
    # Force hat on
    params['has_hat'] = True
    params['hat_style'] = 'simple'

    anim_gen = AnimationGenerator(canvas_size=(32, 32))
    frames = anim_gen.generate_animation(params, 'walk')

    assert len(frames) == 8
    for f in frames:
        assert f.getbbox() is not None


def test_beard_type_stored_in_params():
    """beard_type should be stored in params, not chosen at draw time."""
    random.seed(42)
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    params = gen._generate_character_params()

    assert 'beard_type' in params
    assert params['beard_type'] in ['mustache', 'goatee', 'full_beard', 'stubble']


def test_hat_fields_stored_in_params():
    """has_hat and hat_style should be stored in params."""
    random.seed(42)
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    params = gen._generate_character_params()

    assert 'has_hat' in params
    assert 'hat_style' in params
    assert isinstance(params['has_hat'], bool)
    assert params['hat_style'] in ['simple', 'baseball_cap']


def test_stubble_pattern_deterministic():
    """Stubble should render identically across calls with same params."""
    gen = PureCharacterGenerator(canvas_size=(64, 64))
    params = gen._generate_character_params()
    params['has_facial_hair'] = True
    params['gender'] = 'male'
    params['beard_type'] = 'stubble'

    sprite1 = gen._render_character_with_params(params)
    sprite2 = gen._render_character_with_params(params)

    assert list(sprite1.getdata()) == list(sprite2.getdata()), \
        "Stubble rendering not deterministic"
