"""Tests for 4-directional rendering."""

import random
from PIL import Image
from generator.pure_generator import PureCharacterGenerator
from generator.direction_renderer import Direction, DirectionRenderer


def _make_params():
    random.seed(42)
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    return gen._generate_character_params()


def test_all_directions_produce_correct_size():
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    params = _make_params()
    for d in Direction:
        sprite = gen._render_character_with_params(params, direction=d)
        assert sprite.size == (32, 32), f"{d.value}: got {sprite.size}"


def test_all_directions_non_empty():
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    params = _make_params()
    for d in Direction:
        sprite = gen._render_character_with_params(params, direction=d)
        assert sprite.getbbox() is not None, f"{d.value}: empty image"


def test_right_mirrors_left():
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    params = _make_params()
    left = gen._render_character_with_params(params, direction=Direction.LEFT)
    right = gen._render_character_with_params(params, direction=Direction.RIGHT)
    expected_right = left.transpose(Image.FLIP_LEFT_RIGHT)
    assert list(right.getdata()) == list(expected_right.getdata())


def test_directions_at_64x64():
    gen = PureCharacterGenerator(canvas_size=(64, 64))
    random.seed(99)
    params = gen._generate_character_params()
    for d in Direction:
        sprite = gen._render_character_with_params(params, direction=d)
        assert sprite.size == (64, 64)
        assert sprite.getbbox() is not None


def test_down_matches_front_view():
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    params = _make_params()
    # DOWN should use existing draw methods, not direction renderer
    down = gen._render_character_with_params(params, direction=Direction.DOWN)
    front = gen._render_character_with_params(params)  # default is DOWN
    assert list(down.getdata()) == list(front.getdata())
