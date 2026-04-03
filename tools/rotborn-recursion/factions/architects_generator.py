#!/usr/bin/env python3
"""
DELUSION ARCHITECTS FACTION GENERATOR
======================================

"We do not deny the rot. We curate it."

The Architects are the most unsettling faction because they look
almost normal. Uncanny valley. Something is slightly wrong but
you can't place it. That's the point.

Bodies: Normal... too normal. Uncanny valley.
Faces: Tired, knowing, slightly wrong
Hair: Graying, patchy (from stress)
Clothes: Simple robes, consent contracts visible
Colors: Agreement-gray, memory-blue, fiction-gold
"""

import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from PIL import Image, ImageDraw
from typing import Dict, Optional, Tuple

from generator.pure_generator import PureCharacterGenerator
from generator.broken_proportions import choose_proportions, apply_proportions_to_params
from generator.anomaly_injector import maybe_inject_anomaly
from generator.rotborn_palettes import get_palette


class ArchitectsGenerator:
    """Generates Delusion Architects faction sprites.
    
    The Architects look almost normal. That's what makes them wrong.
    Their sprites have subtle uncanny valley effects — slightly off
    proportions, colors that are almost right but not quite.
    """

    FACTION = "architects"

    # Architect-specific colors — muted, institutional
    ROBE_COLORS = [
        (148, 148, 152),  # Agreement-gray
        (135, 138, 145),  # Memory-blue-gray
        (158, 155, 148),  # Faded consensus
        (128, 132, 138),  # Deep gray
        (165, 162, 155),  # Pale agreement
    ]

    GOLD_ACCENT = (168, 148, 88, 180)   # Fiction-gold (muted)
    BLUE_ACCENT = (88, 108, 148, 160)   # Memory-blue

    def __init__(self, canvas_size: Tuple[int, int] = (32, 32)):
        self.canvas_size = canvas_size
        self.width, self.height = canvas_size
        self.scale = min(self.width, self.height) / 32.0
        self._base_gen = PureCharacterGenerator(canvas_size=canvas_size, palette="bruised")

    def _s(self, value: float) -> int:
        return max(1, int(value * self.scale))

    def generate(self, seed: Optional[int] = None, role: Optional[str] = None) -> Image.Image:
        """Generate an Architects faction sprite.
        
        Args:
            seed: Deterministic seed
            role: Role (archivist/curator/enforcer/citizen)
        
        Returns:
            RGBA PIL Image
        """
        rng = random.Random(seed) if seed is not None else random.Random()

        if role is None:
            role = rng.choice(["citizen", "citizen", "citizen", "archivist", "curator", "enforcer"])

        params = self._generate_architects_params(rng, role)
        sprite = self._base_gen._render_character_with_params(params)
        sprite = self._apply_architects_markings(sprite, params, rng, role)

        # Low anomaly rate — Architects maintain the illusion of normalcy
        sprite, anomaly = maybe_inject_anomaly(sprite, rate=0.04, rng=rng)

        return sprite

    def generate_batch(self, count: int, seed: Optional[int] = None) -> list:
        """Generate multiple Architects sprites."""
        results = []
        base_seed = seed if seed is not None else random.randint(0, 2**31)
        for i in range(count):
            results.append(self.generate(seed=base_seed + i))
        return results

    def _generate_architects_params(self, rng: random.Random, role: str) -> Dict:
        """Generate character params with Architects-specific overrides."""
        random.seed(rng.randint(0, 2**31))
        params = self._base_gen._generate_character_params()

        params["has_hat"] = False
        params["has_jewelry"] = rng.random() < 0.1  # Minimal jewelry

        # Hair: graying, patchy
        if params["gender"] == "male":
            params["hair_style"] = rng.choice(["short", "styled_short", "side_part", "buzzcut"])
        else:
            params["hair_style"] = rng.choice(["bob", "neat_ponytail", "basic_short"])

        # Institutional robes
        robe_color = rng.choice(self.ROBE_COLORS)
        params["clothing"] = {
            "top_style": "institutional",
            "bottom_style": "institutional",
            "top_color": robe_color,
            "bottom_color": robe_color,
        }

        # Architects use mixed proportions — they look almost normal
        proportions = choose_proportions(faction="architects", rng=rng)
        params = apply_proportions_to_params(params, proportions)

        params["_faction"] = self.FACTION
        params["_role"] = role
        return params

    def _apply_architects_markings(self, sprite: Image.Image, params: Dict,
                                    rng: random.Random, role: str) -> Image.Image:
        """Apply Architects-specific visual markings."""
        draw = ImageDraw.Draw(sprite)
        w, h = sprite.size
        s = self._s

        if role in ("archivist", "curator"):
            # Small gold accent mark (contract seal)
            ax = rng.randint(w // 3, 2 * w // 3)
            ay = h // 2 + s(3)
            draw.point((ax, ay), fill=self.GOLD_ACCENT)
            if s(1) > 1:
                draw.ellipse([ax - 1, ay - 1, ax + 1, ay + 1], fill=self.GOLD_ACCENT)

        if role == "enforcer":
            # Blue memory-mark on shoulder area
            sx = w // 2 + rng.choice([-1, 1]) * s(5)
            sy = h // 3
            draw.ellipse([sx - s(1), sy - s(1), sx + s(1), sy + s(1)], fill=self.BLUE_ACCENT)

        return sprite
