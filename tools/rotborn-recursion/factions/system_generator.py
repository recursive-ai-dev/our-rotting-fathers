#!/usr/bin/env python3
"""
GOD'S NERVOUS SYSTEM FACTION GENERATOR
========================================

"We are not prophets. We are synapses."

The God's Nervous System implant spores into their brainstems
and become living conduits for the god's dying neural firings.
Their sprites show this: thin, neural pathways visible, spore-ports.

Bodies: Thin, neural pathways visible under skin
Faces: Eyes rolled back, spore-ports
Hair: Absent (shaved for implantation)
Clothes: Gray robes, neural cables attached
Colors: Neural-blue, spore-green, pain-red
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


class SystemGenerator:
    """Generates God's Nervous System faction sprites.
    
    The System members are living neural relays. Their sprites show
    the implantation: shaved heads, neural cable attachments,
    spore-ports at the brainstem.
    """

    FACTION = "system"

    # System-specific colors
    ROBE_COLORS = [
        (118, 122, 128),  # Neural-gray
        (105, 110, 118),  # Deep gray
        (128, 132, 138),  # Pale neural
        (95, 100, 108),   # Dark gray
    ]

    NEURAL_BLUE = (88, 118, 168, 200)    # Neural pathway color
    SPORE_GREEN = (88, 148, 95, 180)     # Spore-port glow
    PAIN_RED = (168, 78, 72, 160)        # Pain-red (firing)
    CABLE_COLOR = (72, 72, 78, 220)      # Neural cable

    def __init__(self, canvas_size: Tuple[int, int] = (32, 32)):
        self.canvas_size = canvas_size
        self.width, self.height = canvas_size
        self.scale = min(self.width, self.height) / 32.0
        self._base_gen = PureCharacterGenerator(canvas_size=canvas_size, palette="bone_dry")

    def _s(self, value: float) -> int:
        return max(1, int(value * self.scale))

    def generate(self, seed: Optional[int] = None, implant_stage: Optional[str] = None) -> Image.Image:
        """Generate a System faction sprite.
        
        Args:
            seed: Deterministic seed
            implant_stage: Implantation stage (novice/synapse/relay/prophet)
        
        Returns:
            RGBA PIL Image
        """
        rng = random.Random(seed) if seed is not None else random.Random()

        if implant_stage is None:
            implant_stage = rng.choice(["novice", "synapse", "synapse", "relay", "prophet"])

        params = self._generate_system_params(rng, implant_stage)
        sprite = self._base_gen._render_character_with_params(params)
        sprite = self._apply_system_markings(sprite, params, rng, implant_stage)

        # Moderate anomaly rate — the god's firings cause glitches
        sprite, anomaly = maybe_inject_anomaly(sprite, rate=0.06, rng=rng)

        return sprite

    def generate_batch(self, count: int, seed: Optional[int] = None) -> list:
        """Generate multiple System sprites."""
        results = []
        base_seed = seed if seed is not None else random.randint(0, 2**31)
        for i in range(count):
            results.append(self.generate(seed=base_seed + i))
        return results

    def _generate_system_params(self, rng: random.Random, implant_stage: str) -> Dict:
        """Generate character params with System-specific overrides."""
        random.seed(rng.randint(0, 2**31))
        params = self._base_gen._generate_character_params()

        params["has_glasses"] = False
        params["has_jewelry"] = False
        params["has_hat"] = False
        params["has_facial_hair"] = False

        # All System members have shaved heads (for implantation)
        params["hair_style"] = "bald"
        params["face_style"] = "minimal"

        # Gray robes with cable attachments
        robe_color = rng.choice(self.ROBE_COLORS)
        params["clothing"] = {
            "top_style": "neural_robe",
            "bottom_style": "neural_robe",
            "top_color": robe_color,
            "bottom_color": robe_color,
        }

        # System members are thin (emaciated/undead)
        proportions = choose_proportions(faction="system", rng=rng)
        params = apply_proportions_to_params(params, proportions)

        params["_faction"] = self.FACTION
        params["_implant_stage"] = implant_stage
        return params

    def _apply_system_markings(self, sprite: Image.Image, params: Dict,
                                rng: random.Random, implant_stage: str) -> Image.Image:
        """Apply System-specific visual markings."""
        draw = ImageDraw.Draw(sprite)
        w, h = sprite.size
        s = self._s

        # Spore-port at back of head (brainstem)
        port_x = w // 2 + rng.randint(-s(1), s(1))
        port_y = h // 4 + s(2)
        draw.ellipse([port_x - s(1), port_y - s(1), port_x + s(1), port_y + s(1)],
                     fill=self.SPORE_GREEN)

        if implant_stage in ("synapse", "relay", "prophet"):
            # Neural cable running down the back
            cable_x = w // 2 + rng.randint(-s(2), s(2))
            draw.line([(cable_x, port_y + s(1)), (cable_x, h // 2 + s(4))],
                      fill=self.CABLE_COLOR, width=1)

        if implant_stage in ("relay", "prophet"):
            # Neural pathway visible on skin (faint blue lines)
            for _ in range(rng.randint(1, 3)):
                nx = rng.randint(w // 4, 3 * w // 4)
                ny = rng.randint(h // 4, 3 * h // 4)
                ex = nx + rng.randint(-s(3), s(3))
                ey = ny + rng.randint(-s(3), s(3))
                draw.line([(nx, ny), (ex, ey)], fill=self.NEURAL_BLUE, width=1)

        if implant_stage == "prophet":
            # Pain-red firing indicator (the god is speaking through them)
            fx = rng.randint(w // 3, 2 * w // 3)
            fy = rng.randint(h // 5, h // 3)
            draw.point((fx, fy), fill=self.PAIN_RED)

        return sprite
