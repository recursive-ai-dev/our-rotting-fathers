#!/usr/bin/env python3
"""
Generation Controls Widget - Parameter panel with dropdowns, sliders, and randomize.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QComboBox, QSpinBox, QPushButton, QCheckBox,
                              QGroupBox, QLabel)
from PyQt6.QtCore import pyqtSignal


class GenerationControlsWidget(QWidget):
    """Parameter panel for character generation."""

    generate_requested = pyqtSignal(dict)  # params dict
    randomize_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Character attributes group
        char_group = QGroupBox("Character Attributes")
        char_layout = QFormLayout()

        self._gender_combo = QComboBox()
        self._gender_combo.addItems(["Random", "male", "female"])
        char_layout.addRow("Gender:", self._gender_combo)

        self._class_combo = QComboBox()
        self._class_combo.addItems(["Random", "poor", "working", "middle", "upper", "rich"])
        char_layout.addRow("Social Class:", self._class_combo)

        self._age_combo = QComboBox()
        self._age_combo.addItems(["Random", "teenager", "young_adult", "middle_aged", "older_adult", "elderly"])
        char_layout.addRow("Age:", self._age_combo)

        self._body_combo = QComboBox()
        self._body_combo.addItems(["Random", "slim", "average", "broad", "curvy"])
        char_layout.addRow("Body Type:", self._body_combo)

        self._hair_combo = QComboBox()
        hair_styles = [
            "Random",
            "short", "basic_short", "crew_cut", "buzzcut", "bald",
            "short_messy", "unkempt", "styled_short", "side_part", "neat_short",
            "professional", "slicked_back", "executive_cut",
            "expensive_cut", "styled_back", "designer_short",
            "long", "simple_long", "long_messy", "unkempt_long",
            "ponytail", "neat_ponytail", "bob", "elegant_bob",
            "styled_long", "layered", "professional_long", "styled_waves",
            "luxury_long", "expensive_style", "designer_cut", "glamour_waves",
            "short_rough",
        ]
        self._hair_combo.addItems(hair_styles)
        char_layout.addRow("Hair Style:", self._hair_combo)

        self._face_combo = QComboBox()
        self._face_combo.addItems(["Random", "basic", "detailed", "minimal"])
        char_layout.addRow("Face Style:", self._face_combo)

        char_group.setLayout(char_layout)
        layout.addWidget(char_group)

        # Canvas settings
        canvas_group = QGroupBox("Canvas Settings")
        canvas_layout = QFormLayout()

        self._canvas_spin = QSpinBox()
        self._canvas_spin.setRange(16, 256)
        self._canvas_spin.setValue(32)
        self._canvas_spin.setSingleStep(16)
        canvas_layout.addRow("Canvas Size:", self._canvas_spin)

        canvas_group.setLayout(canvas_layout)
        layout.addWidget(canvas_group)

        # Generation settings
        gen_group = QGroupBox("Generation")
        gen_layout = QFormLayout()

        self._seed_spin = QSpinBox()
        self._seed_spin.setRange(-1, 999999)
        self._seed_spin.setValue(-1)
        self._seed_spin.setSpecialValueText("Random")
        gen_layout.addRow("Seed:", self._seed_spin)

        self._swarm_check = QCheckBox("Use Swarm AI")
        gen_layout.addRow(self._swarm_check)

        gen_group.setLayout(gen_layout)
        layout.addWidget(gen_group)

        # Buttons
        btn_layout = QHBoxLayout()

        self._generate_btn = QPushButton("Generate")
        self._generate_btn.clicked.connect(self._on_generate)
        btn_layout.addWidget(self._generate_btn)

        self._randomize_btn = QPushButton("Randomize")
        self._randomize_btn.clicked.connect(self._on_randomize)
        btn_layout.addWidget(self._randomize_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

    def _get_override(self, combo: QComboBox):
        """Get value from combo, or None if 'Random'."""
        val = combo.currentText()
        return None if val == "Random" else val

    def get_params(self) -> dict:
        """Get current parameter selections."""
        seed = self._seed_spin.value()
        return {
            'gender': self._get_override(self._gender_combo),
            'social_class': self._get_override(self._class_combo),
            'age_category': self._get_override(self._age_combo),
            'body_type': self._get_override(self._body_combo),
            'hair_style': self._get_override(self._hair_combo),
            'face_style': self._get_override(self._face_combo),
            'canvas_size': self._canvas_spin.value(),
            'seed': None if seed == -1 else seed,
            'use_swarm': self._swarm_check.isChecked(),
        }

    def _on_generate(self):
        self.generate_requested.emit(self.get_params())

    def _on_randomize(self):
        # Reset all combos to Random
        for combo in [self._gender_combo, self._class_combo, self._age_combo,
                      self._body_combo, self._hair_combo, self._face_combo]:
            combo.setCurrentIndex(0)
        self._seed_spin.setValue(-1)
        self.randomize_requested.emit()
