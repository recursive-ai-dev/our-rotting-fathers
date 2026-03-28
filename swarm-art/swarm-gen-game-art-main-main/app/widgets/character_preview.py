#!/usr/bin/env python3
"""
Character Preview Widget - Displays character sprites with zoom and 4-up grid view.
"""

from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                              QSlider, QPushButton, QGridLayout, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PIL import Image
from typing import Dict, Optional

from generator.direction_renderer import Direction
from app.utils.image_conversion import pil_to_qpixmap


class CharacterPreviewWidget(QWidget):
    """Widget displaying character preview with zoom control."""

    zoom_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._zoom = 4
        self._grid_mode = False
        self._renders: Dict[Direction, Image.Image] = {}
        self._current_direction = Direction.DOWN
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Preview area
        self._preview_frame = QFrame()
        self._preview_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self._preview_frame.setMinimumSize(200, 200)
        self._preview_layout = QVBoxLayout(self._preview_frame)

        self._single_label = QLabel()
        self._single_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview_layout.addWidget(self._single_label)

        # Grid view (hidden by default)
        self._grid_widget = QWidget()
        self._grid_layout = QGridLayout(self._grid_widget)
        self._grid_layout.setSpacing(2)
        self._grid_labels = {}
        positions = {
            Direction.UP: (0, 1),
            Direction.LEFT: (1, 0),
            Direction.DOWN: (1, 1),
            Direction.RIGHT: (1, 2),
        }
        for d, (r, c) in positions.items():
            lbl = QLabel()
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFrameStyle(QFrame.Shape.Box)
            self._grid_layout.addWidget(lbl, r, c)
            self._grid_labels[d] = lbl
        # Direction labels
        for d, (r, c) in positions.items():
            name_lbl = QLabel(d.value.upper())
            name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._grid_layout.addWidget(name_lbl, r + 2 if r == 1 else r, c if r == 0 else c)

        self._grid_widget.hide()
        self._preview_layout.addWidget(self._grid_widget)

        layout.addWidget(self._preview_frame, 1)

        # Controls
        controls = QHBoxLayout()

        controls.addWidget(QLabel("Zoom:"))
        self._zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self._zoom_slider.setRange(1, 16)
        self._zoom_slider.setValue(self._zoom)
        self._zoom_slider.valueChanged.connect(self._on_zoom_changed)
        controls.addWidget(self._zoom_slider)

        self._zoom_label = QLabel(f"{self._zoom}x")
        controls.addWidget(self._zoom_label)

        self._grid_btn = QPushButton("4-Up Grid")
        self._grid_btn.setCheckable(True)
        self._grid_btn.toggled.connect(self._toggle_grid)
        controls.addWidget(self._grid_btn)

        layout.addLayout(controls)

    def set_renders(self, renders: Dict[Direction, Image.Image]):
        """Set all direction renders and update display."""
        self._renders = renders
        self._update_display()

    def set_direction(self, direction: Direction):
        """Set current direction for single view."""
        self._current_direction = direction
        if not self._grid_mode:
            self._update_display()

    def _on_zoom_changed(self, value: int):
        self._zoom = value
        self._zoom_label.setText(f"{value}x")
        self._update_display()
        self.zoom_changed.emit(value)

    def _toggle_grid(self, checked: bool):
        self._grid_mode = checked
        self._single_label.setVisible(not checked)
        self._grid_widget.setVisible(checked)
        self._update_display()

    def _update_display(self):
        if self._grid_mode:
            grid_zoom = max(1, self._zoom // 2)
            for d, label in self._grid_labels.items():
                img = self._renders.get(d)
                if img:
                    pm = pil_to_qpixmap(img, scale=grid_zoom)
                    label.setPixmap(pm)
                else:
                    label.clear()
        else:
            img = self._renders.get(self._current_direction)
            if img:
                pm = pil_to_qpixmap(img, scale=self._zoom)
                self._single_label.setPixmap(pm)
            else:
                self._single_label.clear()
