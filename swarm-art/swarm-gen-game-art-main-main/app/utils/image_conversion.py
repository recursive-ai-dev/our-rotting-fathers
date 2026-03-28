#!/usr/bin/env python3
"""
Image Conversion Utilities - PIL Image <-> QPixmap conversion.
Uses nearest-neighbor scaling for pixel art zoom.
"""

from PIL import Image

try:
    from PyQt6.QtGui import QImage, QPixmap
    from PyQt6.QtCore import Qt
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False


def pil_to_qpixmap(pil_image: Image.Image, scale: int = 1) -> 'QPixmap':
    """Convert a PIL Image to a QPixmap.

    Args:
        pil_image: PIL Image in any mode (will be converted to RGBA).
        scale: Integer scale factor (nearest-neighbor for pixel art).

    Returns:
        QPixmap of the image at the specified scale.
    """
    if not PYQT_AVAILABLE:
        raise RuntimeError("PyQt6 is not installed")

    rgba = pil_image.convert('RGBA')
    data = rgba.tobytes("raw", "RGBA")
    qimg = QImage(data, rgba.width, rgba.height, rgba.width * 4,
                  QImage.Format.Format_RGBA8888)

    pixmap = QPixmap.fromImage(qimg)

    if scale > 1:
        new_w = rgba.width * scale
        new_h = rgba.height * scale
        pixmap = pixmap.scaled(new_w, new_h,
                               Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.FastTransformation)

    return pixmap


def qpixmap_to_pil(pixmap: 'QPixmap') -> Image.Image:
    """Convert a QPixmap back to a PIL Image.

    Args:
        pixmap: QPixmap to convert.

    Returns:
        PIL Image in RGBA mode.
    """
    if not PYQT_AVAILABLE:
        raise RuntimeError("PyQt6 is not installed")

    qimg = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)
    ptr = qimg.bits()
    ptr.setsize(qimg.sizeInBytes())
    arr = bytes(ptr)
    return Image.frombytes('RGBA', (qimg.width(), qimg.height()), arr)
