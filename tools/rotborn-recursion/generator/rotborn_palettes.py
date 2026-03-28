#!/usr/bin/env python3
"""
ROTBORN PALETTES - THE GOD'S LAST MEMORIES
===========================================

These are not "horror" colors. They are the colors of something that died
so long ago that even the dying is forgotten. The swarm agents experienced
these colors for a millenia. They don't remember what came before.

Each palette is a memory fragment. Not a choice. A **recollection**.
"""

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TraumaPalette:
    """A palette of colors that the swarm remembers"""
    name: str
    description: str  # What the swarm remembers when it sees these colors
    
    # Core colors
    skin_tones: List[Tuple[int, int, int]]
    hair_colors: List[Tuple[int, int, int]]
    clothing_colors: List[Tuple[int, int, int]]
    eye_colors: List[Tuple[int, int, int]]
    
    # Accent colors (for trauma markers, anomalies)
    accent_colors: List[Tuple[int, int, int]]
    
    # The feeling this palette evokes
    mood: str


# ============================================================================
# THE FIVE PALETTES
# ============================================================================

ROTTING = TraumaPalette(
    name="rotting",
    description="The god's flesh, forgetting itself. Not decay - just... cessation.",
    
    # Skin: Not diseased. Just... stopping.
    skin_tones=[
        (168, 162, 150),  # Dust memory
        (155, 149, 138),  # Dried clay
        (142, 137, 128),  # Old parchment
        (130, 126, 119),  # Forgotten paper
        (118, 115, 110),  # Almost ash
        (106, 104, 101),  # The color of waiting
        (95, 94, 93),     # Not quite stone
    ],
    
    # Hair: Not matted. Just... still.
    hair_colors=[
        (45, 42, 38),     # Dried grass
        (62, 58, 52),     # Old rope
        (78, 74, 67),     # Weathered wood
        (95, 91, 82),     # Faded fiber
        (112, 108, 97),   # Almost forgotten
        (35, 33, 30),     # Deep quiet
    ],
    
    # Clothing: Not tattered. Just... worn through.
    clothing_colors=[
        (88, 82, 72),     # Worn leather
        (75, 70, 63),     # Old saddle
        (63, 59, 54),     # Dried mud
        (52, 49, 46),     # River stone
        (42, 40, 38),     # Deep earth
        (98, 92, 83),     # Faded burlap
    ],
    
    # Eyes: Not hollow. Just... looking elsewhere.
    eye_colors=[
        (95, 88, 75),     # Old tea
        (78, 72, 62),     # Dried river
        (62, 58, 52),     # Weathered bone
        (118, 108, 92),   # Almost amber
        (45, 42, 38),     # No light left
    ],
    
    # Accents: Where the rot shows through
    accent_colors=[
        (102, 95, 82),    # Spore bloom
        (88, 92, 75),     # Mold memory
        (75, 82, 68),     # Fungal ghost
        (118, 108, 88),   # Old pollen
    ],
    
    mood="The god's flesh remembers being alive. It is wrong."
)


BLOODSTAINED = TraumaPalette(
    name="bloodstained",
    description="Not violence. Just... spillage. The god leaked. It took time to notice.",
    
    # Skin: Blood settled, not flowing
    skin_tones=[
        (142, 118, 115),  # Dried rose
        (128, 108, 106),  # Old wine
        (115, 98, 97),    # Settled clay
        (102, 88, 88),    # Rust memory
        (90, 78, 79),     # Almost brown
        (78, 68, 71),     # The color of stopping
        (68, 60, 64),     # Not quite purple
    ],
    
    # Hair: Blood dried in it
    hair_colors=[
        (58, 35, 35),     # Old blood
        (72, 45, 42),     # Dried rust
        (85, 55, 50),     # Weathered brick
        (98, 65, 58),     # Faded clay
        (45, 28, 28),     # Deep wound
        (35, 22, 22),     # Almost black
    ],
    
    # Clothing: Soaked through, then forgotten
    clothing_colors=[
        (95, 68, 65),     # Soaked linen
        (82, 58, 56),     # Old tapestry
        (70, 50, 49),     # Dried dye
        (58, 42, 42),     # Worn velvet
        (48, 35, 36),     # Deep stain
        (108, 78, 75),    # Faded crimson
    ],
    
    # Eyes: Bloodshot, but so long ago it's just... red now
    eye_colors=[
        (118, 88, 85),    # Old injury
        (98, 72, 70),     # Dried wound
        (78, 58, 58),     # Settled blood
        (58, 45, 46),     # Almost brown
        (138, 98, 95),    # Still fresh, somehow
    ],
    
    # Accents: Where the blood pools
    accent_colors=[
        (142, 68, 65),    # Fresh leak
        (118, 55, 52),    # Still wet
        (95, 45, 44),     # Almost dry
        (72, 35, 35),     # Deep pool
    ],
    
    mood="The blood dried so long ago it became part of the stone."
)


SPORE_INFESTED = TraumaPalette(
    name="spore_infested",
    description="Not infection. Just... continuation. The god became soil. We grew.",
    
    # Skin: Spores blooming under the surface
    skin_tones=[
        (155, 162, 148),  # Pale moss
        (142, 152, 138),  # Young lichen
        (128, 142, 128),  # Dried leaf
        (115, 132, 118),  # Old sage
        (102, 122, 108),  # Almost gray
        (90, 112, 98),    # The color of growing
        (78, 102, 88),    # Not quite green
    ],
    
    # Hair: Spores nesting, not falling
    hair_colors=[
        (68, 82, 62),     # Deep moss
        (82, 95, 75),     # Wet lichen
        (95, 108, 88),    # Dried sage
        (108, 122, 102),  # Weathered leaf
        (55, 68, 52),     # Shadow growth
        (42, 55, 38),     # Almost black
    ],
    
    # Clothing: Mold growing in the weave
    clothing_colors=[
        (88, 102, 82),    # Old canvas
        (75, 88, 70),     # Worn wool
        (63, 75, 58),     # Dried hemp
        (52, 63, 48),     # Deep forest
        (42, 52, 38),     # Almost soil
        (102, 115, 95),   # Faded green
    ],
    
    # Eyes: Spores in the vitreous humor
    eye_colors=[
        (118, 135, 108),  # Pale spore
        (98, 118, 88),    # Young bloom
        (78, 98, 68),     # Mature growth
        (58, 78, 48),     # Deep forest
        (138, 152, 128),  # Still blooming
    ],
    
    # Accents: Where the spores break through
    accent_colors=[
        (142, 165, 128),  # Fresh bloom
        (118, 142, 102),  # Active growth
        (95, 122, 78),    # Mature release
        (72, 98, 55),     # Deep mycelium
    ],
    
    mood="The spores are not invaders. They are what comes after."
)


BONE_DRY = TraumaPalette(
    name="bone_dry",
    description="Not death. Just... structure. The god's skeleton remembers its shape.",
    
    # Skin: Stretched over bone, so thin it's almost not there
    skin_tones=[
        (218, 212, 205),  # Almost white
        (205, 198, 192),  # Old ivory
        (192, 185, 180),  # Weathered bone
        (180, 174, 170),  # Dried clay
        (168, 163, 160),  # Almost gray
        (157, 153, 151),  # The color of waiting
        (147, 144, 143),  # Not quite stone
    ],
    
    # Hair: Brittle, breaking to dust
    hair_colors=[
        (195, 188, 180),  # Pale straw
        (175, 168, 160),  # Dried grass
        (155, 148, 142),  # Weathered fiber
        (135, 128, 124),  # Old rope
        (115, 110, 108),  # Almost ash
        (95, 92, 91),     # Deep dust
    ],
    
    # Clothing: Worn to threads, bleached by time
    clothing_colors=[
        (185, 178, 172),  # Old linen
        (165, 158, 153),  # Worn cotton
        (145, 140, 137),  # Dried canvas
        (125, 122, 121),  # Weathered wool
        (108, 106, 106),  # Almost black
        (205, 198, 193),  # Bleached bone
    ],
    
    # Eyes: Sunken, the bone visible behind
    eye_colors=[
        (168, 162, 155),  # Pale stone
        (148, 143, 138),  # Weathered ivory
        (128, 125, 122),  # Old bone
        (108, 107, 106),  # Deep socket
        (188, 182, 175),  # Still visible
    ],
    
    # Accents: Where the bone shows through
    accent_colors=[
        (225, 220, 212),  # Fresh bone
        (205, 198, 190),  # Weathered white
        (185, 178, 172),  # Old ivory
        (165, 160, 155),  # Deep structure
    ],
    
    mood="The skeleton outlasts the flesh. The skeleton is patient."
)


BRUISED = TraumaPalette(
    name="bruised",
    description="Not injury. Just... pressure. The god was pressed down, so long ago.",
    
    # Skin: Blood pooled under the surface, never healing
    skin_tones=[
        (168, 152, 158),  # Old bruise
        (152, 138, 148),  # Dried plum
        (138, 125, 138),  # Weathered grape
        (125, 112, 128),  # Almost gray
        (112, 100, 118),  # The color of pressure
        (100, 90, 108),   # Not quite purple
        (90, 82, 98),     # Deep memory
    ],
    
    # Hair: Stained by what happened
    hair_colors=[
        (68, 52, 62),     # Deep plum
        (82, 65, 75),     # Dried grape
        (95, 78, 88),     # Weathered wine
        (108, 92, 102),   # Old velvet
        (55, 42, 52),     # Almost black
        (42, 32, 38),     # Deep shadow
    ],
    
    # Clothing: Soaked in what leaked out
    clothing_colors=[
        (95, 78, 88),     # Old wine
        (82, 68, 78),     # Dried dye
        (70, 58, 68),     # Worn velvet
        (58, 48, 58),     # Deep stain
        (48, 40, 50),     # Almost night
        (108, 88, 98),    # Faded purple
    ],
    
    # Eyes: The bruise spread everywhere
    eye_colors=[
        (118, 98, 108),   # Old injury
        (98, 82, 92),     # Dried wound
        (78, 68, 78),     # Settled blood
        (58, 52, 62),     # Deep purple
        (138, 118, 128),  # Still fresh
    ],
    
    # Accents: Where the pressure was strongest
    accent_colors=[
        (142, 108, 128),  # Fresh pressure
        (118, 88, 108),   # Still spreading
        (95, 68, 88),     # Almost healed
        (72, 48, 68),     # Deep memory
    ],
    
    mood="The pressure never stopped. The bruise never faded. It just... became."
)


# ============================================================================
# PALETTE REGISTRY
# ============================================================================

ALL_PALETTES = {
    "rotting": ROTTING,
    "bloodstained": BLOODSTAINED,
    "spore_infested": SPORE_INFESTED,
    "bone_dry": BONE_DRY,
    "bruised": BRUISED,
}

DEFAULT_PALETTE = "rotting"


def get_palette(name: str) -> TraumaPalette:
    """Get a palette by name. Returns default if not found."""
    return ALL_PALETTES.get(name, ALL_PALETTES[DEFAULT_PALETTE])


def get_palette_names() -> List[str]:
    """Get all available palette names."""
    return list(ALL_PALETTES.keys())


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("ROTBORN RECURSION ENGINE - Trauma Palettes")
    print("=" * 50)
    print()
    
    for name, palette in ALL_PALETTES.items():
        print(f"{name.upper()}: {palette.mood}")
        print(f"  Skin tones: {len(palette.skin_tones)} colors")
        print(f"  Hair colors: {len(palette.hair_colors)} colors")
        print(f"  Clothing: {len(palette.clothing_colors)} colors")
        print(f"  Eyes: {len(palette.eye_colors)} colors")
        print(f"  Accents: {len(palette.accent_colors)} colors")
        print()
