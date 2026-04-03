"""
Faction-specific sprite generators for the Rotborn Recursion Engine.

Each faction produces distinct visual styles based on their lore:
- Purified: Emaciated, hollow, lobotomized
- Rotborn: Bloated, mutated, ecstatic
- Architects: Uncanny valley, too-normal, flickering
- System: Thin, neural-visible, spore-implanted
"""

from .purified_generator import PurifiedGenerator
from .rotborn_generator import RotbornGenerator
from .architects_generator import ArchitectsGenerator
from .system_generator import SystemGenerator

__all__ = [
    "PurifiedGenerator",
    "RotbornGenerator",
    "ArchitectsGenerator",
    "SystemGenerator",
]

FACTION_GENERATORS = {
    "purified": PurifiedGenerator,
    "rotborn": RotbornGenerator,
    "architects": ArchitectsGenerator,
    "system": SystemGenerator,
}


def get_faction_generator(faction: str, canvas_size=(32, 32)):
    """Get a faction generator by name."""
    cls = FACTION_GENERATORS.get(faction.lower())
    if cls is None:
        raise ValueError(f"Unknown faction: {faction}. Choose from: {list(FACTION_GENERATORS.keys())}")
    return cls(canvas_size=canvas_size)
