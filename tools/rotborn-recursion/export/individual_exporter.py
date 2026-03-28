#!/usr/bin/env python3
"""
Individual PNG Exporter - Export each frame as a separate PNG file.
Directory structure: output/{animation_name}/{direction}_{frame:02d}.png
"""

import os
from PIL import Image
from typing import Dict, List
from generator.direction_renderer import Direction


def export_individual_frames(frames_by_direction: Dict[Direction, List[Image.Image]],
                             output_dir: str, animation_name: str) -> List[str]:
    """Export individual PNG frames organized by animation and direction.

    Args:
        frames_by_direction: Dict mapping Direction to frame lists.
        output_dir: Base output directory.
        animation_name: Name of the animation (e.g. 'walk').

    Returns:
        List of all saved file paths.
    """
    anim_dir = os.path.join(output_dir, animation_name)
    os.makedirs(anim_dir, exist_ok=True)

    saved_paths = []
    for direction, frames in frames_by_direction.items():
        for frame_idx, frame in enumerate(frames):
            filename = f"{direction.value}_{frame_idx:02d}.png"
            filepath = os.path.join(anim_dir, filename)
            frame.save(filepath, "PNG")
            saved_paths.append(filepath)

    return saved_paths


def export_single_direction_frames(frames: List[Image.Image], output_dir: str,
                                   animation_name: str, direction: Direction) -> List[str]:
    """Export frames for a single direction.

    Args:
        frames: List of frame Images.
        output_dir: Base output directory.
        animation_name: Animation type name.
        direction: The direction being exported.

    Returns:
        List of saved file paths.
    """
    anim_dir = os.path.join(output_dir, animation_name)
    os.makedirs(anim_dir, exist_ok=True)

    saved_paths = []
    for frame_idx, frame in enumerate(frames):
        filename = f"{direction.value}_{frame_idx:02d}.png"
        filepath = os.path.join(anim_dir, filename)
        frame.save(filepath, "PNG")
        saved_paths.append(filepath)

    return saved_paths
