#!/usr/bin/env python3
"""
Background Removal Panel - UI for loading images and removing backgrounds.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QGroupBox, QSlider, QLabel, QSpinBox,
                              QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PIL import Image
from typing import Optional

from app.utils.bg_removal import remove_background
from app.utils.image_conversion import pil_to_qpixmap


class BackgroundRemovalWidget(QWidget):
    """Background removal tool with before/after preview."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._source_image: Optional[Image.Image] = None
        self._result_image: Optional[Image.Image] = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        group = QGroupBox("Background Removal")
        inner = QVBoxLayout()

        # Load button
        self._load_btn = QPushButton("Load Image...")
        self._load_btn.clicked.connect(self._on_load)
        inner.addWidget(self._load_btn)

        # Before/After previews
        preview_layout = QHBoxLayout()

        before_layout = QVBoxLayout()
        before_layout.addWidget(QLabel("Before:"))
        self._before_label = QLabel()
        self._before_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._before_label.setMinimumSize(80, 80)
        before_layout.addWidget(self._before_label)
        preview_layout.addLayout(before_layout)

        after_layout = QVBoxLayout()
        after_layout.addWidget(QLabel("After:"))
        self._after_label = QLabel()
        self._after_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._after_label.setMinimumSize(80, 80)
        after_layout.addWidget(self._after_label)
        preview_layout.addLayout(after_layout)

        inner.addLayout(preview_layout)

        # Controls
        ctrl_layout = QHBoxLayout()
        ctrl_layout.addWidget(QLabel("Threshold:"))
        self._threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self._threshold_slider.setRange(0, 100)
        self._threshold_slider.setValue(10)
        ctrl_layout.addWidget(self._threshold_slider)
        self._threshold_label = QLabel("10")
        self._threshold_slider.valueChanged.connect(
            lambda v: self._threshold_label.setText(str(v)))
        ctrl_layout.addWidget(self._threshold_label)
        inner.addLayout(ctrl_layout)

        refine_layout = QHBoxLayout()
        refine_layout.addWidget(QLabel("Refinement:"))
        self._refine_spin = QSpinBox()
        self._refine_spin.setRange(0, 5)
        self._refine_spin.setValue(1)
        refine_layout.addWidget(self._refine_spin)
        inner.addLayout(refine_layout)

        # Action buttons
        btn_layout = QHBoxLayout()
        self._remove_btn = QPushButton("Remove BG")
        self._remove_btn.clicked.connect(self._on_remove)
        self._remove_btn.setEnabled(False)
        btn_layout.addWidget(self._remove_btn)

        self._save_btn = QPushButton("Save...")
        self._save_btn.clicked.connect(self._on_save)
        self._save_btn.setEnabled(False)
        btn_layout.addWidget(self._save_btn)

        inner.addLayout(btn_layout)
        group.setLayout(inner)
        layout.addWidget(group)
        layout.addStretch()

    def _on_load(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if not path:
            return

        try:
            self._source_image = Image.open(path)
            self._result_image = None
            self._after_label.clear()
            self._save_btn.setEnabled(False)

            # Show before preview
            preview = self._source_image.copy()
            preview.thumbnail((120, 120), Image.NEAREST)
            self._before_label.setPixmap(pil_to_qpixmap(preview))
            self._remove_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {e}")

    def _on_remove(self):
        if self._source_image is None:
            return

        threshold = float(self._threshold_slider.value())
        passes = self._refine_spin.value()

        try:
            self._result_image = remove_background(
                self._source_image,
                threshold_offset=threshold,
                refinement_passes=passes
            )

            # Show after preview
            preview = self._result_image.copy()
            preview.thumbnail((120, 120), Image.NEAREST)
            self._after_label.setPixmap(pil_to_qpixmap(preview))
            self._save_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Background removal failed: {e}")

    def _on_save(self):
        if self._result_image is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Result", "", "PNG Files (*.png)")
        if path:
            self._result_image.save(path, "PNG")
