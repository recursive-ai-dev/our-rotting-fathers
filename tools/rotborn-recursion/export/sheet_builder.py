#!/usr/bin/env python3
"""
RPG Maker Style Sheet Builder.
Builds sprite sheets with rows per direction and columns per frame.

Layout:
    Row 0: DOWN frames  (down_0, down_1, ..., down_N)
    Row 1: LEFT frames
    Row 2: RIGHT frames
    Row 3: UP frames
"""

from PIL import Image
from typing import Dict, List, Tuple
from generator.direction_renderer import Direction


# Standard row order matching RPG Maker conventions
DIRECTION_ROW_ORDER = [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]


def build_rpg_sheet(frames_by_direction: Dict[Direction, List[Image.Image]],
                    output_path: str) -> str:
    """Build an RPG Maker-style sprite sheet.

    Args:
        frames_by_direction: Dict mapping Direction to list of frame Images.
        output_path: Path to save the resulting PNG.

    Returns:
        The output_path on success.
    """
    if not frames_by_direction:
        return ""

    # Determine dimensions from first available direction
    sample_frames = next(iter(frames_by_direction.values()))
    frame_w = sample_frames[0].width
    frame_h = sample_frames[0].height
    max_cols = max(len(frames) for frames in frames_by_direction.values())
    num_rows = len(DIRECTION_ROW_ORDER)

    sheet = Image.new('RGBA', (frame_w * max_cols, frame_h * num_rows), (0, 0, 0, 0))

    for row_idx, direction in enumerate(DIRECTION_ROW_ORDER):
        frames = frames_by_direction.get(direction, [])
        for col_idx, frame in enumerate(frames):
            x = col_idx * frame_w
            y = row_idx * frame_h
            sheet.paste(frame, (x, y), frame)

    sheet.save(output_path, "PNG")
    return output_path


def build_single_direction_sheet(frames: List[Image.Image], output_path: str,
                                 horizontal: bool = True) -> str:
    """Build a simple single-row or single-column sprite sheet."""
    if not frames:
        return ""

    frame_w = frames[0].width
    frame_h = frames[0].height
    count = len(frames)

    if horizontal:
        sheet = Image.new('RGBA', (frame_w * count, frame_h), (0, 0, 0, 0))
        for i, frame in enumerate(frames):
            sheet.paste(frame, (i * frame_w, 0), frame)
    else:
        sheet = Image.new('RGBA', (frame_w, frame_h * count), (0, 0, 0, 0))
        for i, frame in enumerate(frames):
            sheet.paste(frame, (0, i * frame_h), frame)

    sheet.save(output_path, "PNG")
    return output_path
