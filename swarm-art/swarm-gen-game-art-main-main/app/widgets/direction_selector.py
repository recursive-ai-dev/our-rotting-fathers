#!/usr/bin/env python3
"""
Direction Selector Widget - 4-direction toggle grid for selecting view direction.
"""

from PyQt6.QtWidgets import (QWidget, QGridLayout, QPushButton, QGroupBox,
                              QVBoxLayout, QLabel)
from PyQt6.QtCore import pyqtSignal
from generator.direction_renderer import Direction


class DirectionSelectorWidget(QWidget):
    """4-direction toggle button grid."""

    direction_changed = pyqtSignal(object)  # Direction enum

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current = Direction.DOWN
        self._buttons = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("Direction")
        grid = QGridLayout()
        grid.setSpacing(2)

        # Arrow-style layout:
        #       UP
        # LEFT DOWN RIGHT
        button_map = {
            Direction.UP:    (0, 1, "UP"),
            Direction.LEFT:  (1, 0, "LEFT"),
            Direction.DOWN:  (1, 1, "DOWN"),
            Direction.RIGHT: (1, 2, "RIGHT"),
        }

        for direction, (row, col, label) in button_map.items():
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setMinimumSize(50, 30)
            btn.clicked.connect(lambda checked, d=direction: self._on_clicked(d))
            grid.addWidget(btn, row, col)
            self._buttons[direction] = btn

        # Set initial state
        self._buttons[Direction.DOWN].setChecked(True)

        group.setLayout(grid)
        layout.addWidget(group)

    def _on_clicked(self, direction: Direction):
        self._current = direction
        # Update button states
        for d, btn in self._buttons.items():
            btn.setChecked(d == direction)
        self.direction_changed.emit(direction)

    def current_direction(self) -> Direction:
        return self._current
