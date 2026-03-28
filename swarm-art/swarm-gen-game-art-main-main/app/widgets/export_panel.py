#!/usr/bin/env python3
"""
Export Panel Widget - Format selection and file dialogs for exporting.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QComboBox, QGroupBox, QFormLayout, QCheckBox,
                              QProgressBar, QFileDialog, QLabel, QMessageBox)
from PyQt6.QtCore import pyqtSignal
from PIL import Image
from typing import Dict, List, Optional

from generator.direction_renderer import Direction
from generator.animation_types import ANIMATION_DEFS
from export.sheet_builder import build_rpg_sheet
from export.apng_exporter import export_apng, export_apng_per_direction
from export.individual_exporter import export_individual_frames


class ExportPanelWidget(QWidget):
    """Export format selection and execution panel."""

    export_started = pyqtSignal()
    export_finished = pyqtSignal(str)  # message

    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation_cache: Dict[str, Dict[Direction, List[Image.Image]]] = {}
        self._static_renders: Dict[Direction, Image.Image] = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        group = QGroupBox("Export")
        form = QFormLayout()

        self._format_combo = QComboBox()
        self._format_combo.addItems(["RPG Maker Sheet", "Individual PNGs", "APNG"])
        form.addRow("Format:", self._format_combo)

        self._anim_combo = QComboBox()
        self._anim_combo.addItems(["(static)"] + list(ANIMATION_DEFS.keys()))
        form.addRow("Animation:", self._anim_combo)

        # Direction checkboxes
        self._dir_checks = {}
        dir_layout = QHBoxLayout()
        for d in Direction:
            cb = QCheckBox(d.value.upper())
            cb.setChecked(True)
            self._dir_checks[d] = cb
            dir_layout.addWidget(cb)
        form.addRow("Directions:", dir_layout)

        group.setLayout(form)
        layout.addWidget(group)

        # Progress
        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.hide()
        layout.addWidget(self._progress)

        # Export button
        self._export_btn = QPushButton("Export...")
        self._export_btn.clicked.connect(self._on_export)
        layout.addWidget(self._export_btn)

        layout.addStretch()

    def set_static_renders(self, renders: Dict[Direction, Image.Image]):
        self._static_renders = renders

    def set_animation_cache(self, anim_type: str, frames: Dict[Direction, List[Image.Image]]):
        self._animation_cache[anim_type] = frames

    def _get_selected_directions(self) -> List[Direction]:
        return [d for d, cb in self._dir_checks.items() if cb.isChecked()]

    def _on_export(self):
        fmt = self._format_combo.currentText()
        anim = self._anim_combo.currentText()
        directions = self._get_selected_directions()

        if not directions:
            QMessageBox.warning(self, "Export", "Select at least one direction.")
            return

        # Choose save location
        if fmt == "Individual PNGs":
            output_dir = QFileDialog.getExistingDirectory(self, "Choose Export Directory")
            if not output_dir:
                return
        else:
            if fmt == "RPG Maker Sheet":
                path, _ = QFileDialog.getSaveFileName(self, "Save Sprite Sheet", "",
                                                       "PNG Files (*.png)")
            else:  # APNG
                path, _ = QFileDialog.getSaveFileName(self, "Save APNG", "",
                                                       "APNG Files (*.apng *.png)")
            if not path:
                return
            output_dir = None

        self.export_started.emit()
        self._progress.show()
        self._progress.setValue(10)

        try:
            if anim == "(static)":
                self._export_static(fmt, directions, path if output_dir is None else output_dir)
            else:
                self._export_animation(fmt, anim, directions,
                                       path if output_dir is None else output_dir)

            self._progress.setValue(100)
            msg = f"Export complete: {path if output_dir is None else output_dir}"
            self.export_finished.emit(msg)
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))
        finally:
            self._progress.hide()

    def _export_static(self, fmt: str, directions: List[Direction], output: str):
        if fmt == "RPG Maker Sheet":
            # Build dict with single frame per direction
            frames_by_dir = {d: [self._static_renders[d]]
                             for d in directions if d in self._static_renders}
            build_rpg_sheet(frames_by_dir, output)
        elif fmt == "Individual PNGs":
            import os
            os.makedirs(output, exist_ok=True)
            for d in directions:
                if d in self._static_renders:
                    path = os.path.join(output, f"static_{d.value}.png")
                    self._static_renders[d].save(path, "PNG")
        elif fmt == "APNG":
            # Single frame APNG (just a PNG really)
            frames = [self._static_renders[d] for d in directions
                      if d in self._static_renders]
            if frames:
                export_apng(frames, output, duration_ms=500)

    def _export_animation(self, fmt: str, anim_type: str,
                          directions: List[Direction], output: str):
        frames_by_dir = self._animation_cache.get(anim_type, {})
        if not frames_by_dir:
            QMessageBox.warning(self, "Export",
                                f"No animation frames for '{anim_type}'. Generate first.")
            return

        filtered = {d: frames_by_dir[d] for d in directions if d in frames_by_dir}

        if fmt == "RPG Maker Sheet":
            build_rpg_sheet(filtered, output)
        elif fmt == "Individual PNGs":
            export_individual_frames(filtered, output, anim_type)
        elif fmt == "APNG":
            anim_def = ANIMATION_DEFS.get(anim_type)
            duration = anim_def.speed_ms if anim_def else 100
            loop = 0 if (anim_def and anim_def.loop) else 1
            # Concatenate all direction frames
            all_frames = []
            for d in [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]:
                if d in filtered:
                    all_frames.extend(filtered[d])
            if all_frames:
                export_apng(all_frames, output, duration_ms=duration, loop=loop)
