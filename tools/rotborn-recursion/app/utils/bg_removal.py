#!/usr/bin/env python3
"""
Rule-Based Background Removal Engine.
Adaptive deterministic algorithm using border sampling, color distance, and flood fill.
"""

import numpy as np
from PIL import Image
from typing import Tuple, Optional
from collections import deque


def remove_background(image: Image.Image, threshold_offset: float = 10.0,
                      border_samples: int = 20,
                      refinement_passes: int = 1) -> Image.Image:
    """Remove background from an image using adaptive rule-based algorithm.

    Steps:
        1. Border sampling from all 4 edges
        2. Dominant color detection via median of border pixels
        3. Per-pixel color distance from dominant color
        4. Adaptive threshold: mean border distance + 2*std + offset
        5. Flood fill from border pixels below threshold
        6. Morphological refinement (erosion/dilation)
        7. Apply mask as alpha channel

    Args:
        image: Input PIL Image (RGB or RGBA).
        threshold_offset: Base offset added to adaptive threshold.
        border_samples: Number of sample rows from each edge.
        refinement_passes: Number of morphological erosion/dilation passes.

    Returns:
        RGBA PIL Image with background removed (transparent).
    """
    # Ensure RGB
    if image.mode == 'RGBA':
        rgb = image.convert('RGB')
    elif image.mode == 'RGB':
        rgb = image
    else:
        rgb = image.convert('RGB')

    arr = np.array(rgb, dtype=np.float32)
    h, w = arr.shape[:2]

    # Step 1: Border sampling
    border_pixels = _sample_border_pixels(arr, border_samples)

    # Step 2: Dominant color (median is robust to outliers)
    dominant_color = np.median(border_pixels, axis=0)

    # Step 3: Per-pixel color distance
    distance_map = np.sqrt(np.sum((arr - dominant_color) ** 2, axis=2))

    # Step 4: Adaptive threshold
    border_distances = np.sqrt(np.sum((border_pixels - dominant_color) ** 2, axis=1))
    mean_dist = np.mean(border_distances)
    std_dist = np.std(border_distances)
    threshold = mean_dist + 2.0 * std_dist + threshold_offset

    # Step 5: Flood fill from edges
    bg_mask = _flood_fill_from_edges(distance_map, threshold)

    # Step 6: Morphological refinement
    if refinement_passes > 0:
        bg_mask = _morphological_refine(bg_mask, refinement_passes)

    # Step 7: Apply as alpha channel
    alpha = np.where(bg_mask, 0, 255).astype(np.uint8)
    result = image.convert('RGBA')
    result_arr = np.array(result)
    result_arr[:, :, 3] = alpha
    return Image.fromarray(result_arr, 'RGBA')


def _sample_border_pixels(arr: np.ndarray, samples: int) -> np.ndarray:
    """Sample pixels from all 4 edges of the image."""
    h, w = arr.shape[:2]
    pixels = []

    # Top edge
    rows = min(samples, h)
    for r in range(rows):
        pixels.extend(arr[r, :, :].tolist())

    # Bottom edge
    for r in range(max(0, h - rows), h):
        pixels.extend(arr[r, :, :].tolist())

    # Left edge
    cols = min(samples, w)
    for c in range(cols):
        pixels.extend(arr[:, c, :].tolist())

    # Right edge
    for c in range(max(0, w - cols), w):
        pixels.extend(arr[:, c, :].tolist())

    return np.array(pixels, dtype=np.float32)


def _flood_fill_from_edges(distance_map: np.ndarray, threshold: float) -> np.ndarray:
    """BFS flood fill from border pixels that are below threshold."""
    h, w = distance_map.shape
    visited = np.zeros((h, w), dtype=bool)
    bg_mask = np.zeros((h, w), dtype=bool)
    queue = deque()

    # Seed with all border pixels below threshold
    for x in range(w):
        if distance_map[0, x] <= threshold:
            queue.append((0, x))
            visited[0, x] = True
        if distance_map[h - 1, x] <= threshold:
            queue.append((h - 1, x))
            visited[h - 1, x] = True

    for y in range(h):
        if distance_map[y, 0] <= threshold:
            queue.append((y, 0))
            visited[y, 0] = True
        if distance_map[y, w - 1] <= threshold:
            queue.append((y, w - 1))
            visited[y, w - 1] = True

    # BFS expansion
    while queue:
        cy, cx = queue.popleft()
        bg_mask[cy, cx] = True

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                visited[ny, nx] = True
                if distance_map[ny, nx] <= threshold:
                    queue.append((ny, nx))

    return bg_mask


def _morphological_refine(mask: np.ndarray, passes: int) -> np.ndarray:
    """Apply morphological erosion then dilation to smooth mask edges.
    Uses border_value=True so edge pixels are preserved during erosion."""
    try:
        from scipy.ndimage import binary_erosion, binary_dilation
        struct = np.ones((3, 3), dtype=bool)
        result = mask
        for _ in range(passes):
            result = binary_erosion(result, structure=struct, border_value=True, iterations=1)
            result = binary_dilation(result, structure=struct, iterations=1)
        return result
    except ImportError:
        # Fallback: manual 3x3 convolution
        return _manual_morphological_refine(mask, passes)


def _manual_morphological_refine(mask: np.ndarray, passes: int) -> np.ndarray:
    """Manual erosion/dilation fallback without scipy."""
    h, w = mask.shape
    result = mask.copy()

    for _ in range(passes):
        # Erosion: pixel is True only if all 4 neighbors are True
        eroded = np.zeros_like(result)
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if result[y, x] and result[y-1, x] and result[y+1, x] and result[y, x-1] and result[y, x+1]:
                    eroded[y, x] = True
        # Edges stay as-is
        eroded[0, :] = result[0, :]
        eroded[h-1, :] = result[h-1, :]
        eroded[:, 0] = result[:, 0]
        eroded[:, w-1] = result[:, w-1]

        # Dilation: pixel is True if any of 4 neighbors are True
        dilated = eroded.copy()
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if eroded[y-1, x] or eroded[y+1, x] or eroded[y, x-1] or eroded[y, x+1]:
                    dilated[y, x] = True

        result = dilated

    return result
