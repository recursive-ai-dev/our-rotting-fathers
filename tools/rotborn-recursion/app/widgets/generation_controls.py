#!/usr/bin/env python3
"""
ROTBORN GENERATION CONTROLS
============================

The controls the swarm uses to remember.

Not "Generate." Remember.
Not "Social Class." Corruption Source.
Not "Animation." What the body does when it forgets to pretend.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QComboBox, QSpinBox, QPushButton, QCheckBox,
                              QGroupBox, QLabel, QSlider)
from PyQt6.QtCore import pyqtSignal, Qt


class GenerationControlsWidget(QWidget):
    """Rotborn parameter panel for haunted character generation."""

    generate_requested = pyqtSignal(dict)
    randomize_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)

        # ---- Faction ----
        faction_group = QGroupBox("Faction")
        faction_layout = QFormLayout()
        faction_layout.setSpacing(6)

        self._faction_combo = QComboBox()
        self._faction_combo.addItems(["Random", "purified", "rotborn", "architects", "system"])
        self._faction_combo.setToolTip(
            "Purified: hollow, lobotomized\n"
            "Rotborn: bloated, mutated\n"
            "Architects: uncanny valley\n"
            "System: neural-implanted"
        )
        faction_layout.addRow("Faction:", self._faction_combo)

        self._rank_combo = QComboBox()
        self._rank_combo.addItems(["Random"])
        self._faction_combo.currentTextChanged.connect(self._update_rank_options)
        faction_layout.addRow("Rank / Stage:", self._rank_combo)

        faction_group.setLayout(faction_layout)
        layout.addWidget(faction_group)

        # ---- Trauma ----
        trauma_group = QGroupBox("Trauma")
        trauma_layout = QFormLayout()
        trauma_layout.setSpacing(6)

        self._palette_combo = QComboBox()
        self._palette_combo.addItems(["Random", "rotting", "bloodstained", "spore_infested", "bone_dry", "bruised"])
        trauma_layout.addRow("Palette:", self._palette_combo)

        self._body_combo = QComboBox()
        self._body_combo.addItems(["Random", "emaciated", "bloated", "twisted", "undead", "mutated"])
        trauma_layout.addRow("Body Type:", self._body_combo)

        # Trauma slider (0 = mild unease, 100 = full horror)
        trauma_slider_row = QWidget()
        trauma_slider_layout = QHBoxLayout(trauma_slider_row)
        trauma_slider_layout.setContentsMargins(0, 0, 0, 0)
        self._trauma_slider = QSlider(Qt.Orientation.Horizontal)
        self._trauma_slider.setRange(0, 100)
        self._trauma_slider.setValue(50)
        self._trauma_slider.setToolTip("How much horror? 0 = mild unease, 100 = unplayable")
        self._trauma_label = QLabel("50%")
        self._trauma_label.setFixedWidth(32)
        self._trauma_slider.valueChanged.connect(
            lambda v: self._trauma_label.setText(f"{v}%"))
        trauma_slider_layout.addWidget(self._trauma_slider)
        trauma_slider_layout.addWidget(self._trauma_label)
        trauma_layout.addRow("Trauma:", trauma_slider_row)

        # Anomaly toggle
        self._anomaly_check = QCheckBox("Enable anomalies")
        self._anomaly_check.setChecked(True)
        self._anomaly_check.setToolTip("5% chance of rule-breaking sprites")
        trauma_layout.addRow(self._anomaly_check)

        trauma_group.setLayout(trauma_layout)
        layout.addWidget(trauma_group)

        # ---- Animation ----
        anim_group = QGroupBox("Animation")
        anim_layout = QFormLayout()
        anim_layout.setSpacing(6)

        self._anim_combo = QComboBox()
        self._anim_combo.addItems([
            "twitch", "shamble", "convulse", "stumble", "worship", "transform",
            "idle", "walk", "run", "attack",
        ])
        self._anim_combo.setToolTip(
            "twitch: involuntary spasms\n"
            "shamble: dragging movement\n"
            "convulse: violent full-body\n"
            "stumble: almost falling\n"
            "worship: ritual prostration\n"
            "transform: body changing"
        )
        anim_layout.addRow("Animation:", self._anim_combo)

        anim_group.setLayout(anim_layout)
        layout.addWidget(anim_group)

        # ---- Canvas ----
        canvas_group = QGroupBox("Canvas")
        canvas_layout = QFormLayout()
        canvas_layout.setSpacing(6)

        self._canvas_spin = QSpinBox()
        self._canvas_spin.setRange(16, 256)
        self._canvas_spin.setValue(32)
        self._canvas_spin.setSingleStep(16)
        canvas_layout.addRow("Size:", self._canvas_spin)

        self._seed_spin = QSpinBox()
        self._seed_spin.setRange(-1, 999999)
        self._seed_spin.setValue(-1)
        self._seed_spin.setSpecialValueText("Random")
        canvas_layout.addRow("Seed:", self._seed_spin)

        canvas_group.setLayout(canvas_layout)
        layout.addWidget(canvas_group)

        # ---- Buttons ----
        self._remember_btn = QPushButton("REMEMBER")
        self._remember_btn.setObjectName("remember_btn")
        self._remember_btn.setToolTip("Generate a haunted sprite (Ctrl+R)")
        self._remember_btn.clicked.connect(self._on_generate)
        layout.addWidget(self._remember_btn)

        self._randomize_btn = QPushButton("Randomize")
        self._randomize_btn.setToolTip("Randomize all parameters")
        self._randomize_btn.clicked.connect(self._on_randomize)
        layout.addWidget(self._randomize_btn)

        layout.addStretch()

    def _update_rank_options(self, faction: str):
        """Update rank/stage options based on selected faction."""
        self._rank_combo.clear()
        self._rank_combo.addItem("Random")

        rank_options = {
            "purified": ["flesh_bound", "memory_stripped", "hollow"],
            "rotborn": ["seed", "sprout", "bloom", "twisted"],
            "architects": ["citizen", "archivist", "curator", "enforcer"],
            "system": ["novice", "synapse", "relay", "prophet"],
        }
        options = rank_options.get(faction, [])
        for opt in options:
            self._rank_combo.addItem(opt)

    def _get_override(self, combo: QComboBox):
        """Return None if 'Random', else the selected value."""
        val = combo.currentText()
        return None if val == "Random" else val

    def get_params(self) -> dict:
        """Get current parameter selections."""
        seed = self._seed_spin.value()
        return {
            'faction': self._get_override(self._faction_combo),
            'rank': self._get_override(self._rank_combo),
            'palette': self._get_override(self._palette_combo),
            'body_type': self._get_override(self._body_combo),
            'trauma_level': self._trauma_slider.value() / 100.0,
            'anomaly_enabled': self._anomaly_check.isChecked(),
            'animation': self._anim_combo.currentText(),
            'canvas_size': self._canvas_spin.value(),
            'seed': None if seed == -1 else seed,
            # Legacy compat
            'use_swarm': False,
        }

    def _on_generate(self):
        self.generate_requested.emit(self.get_params())

    def _on_randomize(self):
        self._faction_combo.setCurrentIndex(0)
        self._rank_combo.setCurrentIndex(0)
        self._palette_combo.setCurrentIndex(0)
        self._body_combo.setCurrentIndex(0)
        self._trauma_slider.setValue(50)
        self._anomaly_check.setChecked(True)
        self._seed_spin.setValue(-1)
        self.randomize_requested.emit()
