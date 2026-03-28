"""Tests for background removal engine."""

import numpy as np
from PIL import Image
from app.utils.bg_removal import remove_background


def test_solid_color_background_fully_removed():
    """A solid-color background with a distinct subject should be fully removed."""
    # Create 64x64 image: white background, red square in center
    img = Image.new('RGB', (64, 64), (255, 255, 255))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 44, 44], fill=(255, 0, 0))

    result = remove_background(img, threshold_offset=10.0)
    arr = np.array(result)

    # Background pixels (corners) should be transparent
    assert arr[0, 0, 3] == 0, "Top-left corner should be transparent"
    assert arr[63, 63, 3] == 0, "Bottom-right corner should be transparent"

    # Subject pixels (center) should be opaque
    assert arr[32, 32, 3] == 255, "Center (subject) should be opaque"


def test_preserves_subject():
    """Subject area should remain intact."""
    # Use larger image so border samples don't overlap with subject
    img = Image.new('RGB', (128, 128), (0, 0, 200))  # Blue background
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 88, 88], fill=(200, 50, 50))  # Red subject

    result = remove_background(img, threshold_offset=10.0, border_samples=5)
    arr = np.array(result)

    # Subject should be opaque and have correct color
    assert arr[64, 64, 3] == 255
    assert arr[64, 64, 0] == 200  # Red channel


def test_rgba_input():
    """Should handle RGBA input images."""
    img = Image.new('RGBA', (32, 32), (255, 255, 255, 255))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, 24, 24], fill=(0, 128, 0, 255))

    result = remove_background(img)
    assert result.mode == 'RGBA'
    arr = np.array(result)
    assert arr[0, 0, 3] == 0  # Background transparent


def test_empty_image():
    """Uniform image should become fully transparent."""
    img = Image.new('RGB', (16, 16), (128, 128, 128))
    result = remove_background(img)
    arr = np.array(result)
    # All pixels are the same as border - should be removed
    assert np.all(arr[:, :, 3] == 0)
