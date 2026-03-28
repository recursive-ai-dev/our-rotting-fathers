#!/usr/bin/env python3
"""
APNG Exporter - Export animated PNG files using Pillow's native APNG support.
"""

from PIL import Image
from typing import Dict, List, Optional
from generator.direction_renderer import Direction


def export_apng(frames: List[Image.Image], output_path: str,
                duration_ms: int = 100, loop: int = 0) -> str:
    """Export frames as an APNG (Animated PNG).

    Args:
        frames: List of PIL Image frames (RGBA).
        output_path: Path to save the APNG file.
        duration_ms: Duration per frame in milliseconds.
        loop: Number of loops (0 = infinite).

    Returns:
        The output_path on success, empty string on failure.
    """
    if not frames:
        return ""

    frames[0].save(
        output_path,
        format='PNG',
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=loop,
    )
    return output_path


def export_apng_per_direction(frames_by_direction: Dict[Direction, List[Image.Image]],
                              output_dir: str, animation_name: str,
                              duration_ms: int = 100, loop: int = 0) -> List[str]:
    """Export one APNG per direction.

    Args:
        frames_by_direction: Dict mapping Direction to frame lists.
        output_dir: Directory to save files in.
        animation_name: Base name for the animation (e.g. 'walk').
        duration_ms: Duration per frame.
        loop: Loop count.

    Returns:
        List of output file paths.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    paths = []
    for direction, frames in frames_by_direction.items():
        path = os.path.join(output_dir, f"{animation_name}_{direction.value}.apng")
        export_apng(frames, path, duration_ms, loop)
        paths.append(path)

    return paths


def export_apng_combined(frames_by_direction: Dict[Direction, List[Image.Image]],
                         output_path: str, duration_ms: int = 100,
                         loop: int = 0) -> str:
    """Export all directions as a single APNG, cycling through all directions sequentially.

    Args:
        frames_by_direction: Dict mapping Direction to frame lists.
        output_path: Path to save the APNG.
        duration_ms: Duration per frame.
        loop: Loop count.

    Returns:
        The output_path on success.
    """
    all_frames = []
    direction_order = [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]
    for d in direction_order:
        all_frames.extend(frames_by_direction.get(d, []))

    return export_apng(all_frames, output_path, duration_ms, loop)
