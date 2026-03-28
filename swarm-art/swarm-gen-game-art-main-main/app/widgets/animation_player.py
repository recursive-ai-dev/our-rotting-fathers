#!/usr/bin/env python3
"""
Animation Player Widget - QTimer-based frame playback with controls.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QComboBox, QSlider, QLabel, QSpinBox, QGroupBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PIL import Image
from typing import Dict, List, Optional

from generator.direction_renderer import Direction
from generator.animation_types import ANIMATION_DEFS
from app.utils.image_conversion import pil_to_qpixmap


class AnimationPlayerWidget(QWidget):
    """Animation playback controls and display."""

    animation_type_changed = pyqtSignal(str)
    generate_animation_requested = pyqtSignal(str)  # anim_type

    def __init__(self, parent=None):
        super().__init__(parent)
        self._frames: List[Image.Image] = []
        self._current_frame = 0
        self._playing = False
        self._zoom = 4
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._next_frame)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Animation preview
        self._preview_label = QLabel()
        self._preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview_label.setMinimumSize(100, 100)
        layout.addWidget(self._preview_label, 1)

        # Animation type selector
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Animation:"))
        self._type_combo = QComboBox()
        self._type_combo.addItems(list(ANIMATION_DEFS.keys()))
        self._type_combo.currentTextChanged.connect(self._on_type_changed)
        type_layout.addWidget(self._type_combo)

        self._gen_btn = QPushButton("Generate")
        self._gen_btn.clicked.connect(self._on_generate)
        type_layout.addWidget(self._gen_btn)
        layout.addLayout(type_layout)

        # Playback controls
        playback = QHBoxLayout()

        self._play_btn = QPushButton("Play")
        self._play_btn.setCheckable(True)
        self._play_btn.toggled.connect(self._toggle_play)
        playback.addWidget(self._play_btn)

        playback.addWidget(QLabel("Speed:"))
        self._speed_slider = QSlider(Qt.Orientation.Horizontal)
        self._speed_slider.setRange(20, 500)
        self._speed_slider.setValue(100)
        self._speed_slider.valueChanged.connect(self._on_speed_changed)
        playback.addWidget(self._speed_slider)
        self._speed_label = QLabel("100ms")
        playback.addWidget(self._speed_label)

        layout.addLayout(playback)

        # Frame scrubber
        scrub = QHBoxLayout()
        scrub.addWidget(QLabel("Frame:"))
        self._frame_slider = QSlider(Qt.Orientation.Horizontal)
        self._frame_slider.setRange(0, 0)
        self._frame_slider.valueChanged.connect(self._on_frame_scrub)
        scrub.addWidget(self._frame_slider)
        self._frame_label = QLabel("0/0")
        scrub.addWidget(self._frame_label)
        layout.addLayout(scrub)

    def set_frames(self, frames: List[Image.Image]):
        """Set animation frames for playback."""
        self._frames = frames
        self._current_frame = 0
        self._frame_slider.setRange(0, max(0, len(frames) - 1))
        self._frame_slider.setValue(0)
        self._update_display()

    def set_zoom(self, zoom: int):
        """Set zoom level for animation preview."""
        self._zoom = zoom
        self._update_display()

    def _on_type_changed(self, text: str):
        self.animation_type_changed.emit(text)

    def _on_generate(self):
        self.generate_animation_requested.emit(self._type_combo.currentText())

    def _toggle_play(self, checked: bool):
        self._playing = checked
        self._play_btn.setText("Pause" if checked else "Play")
        if checked:
            speed = self._speed_slider.value()
            self._timer.start(speed)
        else:
            self._timer.stop()

    def _on_speed_changed(self, value: int):
        self._speed_label.setText(f"{value}ms")
        if self._playing:
            self._timer.setInterval(value)

    def _on_frame_scrub(self, value: int):
        self._current_frame = value
        self._update_display()

    def _next_frame(self):
        if not self._frames:
            return
        anim_type = self._type_combo.currentText()
        anim_def = ANIMATION_DEFS.get(anim_type)
        self._current_frame += 1
        if self._current_frame >= len(self._frames):
            if anim_def and anim_def.loop:
                self._current_frame = 0
            else:
                self._current_frame = len(self._frames) - 1
                self._toggle_play(False)
                self._play_btn.setChecked(False)
                return
        self._frame_slider.blockSignals(True)
        self._frame_slider.setValue(self._current_frame)
        self._frame_slider.blockSignals(False)
        self._update_display()

    def _update_display(self):
        if self._frames and 0 <= self._current_frame < len(self._frames):
            frame = self._frames[self._current_frame]
            pm = pil_to_qpixmap(frame, scale=self._zoom)
            self._preview_label.setPixmap(pm)
            self._frame_label.setText(f"{self._current_frame + 1}/{len(self._frames)}")
        else:
            self._preview_label.clear()
            self._frame_label.setText("0/0")
