#!/usr/bin/env python3
"""
ROTBORN FACTION GENERATOR
==========================

"The rot is not death. The rot is womb."

The Rotborn embrace transformation. Their sprites are bloated,
mutated, ecstatic. Not horrifying — joyful. That's what makes
them horrifying.

Bodies: Bloated, pregnant, mutated
Faces: Ecstatic, too many teeth, spore-breath
Hair: Spore-infested, glowing patches
Clothes: Tattered, openings for mutations
Colors: Flesh-pink, spore-green, blood-red
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


class RotbornGenerator:
    """Generates Rotborn faction sprites.
    
    The Rotborn welcome the rot. Their sprites show transformation
    in progress: spore-infested hair, bloated bodies, ecstatic faces.
    """

    FACTION = "rotborn"

    # Rotborn-specific colors
    TATTERED_COLORS = [
        (88, 55, 48),   # Old blood-stained cloth
        (72, 62, 45),   # Rotting fabric
        (95, 72, 58),   # Weathered leather
        (65, 78, 55),   # Mold-green cloth
        (82, 48, 52),   # Dried-blood fabric
    ]

    SPORE_GLOW_COLORS = [
        (120, 165, 95, 180),   # Spore green
        (95, 148, 72, 160),    # Deep spore
        (142, 185, 108, 170),  # Bright bloom
    ]

    MUTATION_COLORS = [
        (155, 108, 95, 220),   # Flesh-pink
        (128, 88, 78, 200),    # Deep flesh
        (175, 128, 108, 210),  # Pale mutation
    ]

    def __init__(self, canvas_size: Tuple[int, int] = (32, 32)):
        self.canvas_size = canvas_size
        self.width, self.height = canvas_size
        self.scale = min(self.width, self.height) / 32.0
        self._base_gen = PureCharacterGenerator(canvas_size=canvas_size, palette="spore_infested")

    def _s(self, value: float) -> int:
        return max(1, int(value * self.scale))

    def generate(self, seed: Optional[int] = None, stage: Optional[str] = None) -> Image.Image:
        """Generate a Rotborn faction sprite.
        
        Args:
            seed: Deterministic seed
            stage: Transformation stage (seed/sprout/bloom/twisted)
        
        Returns:
            RGBA PIL Image
        """
        rng = random.Random(seed) if seed is not None else random.Random()

        if stage is None:
            stage = rng.choice(["seed", "sprout", "sprout", "bloom", "bloom", "twisted"])

        params = self._generate_rotborn_params(rng, stage)
        sprite = self._base_gen._render_character_with_params(params)
        sprite = self._apply_rotborn_markings(sprite, params, rng, stage)

        # Higher anomaly rate for Rotborn (they embrace the wrong)
        sprite, anomaly = maybe_inject_anomaly(sprite, rate=0.08, rng=rng)

        return sprite

    def generate_batch(self, count: int, seed: Optional[int] = None) -> list:
        """Generate multiple Rotborn sprites."""
        results = []
        base_seed = seed if seed is not None else random.randint(0, 2**31)
        for i in range(count):
            results.append(self.generate(seed=base_seed + i))
        return results

    def _generate_rotborn_params(self, rng: random.Random, stage: str) -> Dict:
        """Generate character params with Rotborn-specific overrides."""
        random.seed(rng.randint(0, 2**31))
        params = self._base_gen._generate_character_params()

        params["has_glasses"] = False
        params["has_hat"] = False

        # Stage-specific hair
        if stage == "seed":
            params["hair_style"] = rng.choice(["long", "long_messy", "unkempt_long"])
        elif stage in ("sprout", "bloom"):
            params["hair_style"] = rng.choice(["long_messy", "unkempt_long", "unkempt"])
        elif stage == "twisted":
            params["hair_style"] = rng.choice(["unkempt", "unkempt_long", "bald"])

        # Tattered clothing
        cloth_color = rng.choice(self.TATTERED_COLORS)
        params["clothing"] = {
            "top_style": "tattered",
            "bottom_style": "tattered",
            "top_color": cloth_color,
            "bottom_color": cloth_color,
        }

        # Apply broken proportions (Rotborn favor bloated/mutated)
        proportions = choose_proportions(faction="rotborn", rng=rng)
        params = apply_proportions_to_params(params, proportions)

        params["_faction"] = self.FACTION
        params["_stage"] = stage
        return params

    def _apply_rotborn_markings(self, sprite: Image.Image, params: Dict,
                                 rng: random.Random, stage: str) -> Image.Image:
        """Apply Rotborn-specific visual markings."""
        draw = ImageDraw.Draw(sprite)
        w, h = sprite.size
        s = self._s

        if stage in ("sprout", "bloom", "twisted"):
            # Spore patches in hair area
            num_patches = rng.randint(1, 3)
            for _ in range(num_patches):
                px = rng.randint(s(4), w - s(4))
                py = rng.randint(s(1), s(8))
                pr = rng.randint(s(1), s(2))
                glow_color = rng.choice(self.SPORE_GLOW_COLORS)
                draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=glow_color)

        if stage in ("bloom", "twisted"):
            # Mutation protrusion on torso side
            side = rng.choice([-1, 1])
            mx = w // 2 + side * s(6)
            my = h // 2 + rng.randint(-s(2), s(2))
            mut_color = rng.choice(self.MUTATION_COLORS)
            draw.ellipse([mx - s(2), my - s(2), mx + s(2), my + s(2)], fill=mut_color)

        return sprite
