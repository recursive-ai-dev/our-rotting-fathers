#!/usr/bin/env python3
"""
ROTBORN DARK THEME
==================

The interface remembers the god's colors.
Not designed. Remembered.

Blacks, grays, blood reds. The UI feels like it grew here.
"""

# The palette the interface uses
BACKGROUND = "#0d0b0a"       # Almost black — the void between memories
SURFACE = "#161210"          # Slightly lighter — where things rest
SURFACE_RAISED = "#1e1a18"   # Raised surfaces — panels, cards
BORDER = "#2a2420"           # Borders — barely visible
BORDER_ACCENT = "#3d2e28"    # Accent borders — slightly warmer

TEXT_PRIMARY = "#c8bfb8"     # Primary text — pale, readable
TEXT_SECONDARY = "#7a6e68"   # Secondary text — faded
TEXT_DISABLED = "#3d3530"    # Disabled text — almost gone

ACCENT_RED = "#6b2020"       # Blood red — primary accent
ACCENT_RED_HOVER = "#8b2828" # Hover state
ACCENT_RED_PRESS = "#4a1515" # Pressed state

ACCENT_BONE = "#8b7d6b"      # Bone color — secondary accent
ACCENT_SPORE = "#3d5c3a"     # Spore green — tertiary accent

SCROLLBAR_BG = "#0d0b0a"
SCROLLBAR_HANDLE = "#2a2420"
SCROLLBAR_HOVER = "#3d2e28"


DARK_STYLESHEET = f"""
/* ============================================================
   ROTBORN RECURSION ENGINE - DARK THEME
   The interface remembers the god's colors.
   ============================================================ */

QMainWindow, QDialog, QWidget {{
    background-color: {BACKGROUND};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI", "Ubuntu", "Helvetica Neue", sans-serif;
    font-size: 12px;
}}

/* ---- Panels and Groups ---- */
QGroupBox {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 3px;
    margin-top: 8px;
    padding-top: 8px;
    color: {TEXT_SECONDARY};
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 4px;
    color: {ACCENT_BONE};
    background-color: {BACKGROUND};
}}

/* ---- Buttons ---- */
QPushButton {{
    background-color: {SURFACE_RAISED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_ACCENT};
    border-radius: 2px;
    padding: 5px 12px;
    min-height: 24px;
}}

QPushButton:hover {{
    background-color: {BORDER_ACCENT};
    border-color: {ACCENT_BONE};
    color: {TEXT_PRIMARY};
}}

QPushButton:pressed {{
    background-color: {ACCENT_RED_PRESS};
    border-color: {ACCENT_RED};
}}

QPushButton:disabled {{
    background-color: {SURFACE};
    color: {TEXT_DISABLED};
    border-color: {BORDER};
}}

/* The "Remember" button — primary action */
QPushButton#remember_btn {{
    background-color: {ACCENT_RED};
    color: {TEXT_PRIMARY};
    border: 1px solid {ACCENT_RED_HOVER};
    font-weight: bold;
    letter-spacing: 1px;
    min-height: 32px;
    font-size: 13px;
}}

QPushButton#remember_btn:hover {{
    background-color: {ACCENT_RED_HOVER};
}}

QPushButton#remember_btn:pressed {{
    background-color: {ACCENT_RED_PRESS};
}}

/* ---- Combo Boxes ---- */
QComboBox {{
    background-color: {SURFACE_RAISED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_ACCENT};
    border-radius: 2px;
    padding: 3px 6px;
    min-height: 22px;
}}

QComboBox:hover {{
    border-color: {ACCENT_BONE};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    width: 8px;
    height: 8px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {TEXT_SECONDARY};
}}

QComboBox QAbstractItemView {{
    background-color: {SURFACE_RAISED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_ACCENT};
    selection-background-color: {ACCENT_RED};
    selection-color: {TEXT_PRIMARY};
    outline: none;
}}

/* ---- Spin Boxes ---- */
QSpinBox, QDoubleSpinBox {{
    background-color: {SURFACE_RAISED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_ACCENT};
    border-radius: 2px;
    padding: 3px 6px;
    min-height: 22px;
}}

QSpinBox:hover, QDoubleSpinBox:hover {{
    border-color: {ACCENT_BONE};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    background-color: {BORDER_ACCENT};
    border: none;
    width: 16px;
}}

QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: {ACCENT_BONE};
}}

/* ---- Sliders ---- */
QSlider::groove:horizontal {{
    background-color: {SURFACE_RAISED};
    border: 1px solid {BORDER};
    height: 4px;
    border-radius: 2px;
}}

QSlider::handle:horizontal {{
    background-color: {ACCENT_BONE};
    border: 1px solid {BORDER_ACCENT};
    width: 12px;
    height: 12px;
    margin: -4px 0;
    border-radius: 6px;
}}

QSlider::handle:horizontal:hover {{
    background-color: {ACCENT_RED};
    border-color: {ACCENT_RED_HOVER};
}}

QSlider::sub-page:horizontal {{
    background-color: {ACCENT_RED};
    border-radius: 2px;
}}

/* ---- Check Boxes ---- */
QCheckBox {{
    color: {TEXT_PRIMARY};
    spacing: 6px;
}}

QCheckBox::indicator {{
    width: 14px;
    height: 14px;
    border: 1px solid {BORDER_ACCENT};
    border-radius: 2px;
    background-color: {SURFACE_RAISED};
}}

QCheckBox::indicator:checked {{
    background-color: {ACCENT_RED};
    border-color: {ACCENT_RED_HOVER};
}}

QCheckBox::indicator:hover {{
    border-color: {ACCENT_BONE};
}}

/* ---- Labels ---- */
QLabel {{
    color: {TEXT_PRIMARY};
    background-color: transparent;
}}

QLabel#section_label {{
    color: {ACCENT_BONE};
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
}}

/* ---- Splitter ---- */
QSplitter::handle {{
    background-color: {BORDER};
    width: 2px;
    height: 2px;
}}

QSplitter::handle:hover {{
    background-color: {ACCENT_RED};
}}

/* ---- Scroll Bars ---- */
QScrollBar:vertical {{
    background-color: {SCROLLBAR_BG};
    width: 8px;
    border: none;
}}

QScrollBar::handle:vertical {{
    background-color: {SCROLLBAR_HANDLE};
    border-radius: 4px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {SCROLLBAR_HOVER};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {SCROLLBAR_BG};
    height: 8px;
    border: none;
}}

QScrollBar::handle:horizontal {{
    background-color: {SCROLLBAR_HANDLE};
    border-radius: 4px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {SCROLLBAR_HOVER};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* ---- Menu Bar ---- */
QMenuBar {{
    background-color: {SURFACE};
    color: {TEXT_PRIMARY};
    border-bottom: 1px solid {BORDER};
}}

QMenuBar::item:selected {{
    background-color: {ACCENT_RED};
}}

QMenu {{
    background-color: {SURFACE_RAISED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_ACCENT};
}}

QMenu::item:selected {{
    background-color: {ACCENT_RED};
}}

QMenu::separator {{
    height: 1px;
    background-color: {BORDER};
    margin: 2px 0;
}}

/* ---- Tool Bar ---- */
QToolBar {{
    background-color: {SURFACE};
    border-bottom: 1px solid {BORDER};
    spacing: 2px;
    padding: 2px;
}}

QToolBar QToolButton {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    border: 1px solid transparent;
    border-radius: 2px;
    padding: 3px 8px;
}}

QToolBar QToolButton:hover {{
    background-color: {SURFACE_RAISED};
    border-color: {BORDER_ACCENT};
}}

/* ---- Status Bar ---- */
QStatusBar {{
    background-color: {SURFACE};
    color: {TEXT_SECONDARY};
    border-top: 1px solid {BORDER};
    font-size: 11px;
}}

/* ---- Tab Widget ---- */
QTabWidget::pane {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
}}

QTabBar::tab {{
    background-color: {SURFACE_RAISED};
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER};
    padding: 4px 12px;
    border-bottom: none;
}}

QTabBar::tab:selected {{
    background-color: {SURFACE};
    color: {TEXT_PRIMARY};
    border-bottom: 2px solid {ACCENT_RED};
}}

QTabBar::tab:hover {{
    color: {TEXT_PRIMARY};
}}

/* ---- Line Edit ---- */
QLineEdit {{
    background-color: {SURFACE_RAISED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_ACCENT};
    border-radius: 2px;
    padding: 3px 6px;
    min-height: 22px;
}}

QLineEdit:focus {{
    border-color: {ACCENT_BONE};
}}

/* ---- Progress Bar ---- */
QProgressBar {{
    background-color: {SURFACE_RAISED};
    border: 1px solid {BORDER};
    border-radius: 2px;
    text-align: center;
    color: {TEXT_PRIMARY};
    height: 12px;
}}

QProgressBar::chunk {{
    background-color: {ACCENT_RED};
    border-radius: 2px;
}}

/* ---- Tooltip ---- */
QToolTip {{
    background-color: {SURFACE_RAISED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_ACCENT};
    padding: 4px;
}}
"""


def apply_dark_theme(app):
    """Apply the Rotborn dark theme to a QApplication."""
    app.setStyleSheet(DARK_STYLESHEET)
