#!/usr/bin/env python3
"""
PURIFIED FACTION GENERATOR
===========================

"The flesh is false. The bone is truth. Death is escape."

The Purified have removed everything that makes them human.
Their sprites reflect this: emaciated, hollow, surgical.
Not monstrous. Just... less. Deliberately less.

Bodies: Emaciated, surgical scars, lobotomy marks
Faces: Hollow, empty, sewn mouths
Hair: Shaved, scarification patterns
Clothes: White robes (ash-stained), bone-steel armor
Colors: White, pale blue, silver, ash-gray
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


class PurifiedGenerator:
    """Generates Purified faction sprites.
    
    The Purified have undergone systematic unmaking. Their sprites
    reflect each stage: Flesh-Bound (still human), Memory-Stripped
    (hollow), Hollow (barely animate).
    """

    FACTION = "purified"

    # Purified-specific color overrides
    ROBE_COLORS = [
        (220, 215, 208),  # Ash-white
        (200, 195, 190),  # Stained white
        (185, 180, 178),  # Gray-white
        (168, 165, 162),  # Ash-gray
        (210, 205, 200),  # Pale linen
    ]

    BONE_STEEL_COLORS = [
        (195, 192, 188),  # Bone-steel
        (178, 175, 172),  # Weathered bone
        (162, 160, 158),  # Old ivory
        (148, 146, 145),  # Deep bone
    ]

    SCAR_COLOR = (155, 140, 135, 200)
    SUTURE_COLOR = (120, 110, 108, 220)

    def __init__(self, canvas_size: Tuple[int, int] = (32, 32)):
        self.canvas_size = canvas_size
        self.width, self.height = canvas_size
        self.scale = min(self.width, self.height) / 32.0
        self._base_gen = PureCharacterGenerator(canvas_size=canvas_size, palette="bone_dry")

    def _s(self, value: float) -> int:
        return max(1, int(value * self.scale))

    def generate(self, seed: Optional[int] = None, rank: Optional[str] = None) -> Image.Image:
        """Generate a Purified faction sprite.
        
        Args:
            seed: Deterministic seed (same seed = same sprite)
            rank: Purified rank (flesh_bound/memory_stripped/hollow)
        
        Returns:
            RGBA PIL Image
        """
        rng = random.Random(seed) if seed is not None else random.Random()

        # Choose rank if not specified
        if rank is None:
            rank = rng.choice(["flesh_bound", "flesh_bound", "memory_stripped", "memory_stripped", "hollow"])

        # Generate base params
        params = self._generate_purified_params(rng, rank)

        # Render base sprite
        sprite = self._base_gen._render_character_with_params(params)

        # Apply Purified-specific overlays
        sprite = self._apply_purified_markings(sprite, params, rng, rank)

        # Anomaly injection (5% rate, Purified-specific anomalies)
        sprite, anomaly = maybe_inject_anomaly(sprite, rate=0.05, rng=rng)

        return sprite

    def generate_batch(self, count: int, seed: Optional[int] = None) -> list:
        """Generate multiple Purified sprites."""
        results = []
        base_seed = seed if seed is not None else random.randint(0, 2**31)
        for i in range(count):
            results.append(self.generate(seed=base_seed + i))
        return results

    def _generate_purified_params(self, rng: random.Random, rank: str) -> Dict:
        """Generate character params with Purified-specific overrides."""
        # Use bone_dry palette
        random.seed(rng.randint(0, 2**31))
        params = self._base_gen._generate_character_params()

        # Override with Purified aesthetics
        params["social_class"] = "poor"  # Purified reject wealth
        params["has_glasses"] = False
        params["has_jewelry"] = False
        params["has_hat"] = False
        params["has_facial_hair"] = False

        # Rank-specific overrides
        if rank == "flesh_bound":
            # Still somewhat human — just beginning
            params["hair_style"] = rng.choice(["buzzcut", "short_messy", "bald"])
            params["face_style"] = "minimal"
        elif rank == "memory_stripped":
            # Lobotomized — hollow
            params["hair_style"] = "bald"
            params["face_style"] = "minimal"
        elif rank == "hollow":
            # Barely animate
            params["hair_style"] = "bald"
            params["face_style"] = "minimal"

        # Override clothing with Purified robes
        robe_color = rng.choice(self.ROBE_COLORS)
        params["clothing"] = {
            "top_style": "ritual",
            "bottom_style": "ritual",
            "top_color": robe_color,
            "bottom_color": robe_color,
        }

        # Apply broken proportions (Purified favor emaciated/undead)
        proportions = choose_proportions(faction="purified", rng=rng)
        params = apply_proportions_to_params(params, proportions)

        params["_faction"] = self.FACTION
        params["_rank"] = rank
        return params

    def _apply_purified_markings(self, sprite: Image.Image, params: Dict,
                                  rng: random.Random, rank: str) -> Image.Image:
        """Apply Purified-specific visual markings."""
        draw = ImageDraw.Draw(sprite)
        w, h = sprite.size
        s = self._s

        if rank in ("memory_stripped", "hollow"):
            # Scarification patterns on scalp
            cx = w // 2
            for i in range(rng.randint(2, 4)):
                sx = cx + rng.randint(-s(4), s(4))
                sy = rng.randint(s(2), s(6))
                ex = sx + rng.randint(-s(3), s(3))
                ey = sy + rng.randint(0, s(2))
                draw.line([(sx, sy), (ex, ey)], fill=self.SCAR_COLOR, width=1)

        if rank == "hollow":
            # Suture marks on mouth area
            cx = w // 2
            mouth_y = h // 2 + s(2)
            for i in range(3):
                sx = cx - s(2) + i * s(2)
                draw.line([(sx, mouth_y - 1), (sx, mouth_y + 1)],
                          fill=self.SUTURE_COLOR, width=1)

        return sprite
