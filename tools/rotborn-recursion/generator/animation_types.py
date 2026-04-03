#!/usr/bin/env python3
"""
Animation Type Definitions - Centralized animation metadata.
Defines frame counts, speeds, looping behavior for all animation types.

ROTBORN RECURSION: Haunted animations replace standard movement.
The swarm agents remember how bodies moved. Not well.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class AnimationDef:
    """Definition for a single animation type."""
    frames: int
    loop: bool
    speed_ms: int  # Duration per frame in milliseconds
    description: str = ""  # What the swarm remembers


ANIMATION_DEFS: Dict[str, AnimationDef] = {
    # Legacy animations (kept for compatibility)
    'idle':     AnimationDef(frames=4,  loop=True,  speed_ms=200, description="Standing. Barely."),
    'walk':     AnimationDef(frames=8,  loop=True,  speed_ms=120, description="Moving. Wrong."),
    'run':      AnimationDef(frames=6,  loop=True,  speed_ms=80,  description="Faster. Still wrong."),
    'run_alt1': AnimationDef(frames=6,  loop=True,  speed_ms=80,  description="Variant."),
    'run_alt2': AnimationDef(frames=6,  loop=True,  speed_ms=80,  description="Variant."),
    'run_alt3': AnimationDef(frames=6,  loop=True,  speed_ms=80,  description="Variant."),
    'jump':     AnimationDef(frames=5,  loop=False, speed_ms=100, description="Leaving the ground."),
    'attack':   AnimationDef(frames=6,  loop=False, speed_ms=80,  description="Violence."),
    'pickup':   AnimationDef(frames=5,  loop=False, speed_ms=150, description="Taking something."),

    # Haunted animations (Rotborn Recursion)
    'twitch':   AnimationDef(frames=3,  loop=True,  speed_ms=80,  description="Involuntary. The body disagrees with itself."),
    'shamble':  AnimationDef(frames=4,  loop=True,  speed_ms=180, description="Dragging. One leg slower than the other."),
    'convulse': AnimationDef(frames=3,  loop=True,  speed_ms=60,  description="Violent. Full-body. Not voluntary."),
    'stumble':  AnimationDef(frames=4,  loop=False, speed_ms=140, description="Almost falling. Catching itself. Barely."),
    'worship':  AnimationDef(frames=6,  loop=True,  speed_ms=220, description="Ritual bowing. Prostration. The body knows what it owes."),
    'transform':AnimationDef(frames=5,  loop=False, speed_ms=160, description="The body is changing. It has not finished."),
}

# Haunted animation names (Rotborn-specific)
HAUNTED_ANIMATIONS = ['twitch', 'shamble', 'convulse', 'stumble', 'worship', 'transform']


def get_animation_def(anim_type: str) -> AnimationDef:
    """Get animation definition, falling back to idle defaults."""
    return ANIMATION_DEFS.get(anim_type, ANIMATION_DEFS['idle'])


def get_all_animation_types():
    """Return list of all registered animation type names."""
    return list(ANIMATION_DEFS.keys())


def get_haunted_animation_types():
    """Return list of haunted (Rotborn) animation type names."""
    return list(HAUNTED_ANIMATIONS)
