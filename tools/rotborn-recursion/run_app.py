#!/usr/bin/env python3
"""Convenience launcher for the 2D Game Art Generator GUI."""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == "__main__":
    main()
