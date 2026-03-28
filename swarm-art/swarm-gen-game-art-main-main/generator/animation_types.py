#!/usr/bin/env python3
"""
Animation Type Definitions - Centralized animation metadata.
Defines frame counts, speeds, looping behavior for all animation types.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class AnimationDef:
    """Definition for a single animation type."""
    frames: int
    loop: bool
    speed_ms: int  # Duration per frame in milliseconds


ANIMATION_DEFS: Dict[str, AnimationDef] = {
    'idle':     AnimationDef(frames=4,  loop=True,  speed_ms=200),
    'walk':     AnimationDef(frames=8,  loop=True,  speed_ms=120),
    'run':      AnimationDef(frames=6,  loop=True,  speed_ms=80),
    'run_alt1': AnimationDef(frames=6,  loop=True,  speed_ms=80),
    'run_alt2': AnimationDef(frames=6,  loop=True,  speed_ms=80),
    'run_alt3': AnimationDef(frames=6,  loop=True,  speed_ms=80),
    'jump':     AnimationDef(frames=5,  loop=False, speed_ms=100),
    'attack':   AnimationDef(frames=6,  loop=False, speed_ms=80),
    'pickup':   AnimationDef(frames=5,  loop=False, speed_ms=150),
}


def get_animation_def(anim_type: str) -> AnimationDef:
    """Get animation definition, falling back to idle defaults."""
    return ANIMATION_DEFS.get(anim_type, ANIMATION_DEFS['idle'])


def get_all_animation_types():
    """Return list of all registered animation type names."""
    return list(ANIMATION_DEFS.keys())
