"""
Launcher for ABVCS Studio Desktop Application.
Run: python run_ide.py
"""

import sys
import os
from pathlib import Path

# Ensure root directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from abvcs.gui.studio import main

if __name__ == "__main__":
    main()
