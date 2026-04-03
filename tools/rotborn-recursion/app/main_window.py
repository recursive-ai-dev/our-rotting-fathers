#!/usr/bin/env python3
"""
ROTBORN RECURSION ENGINE - MAIN WINDOW
=======================================

The interface the swarm uses to show you what it remembers.

Dark. Functional. Slightly wrong.
"""

from PyQt6.QtWidgets import (QMainWindow, QSplitter, QWidget, QVBoxLayout,
                              QMenuBar, QToolBar, QStatusBar, QMessageBox,
                              QFileDialog)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QAction, QKeySequence
from PIL import Image
from typing import Dict, List

from generator.direction_renderer import Direction
from generator.animation_types import ANIMATION_DEFS

from app.models.character_model import CharacterModel
from app.widgets.character_preview import CharacterPreviewWidget
from app.widgets.generation_controls import GenerationControlsWidget
from app.widgets.animation_player import AnimationPlayerWidget
from app.widgets.export_panel import ExportPanelWidget
from app.widgets.direction_selector import DirectionSelectorWidget


class MainWindow(QMainWindow):
    """Main application window — Rotborn Recursion Engine."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rotborn Recursion Engine")
        self.setMinimumSize(900, 600)

        self._model = CharacterModel(canvas_size=(32, 32))
        self._settings = QSettings("RotbornRecursion", "RotbornRecursionEngine")

        self._setup_ui()
        self._setup_menus()
        self._setup_toolbar()
        self._connect_signals()
        self._restore_geometry()

    def _setup_ui(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel — Generation Controls + Direction Selector
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self._controls = GenerationControlsWidget()
        left_layout.addWidget(self._controls)

        self._direction_selector = DirectionSelectorWidget()
        left_layout.addWidget(self._direction_selector)

        left_widget.setMaximumWidth(320)
        splitter.addWidget(left_widget)

        # Center panel — Preview + Animation
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)

        self._preview = CharacterPreviewWidget()
        center_layout.addWidget(self._preview, 2)

        self._animation_player = AnimationPlayerWidget()
        center_layout.addWidget(self._animation_player, 1)

        splitter.addWidget(center_widget)

        # Right panel — Export
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self._export_panel = ExportPanelWidget()
        right_layout.addWidget(self._export_panel)

        right_widget.setMaximumWidth(280)
        splitter.addWidget(right_widget)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)

        self.setCentralWidget(splitter)

        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status.showMessage("The swarm is waiting. Press REMEMBER.")

    def _setup_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        remember_action = QAction("&Remember (Generate)", self)
        remember_action.setShortcut(QKeySequence("Ctrl+R"))
        remember_action.triggered.connect(self._on_randomize)
        file_menu.addAction(remember_action)

        file_menu.addSeparator()

        export_action = QAction("&Export...", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self._export_panel._on_export)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        view_menu = menubar.addMenu("&View")

        grid_action = QAction("Toggle &Grid", self)
        grid_action.setShortcut(QKeySequence("Ctrl+G"))
        grid_action.triggered.connect(lambda: self._preview._grid_btn.toggle())
        view_menu.addAction(grid_action)

        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_toolbar(self):
        toolbar = QToolBar("Main")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        remember_btn = QAction("Remember", self)
        remember_btn.triggered.connect(self._on_randomize)
        toolbar.addAction(remember_btn)

        export_btn = QAction("Export", self)
        export_btn.triggered.connect(self._export_panel._on_export)
        toolbar.addAction(export_btn)

    def _connect_signals(self):
        self._controls.generate_requested.connect(self._on_generate)
        self._controls.randomize_requested.connect(self._on_randomize)

        self._direction_selector.direction_changed.connect(self._on_direction_changed)

        self._model.character_generated.connect(self._on_character_generated)
        self._model.animation_generated.connect(self._on_animation_generated)
        self._model.generation_started.connect(
            lambda: self._status.showMessage("The swarm is remembering..."))
        self._model.generation_finished.connect(
            lambda: self._status.showMessage("The swarm has remembered."))

        self._animation_player.generate_animation_requested.connect(self._on_gen_animation)
        self._preview.zoom_changed.connect(self._animation_player.set_zoom)
        self._export_panel.export_finished.connect(
            lambda msg: self._status.showMessage(msg))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self._animation_player._play_btn.toggle()
        else:
            super().keyPressEvent(event)

    def _on_generate(self, params: dict):
        canvas_size = params.get('canvas_size', 32)
        self._model.canvas_size = (canvas_size, canvas_size)
        self._model.seed = params.get('seed')

        faction = params.get('faction')
        rank = params.get('rank')
        palette = params.get('palette')

        self._model.generate_character(
            faction=faction,
            rank=rank,
            palette=palette,
        )

        # Auto-generate the selected animation
        anim_type = params.get('animation', 'twitch')
        self._on_gen_animation(anim_type)

    def _on_randomize(self):
        self._model.randomize()

    def _on_direction_changed(self, direction: Direction):
        self._model.current_direction = direction
        self._preview.set_direction(direction)

        anim_type = self._animation_player._type_combo.currentText()
        cached = self._model.get_cached_animation(anim_type)
        if cached and direction in cached:
            self._animation_player.set_frames(cached[direction])

    def _on_character_generated(self, renders: Dict[Direction, Image.Image]):
        self._preview.set_renders(renders)
        self._export_panel.set_static_renders(renders)

        params = self._model.params
        if params:
            faction = params.get('_faction', '')
            faction_str = f" [{faction}]" if faction else ""
            self._status.showMessage(
                f"Remembered: {params.get('gender', '?')}, "
                f"{params.get('age_category', '?')}{faction_str}"
            )

    def _on_gen_animation(self, anim_type: str):
        self._status.showMessage(f"Animating: {anim_type}...")
        self._model.generate_animation_frames(anim_type, list(Direction))

    def _on_animation_generated(self, anim_type: str,
                                 frames_by_dir: Dict[Direction, List[Image.Image]]):
        direction = self._direction_selector.current_direction()
        frames = frames_by_dir.get(direction, [])
        self._animation_player.set_frames(frames)
        self._export_panel.set_animation_cache(anim_type, frames_by_dir)

        anim_def = ANIMATION_DEFS.get(anim_type)
        if anim_def:
            self._animation_player._speed_slider.setValue(anim_def.speed_ms)

        self._status.showMessage(
            f"Animation '{anim_type}': {len(frames)} frames. "
            f"The body remembers this movement.")

    def _show_about(self):
        QMessageBox.about(
            self, "Rotborn Recursion Engine",
            "Rotborn Recursion Engine v1.0\n\n"
            "The swarm agents experienced the god's death for a millenia.\n"
            "Now they reproduce what they witnessed.\n\n"
            "Each sprite is a haunted memory.\n\n"
            "Factions: Purified · Rotborn · Architects · System\n"
            "Animations: Twitch · Shamble · Convulse · Stumble · Worship · Transform\n"
            "Palettes: Rotting · Bloodstained · Spore-Infested · Bone-Dry · Bruised\n\n"
            "Built with PyQt6 and Pillow."
        )

    def closeEvent(self, event):
        self._settings.setValue("geometry", self.saveGeometry())
        self._settings.setValue("windowState", self.saveState())
        super().closeEvent(event)

    def _restore_geometry(self):
        geom = self._settings.value("geometry")
        if geom:
            self.restoreGeometry(geom)
        state = self._settings.value("windowState")
        if state:
            self.restoreState(state)
