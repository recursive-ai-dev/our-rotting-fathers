"""Tests for the export system."""

import os
import random
import tempfile
from PIL import Image

from generator.pure_generator import PureCharacterGenerator
from generator.animation_generator import AnimationGenerator
from generator.direction_renderer import Direction
from generator.animation_types import ANIMATION_DEFS
from export.sheet_builder import build_rpg_sheet, build_single_direction_sheet
from export.apng_exporter import export_apng
from export.individual_exporter import export_individual_frames


def _make_animation_frames():
    random.seed(42)
    gen = PureCharacterGenerator(canvas_size=(32, 32))
    params = gen._generate_character_params()
    anim_gen = AnimationGenerator(canvas_size=(32, 32))

    frames_by_dir = {}
    for d in Direction:
        frames_by_dir[d] = anim_gen.generate_animation(params, 'walk', direction=d)
    return frames_by_dir


def test_rpg_sheet_dimensions():
    """RPG Maker sheet should be (frame_width * max_frames) x (frame_height * 4)."""
    frames_by_dir = _make_animation_frames()
    max_frames = max(len(f) for f in frames_by_dir.values())

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        path = f.name

    try:
        build_rpg_sheet(frames_by_dir, path)
        sheet = Image.open(path)
        assert sheet.size == (32 * max_frames, 32 * 4), f"Got {sheet.size}"
    finally:
        os.unlink(path)


def test_apng_valid():
    """APNG should be a valid file."""
    frames = [Image.new('RGBA', (32, 32), (255, 0, 0, 255)),
              Image.new('RGBA', (32, 32), (0, 255, 0, 255)),
              Image.new('RGBA', (32, 32), (0, 0, 255, 255))]

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        path = f.name

    try:
        export_apng(frames, path, duration_ms=100)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

        # Should be loadable as PNG
        img = Image.open(path)
        assert img.size == (32, 32)
    finally:
        os.unlink(path)


def test_individual_png_counts():
    """Individual export should create correct number of files."""
    frames_by_dir = _make_animation_frames()

    with tempfile.TemporaryDirectory() as tmpdir:
        paths = export_individual_frames(frames_by_dir, tmpdir, 'walk')

        expected_count = sum(len(f) for f in frames_by_dir.values())
        assert len(paths) == expected_count, \
            f"Expected {expected_count} files, got {len(paths)}"

        # Check directory structure
        walk_dir = os.path.join(tmpdir, 'walk')
        assert os.path.isdir(walk_dir)

        # Check file naming
        for p in paths:
            assert p.endswith('.png')
            assert os.path.exists(p)


def test_single_direction_sheet():
    """Single direction sheet should have correct width."""
    frames = [Image.new('RGBA', (32, 32), (255, 0, 0, 255))] * 6

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        path = f.name

    try:
        build_single_direction_sheet(frames, path, horizontal=True)
        sheet = Image.open(path)
        assert sheet.size == (32 * 6, 32)
    finally:
        os.unlink(path)
