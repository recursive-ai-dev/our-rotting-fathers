"""Tests for anomaly injection - the Memory-Agent's special ability."""

import random
import pytest
from PIL import Image, ImageDraw

from generator.anomaly_injector import (
    maybe_inject_anomaly, ANOMALIES, ANOMALY_NAMES,
    DEFAULT_ANOMALY_RATE,
)


def _make_test_sprite(size=(32, 32)) -> Image.Image:
    """Create a minimal test sprite with head and torso."""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    # Head
    draw.ellipse([w//4, h//8, 3*w//4, h//2], fill=(142, 128, 118, 255))
    # Torso
    draw.rectangle([w//4 + 2, h//2, 3*w//4 - 2, 7*h//8], fill=(88, 82, 72, 255))
    return img


def test_anomaly_rate_default():
    assert DEFAULT_ANOMALY_RATE == 0.05


def test_at_least_nine_anomaly_types():
    assert len(ANOMALIES) >= 9


def test_all_anomaly_names_unique():
    assert len(ANOMALY_NAMES) == len(set(ANOMALY_NAMES))


def test_no_anomaly_when_rate_zero():
    sprite = _make_test_sprite()
    rng = random.Random(42)
    result, name = maybe_inject_anomaly(sprite, rate=0.0, rng=rng)
    assert name is None
    assert result is sprite  # Same object returned


def test_anomaly_always_injected_at_rate_one():
    sprite = _make_test_sprite()
    rng = random.Random(42)
    result, name = maybe_inject_anomaly(sprite, rate=1.0, rng=rng)
    assert name is not None
    assert name in ANOMALY_NAMES


def test_each_anomaly_produces_valid_image():
    """Every anomaly type should produce a valid RGBA image."""
    sprite = _make_test_sprite()
    rng = random.Random(99)
    for anomaly in ANOMALIES:
        result, name = maybe_inject_anomaly(sprite, rate=1.0, rng=rng, force_anomaly=anomaly.name)
        assert result is not None, f"{anomaly.name}: returned None"
        assert result.size == sprite.size, f"{anomaly.name}: size changed"
        assert result.mode == 'RGBA', f"{anomaly.name}: mode changed"


def test_anomaly_injection_rate_approximately_five_percent():
    """Over 1000 trials, anomaly rate should be ~5% (within 2%)."""
    sprite = _make_test_sprite()
    rng = random.Random(12345)
    injected = 0
    trials = 1000
    for _ in range(trials):
        _, name = maybe_inject_anomaly(sprite, rate=DEFAULT_ANOMALY_RATE, rng=rng)
        if name is not None:
            injected += 1
    rate = injected / trials
    assert 0.03 <= rate <= 0.07, f"Anomaly rate {rate:.3f} outside expected 3-7% range"


def test_force_anomaly_by_name():
    sprite = _make_test_sprite()
    rng = random.Random(1)
    for name in ANOMALY_NAMES:
        result, injected_name = maybe_inject_anomaly(sprite, rate=0.0, rng=rng, force_anomaly=name)
        assert injected_name == name, f"Expected {name}, got {injected_name}"


def test_anomaly_does_not_crash_on_tiny_sprite():
    """Anomalies should not crash on very small sprites."""
    sprite = _make_test_sprite(size=(8, 8))
    rng = random.Random(42)
    for anomaly in ANOMALIES:
        result, _ = maybe_inject_anomaly(sprite, rate=1.0, rng=rng, force_anomaly=anomaly.name)
        assert result is not None


def test_anomaly_preserves_image_mode():
    sprite = _make_test_sprite()
    rng = random.Random(7)
    result, _ = maybe_inject_anomaly(sprite, rate=1.0, rng=rng)
    assert result.mode == 'RGBA'


def test_anomaly_names_are_strings():
    for anomaly in ANOMALIES:
        assert isinstance(anomaly.name, str)
        assert len(anomaly.name) > 0
        assert isinstance(anomaly.description, str)
