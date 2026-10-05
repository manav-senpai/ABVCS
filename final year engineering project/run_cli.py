"""
Entrypoint script to run ABVCS CLI commands directly from source.
"""

import sys
import os

# Ensure project root is on PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from abvcs.cli.main import main

if __name__ == "__main__":
    main()
