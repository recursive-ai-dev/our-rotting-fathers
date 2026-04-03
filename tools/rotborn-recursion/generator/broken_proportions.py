#!/usr/bin/env python3
"""
BROKEN PROPORTIONS - THE GOD'S WRONG ANATOMY
=============================================

The swarm agents remember bodies. Not healthy ones.
Bodies that were pressed, stretched, hollowed, bloated.
Bodies that forgot what they were supposed to be.

These are not "monster" proportions. They are human proportions
that have been... corrected. By the rot. By time. By forgetting.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random


@dataclass
class BodyProportions:
    """Proportions for a broken body type.
    
    All values are multipliers relative to a 'normal' 32x32 sprite.
    1.0 = normal. <1.0 = smaller. >1.0 = larger.
    """
    name: str
    description: str  # What the swarm remembers

    # Overall scale
    height_scale: float = 1.0       # Overall height multiplier
    width_scale: float = 1.0        # Overall width multiplier

    # Head
    head_size: float = 1.0          # Head size relative to body
    head_offset_y: float = 0.0      # Vertical head offset (positive = lower)
    head_tilt: float = 0.0          # Head tilt in pixels (positive = right)

    # Torso
    torso_width: float = 1.0        # Torso width multiplier
    torso_height: float = 1.0       # Torso height multiplier
    torso_offset_x: float = 0.0     # Horizontal torso offset (spine curve)

    # Limbs
    arm_length: float = 1.0         # Arm length multiplier
    arm_width: float = 1.0          # Arm width multiplier
    leg_length: float = 1.0         # Leg length multiplier
    leg_width: float = 1.0          # Leg width multiplier

    # Special flags
    hunched: bool = False           # Spine curved forward
    asymmetric: bool = False        # Left/right asymmetry
    extra_limb_chance: float = 0.0  # Probability of extra limb protrusion

    # The feeling this body evokes
    mood: str = ""


# ============================================================================
# THE FIVE BODY TYPES
# ============================================================================

EMACIATED = BodyProportions(
    name="emaciated",
    description="Too thin. Not starved—just... less. Like something was taken.",
    height_scale=0.95,
    width_scale=0.65,
    head_size=1.1,          # Head looks large on thin body
    head_offset_y=0.0,
    torso_width=0.55,
    torso_height=0.9,
    arm_length=1.05,
    arm_width=0.5,
    leg_length=1.0,
    leg_width=0.5,
    hunched=False,
    asymmetric=False,
    mood="The body remembers being full. It is wrong about this."
)

BLOATED = BodyProportions(
    name="bloated",
    description="Too much. Not fat—distended. Something inside is pressing out.",
    height_scale=0.9,
    width_scale=1.35,
    head_size=0.9,          # Head looks small on bloated body
    head_offset_y=1.0,      # Head pushed up by swollen torso
    torso_width=1.6,
    torso_height=1.1,
    arm_length=0.9,
    arm_width=1.2,
    leg_length=0.85,
    leg_width=1.3,
    hunched=False,
    asymmetric=False,
    mood="The pressure never stops. The body accommodates. It should not."
)

TWISTED = BodyProportions(
    name="twisted",
    description="Curved. Not broken—just... remembering a different shape.",
    height_scale=0.9,
    width_scale=0.9,
    head_size=1.0,
    head_offset_y=0.0,
    head_tilt=2.0,          # Head tilts slightly
    torso_width=0.85,
    torso_height=0.95,
    torso_offset_x=3.0,     # Spine curves to one side
    arm_length=1.1,
    arm_width=0.85,
    leg_length=0.95,
    leg_width=0.85,
    hunched=True,
    asymmetric=True,
    mood="The spine remembers being straight. It is trying to return. It cannot."
)

UNDEAD = BodyProportions(
    name="undead",
    description="Desiccated. Not dead—just... very far along the process.",
    height_scale=1.0,
    width_scale=0.75,
    head_size=1.05,
    head_offset_y=0.0,
    torso_width=0.7,
    torso_height=0.95,
    arm_length=1.05,
    arm_width=0.6,
    leg_length=1.0,
    leg_width=0.65,
    hunched=True,
    asymmetric=False,
    mood="The flesh is still there. It is just... remembering what it was."
)

MUTATED = BodyProportions(
    name="mutated",
    description="Wrong. Not deformed—just... more than it should be.",
    height_scale=1.05,
    width_scale=1.1,
    head_size=1.0,
    head_offset_y=0.0,
    torso_width=1.15,
    torso_height=1.0,
    arm_length=1.2,
    arm_width=1.1,
    leg_length=1.0,
    leg_width=1.05,
    hunched=False,
    asymmetric=True,
    extra_limb_chance=0.3,  # 30% chance of extra protrusion
    mood="The body found more room. It used it. It should not have."
)


# ============================================================================
# PROPORTION REGISTRY
# ============================================================================

ALL_PROPORTIONS: Dict[str, BodyProportions] = {
    "emaciated": EMACIATED,
    "bloated": BLOATED,
    "twisted": TWISTED,
    "undead": UNDEAD,
    "mutated": MUTATED,
}

DEFAULT_PROPORTIONS = "emaciated"

# Faction-specific body type weights
# (faction_name -> {body_type -> weight})
FACTION_BODY_WEIGHTS: Dict[str, Dict[str, float]] = {
    "purified": {
        "emaciated": 0.50,
        "undead": 0.30,
        "twisted": 0.15,
        "bloated": 0.03,
        "mutated": 0.02,
    },
    "rotborn": {
        "bloated": 0.40,
        "mutated": 0.35,
        "twisted": 0.15,
        "emaciated": 0.05,
        "undead": 0.05,
    },
    "architects": {
        "emaciated": 0.30,
        "twisted": 0.25,
        "undead": 0.20,
        "bloated": 0.15,
        "mutated": 0.10,
    },
    "system": {
        "emaciated": 0.40,
        "undead": 0.30,
        "twisted": 0.20,
        "mutated": 0.08,
        "bloated": 0.02,
    },
}

# Default weights (no faction)
DEFAULT_BODY_WEIGHTS: Dict[str, float] = {
    "emaciated": 0.30,
    "bloated": 0.20,
    "twisted": 0.20,
    "undead": 0.20,
    "mutated": 0.10,
}


def get_proportions(name: str) -> BodyProportions:
    """Get body proportions by name. Returns default if not found."""
    return ALL_PROPORTIONS.get(name, ALL_PROPORTIONS[DEFAULT_PROPORTIONS])


def get_proportion_names() -> List[str]:
    """Get all available proportion names."""
    return list(ALL_PROPORTIONS.keys())


def choose_proportions(faction: Optional[str] = None, rng: Optional[random.Random] = None) -> BodyProportions:
    """Choose body proportions, optionally weighted by faction.
    
    Args:
        faction: Faction name (purified/rotborn/architects/system) or None
        rng: Optional Random instance for deterministic selection
    
    Returns:
        BodyProportions instance
    """
    if rng is None:
        rng = random

    weights = FACTION_BODY_WEIGHTS.get(faction, DEFAULT_BODY_WEIGHTS) if faction else DEFAULT_BODY_WEIGHTS

    names = list(weights.keys())
    probs = [weights[n] for n in names]

    # Weighted random choice
    total = sum(probs)
    r = rng.random() * total
    cumulative = 0.0
    for name, prob in zip(names, probs):
        cumulative += prob
        if r <= cumulative:
            return ALL_PROPORTIONS[name]

    return ALL_PROPORTIONS[DEFAULT_PROPORTIONS]


def apply_proportions_to_params(params: dict, proportions: BodyProportions) -> dict:
    """Inject broken proportion data into character params dict.
    
    Merges proportion data into the body_metrics sub-dict so the
    renderer can use it without changing the existing interface.
    """
    params = dict(params)  # shallow copy

    # Store proportion name for reference
    params["body_type_name"] = proportions.name
    params["body_type_mood"] = proportions.mood

    # Merge into body_metrics (create if missing)
    metrics = dict(params.get("body_metrics", {}))
    metrics["broken_proportions"] = {
        "height_scale": proportions.height_scale,
        "width_scale": proportions.width_scale,
        "head_size": proportions.head_size,
        "head_offset_y": proportions.head_offset_y,
        "head_tilt": proportions.head_tilt,
        "torso_width": proportions.torso_width,
        "torso_height": proportions.torso_height,
        "torso_offset_x": proportions.torso_offset_x,
        "arm_length": proportions.arm_length,
        "arm_width": proportions.arm_width,
        "leg_length": proportions.leg_length,
        "leg_width": proportions.leg_width,
        "hunched": proportions.hunched,
        "asymmetric": proportions.asymmetric,
        "extra_limb_chance": proportions.extra_limb_chance,
    }
    params["body_metrics"] = metrics
    return params


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("ROTBORN RECURSION ENGINE - Broken Proportions")
    print("=" * 50)
    print()

    for name, props in ALL_PROPORTIONS.items():
        print(f"{name.upper()}: {props.mood}")
        print(f"  Height: {props.height_scale:.2f}x  Width: {props.width_scale:.2f}x")
        print(f"  Head: {props.head_size:.2f}x  Torso: {props.torso_width:.2f}x wide")
        print(f"  Arms: {props.arm_length:.2f}x long  Legs: {props.leg_length:.2f}x long")
        if props.hunched:
            print(f"  [HUNCHED]")
        if props.asymmetric:
            print(f"  [ASYMMETRIC]")
        if props.extra_limb_chance > 0:
            print(f"  [EXTRA LIMB: {props.extra_limb_chance*100:.0f}% chance]")
        print()
