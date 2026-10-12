"""Start Arketype Desktop (Catalogue, Create Kristal, Developer Ops).

Windows entrypoint: double-click this file with Python 3.10+ and Tkinter.
UI labels include Primary archetype, Create Kristal and logo-k-ui.png.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from arketype_gui import main

if __name__ == '__main__':
    main()
