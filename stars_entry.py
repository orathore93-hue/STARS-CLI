"""STARS CLI - PyInstaller entry point"""
import sys
import os

# Add src to path for PyInstaller
if getattr(sys, 'frozen', False):
    # Running as compiled binary
    bundle_dir = sys._MEIPASS
else:
    # Running as script
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(bundle_dir, 'src'))

from stars.cli import main

if __name__ == "__main__":
    main()
