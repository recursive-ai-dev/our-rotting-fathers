#!/usr/bin/env python3
"""
ROTBORN RECURSION ENGINE - Application Entry Point
"""

import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow
from app.dark_theme import apply_dark_theme


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Rotborn Recursion Engine")
    app.setOrganizationName("RotbornRecursion")

    apply_dark_theme(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
