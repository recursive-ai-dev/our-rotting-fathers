#!/usr/bin/env python3
"""
Main Application Entry Point - QApplication setup for the 2D Game Art Generator.
"""

import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("2D Game Art Generator")
    app.setOrganizationName("SwarmGenGameArt")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
