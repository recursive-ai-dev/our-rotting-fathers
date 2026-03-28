#!/usr/bin/env python3
"""
Main Window - QMainWindow with splitter layout for the character generator GUI.
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
from app.widgets.bg_removal_panel import BackgroundRemovalWidget
from app.widgets.direction_selector import DirectionSelectorWidget


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Game Art Generator")
        self.setMinimumSize(900, 600)

        self._model = CharacterModel(canvas_size=(32, 32))
        self._settings = QSettings("SwarmGenGameArt", "GameArtGenerator")

        self._setup_ui()
        self._setup_menus()
        self._setup_toolbar()
        self._connect_signals()
        self._restore_geometry()

    def _setup_ui(self):
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Generation Controls + Direction Selector
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self._controls = GenerationControlsWidget()
        left_layout.addWidget(self._controls)

        self._direction_selector = DirectionSelectorWidget()
        left_layout.addWidget(self._direction_selector)

        left_widget.setMaximumWidth(350)
        splitter.addWidget(left_widget)

        # Center panel - Preview + Animation
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)

        self._preview = CharacterPreviewWidget()
        center_layout.addWidget(self._preview, 2)

        self._animation_player = AnimationPlayerWidget()
        center_layout.addWidget(self._animation_player, 1)

        splitter.addWidget(center_widget)

        # Right panel - Export + BG Removal
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self._export_panel = ExportPanelWidget()
        right_layout.addWidget(self._export_panel)

        self._bg_removal = BackgroundRemovalWidget()
        right_layout.addWidget(self._bg_removal)

        right_widget.setMaximumWidth(300)
        splitter.addWidget(right_widget)

        # Set stretch factors
        splitter.setStretchFactor(0, 0)  # Left fixed
        splitter.setStretchFactor(1, 1)  # Center stretches
        splitter.setStretchFactor(2, 0)  # Right fixed

        self.setCentralWidget(splitter)

        # Status bar
        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status.showMessage("Ready. Click Generate or press Ctrl+R to randomize.")

    def _setup_menus(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New Character", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._on_randomize)
        file_menu.addAction(new_action)

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

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        randomize_action = QAction("&Randomize", self)
        randomize_action.setShortcut(QKeySequence("Ctrl+R"))
        randomize_action.triggered.connect(self._on_randomize)
        edit_menu.addAction(randomize_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        grid_action = QAction("Toggle &Grid View", self)
        grid_action.setShortcut(QKeySequence("Ctrl+G"))
        grid_action.triggered.connect(lambda: self._preview._grid_btn.toggle())
        view_menu.addAction(grid_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_toolbar(self):
        toolbar = QToolBar("Main")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        new_btn = QAction("New", self)
        new_btn.triggered.connect(self._on_randomize)
        toolbar.addAction(new_btn)

        randomize_btn = QAction("Randomize", self)
        randomize_btn.triggered.connect(self._on_randomize)
        toolbar.addAction(randomize_btn)

        export_btn = QAction("Export", self)
        export_btn.triggered.connect(self._export_panel._on_export)
        toolbar.addAction(export_btn)

    def _connect_signals(self):
        # Controls -> Model
        self._controls.generate_requested.connect(self._on_generate)
        self._controls.randomize_requested.connect(self._on_randomize)

        # Direction selector -> Preview
        self._direction_selector.direction_changed.connect(self._on_direction_changed)

        # Model -> Preview
        self._model.character_generated.connect(self._on_character_generated)
        self._model.animation_generated.connect(self._on_animation_generated)
        self._model.generation_started.connect(
            lambda: self._status.showMessage("Generating..."))
        self._model.generation_finished.connect(
            lambda: self._status.showMessage("Character generated."))

        # Animation player
        self._animation_player.generate_animation_requested.connect(self._on_gen_animation)

        # Preview zoom -> animation player zoom
        self._preview.zoom_changed.connect(self._animation_player.set_zoom)

        # Export panel
        self._export_panel.export_finished.connect(
            lambda msg: self._status.showMessage(msg))

        # Play/Pause with Space
        # (handled by keyPressEvent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self._animation_player._play_btn.toggle()
        else:
            super().keyPressEvent(event)

    def _on_generate(self, params: dict):
        canvas_size = params.get('canvas_size', 32)
        self._model.canvas_size = (canvas_size, canvas_size)
        self._model.seed = params.get('seed')
        self._model.use_swarm = params.get('use_swarm', False)
        self._model.generate_character(
            gender=params.get('gender'),
            social_class=params.get('social_class'),
            age_category=params.get('age_category'),
            body_type=params.get('body_type'),
            hair_style=params.get('hair_style'),
            face_style=params.get('face_style'),
        )

    def _on_randomize(self):
        self._model.randomize()

    def _on_direction_changed(self, direction: Direction):
        self._model.current_direction = direction
        self._preview.set_direction(direction)

        # Update animation player frames for new direction
        anim_type = self._animation_player._type_combo.currentText()
        cached = self._model.get_cached_animation(anim_type)
        if cached and direction in cached:
            self._animation_player.set_frames(cached[direction])

    def _on_character_generated(self, renders: Dict[Direction, Image.Image]):
        self._preview.set_renders(renders)
        self._export_panel.set_static_renders(renders)

        # Show params in status
        params = self._model.params
        if params:
            self._status.showMessage(
                f"Generated: {params['gender']}, {params['age_category']}, "
                f"{params['social_class']} - {params['body_metrics'].get('body_type_display', '')}"
            )

    def _on_gen_animation(self, anim_type: str):
        direction = self._direction_selector.current_direction()
        self._status.showMessage(f"Generating {anim_type} animation...")
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
            f"Animation '{anim_type}': {len(frames)} frames generated for all directions.")

    def _show_about(self):
        QMessageBox.about(
            self, "About 2D Game Art Generator",
            "2D Game Art Generator v2.0\n\n"
            "Procedural character sprite generator with:\n"
            "- 338M+ unique character combinations\n"
            "- 4-directional rendering (front/back/left/right)\n"
            "- 9 animation types (idle, walk, run, jump, attack, pickup, variants)\n"
            "- RPG Maker sheet, APNG, and individual PNG export\n"
            "- Rule-based background removal\n"
            "- Multi-agent swarm AI generation\n\n"
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
