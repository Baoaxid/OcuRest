import sys
import ctypes
from unittest.mock import MagicMock

# Mock matplotlib dependencies required transitively by mediapipe
sys.modules["matplotlib"] = MagicMock()
sys.modules["matplotlib.pyplot"] = MagicMock()

# Set explicit AppUserModelID so Windows displays the correct application icon
try:
    myappid = "baoaxid.ocurest.guardian.1.0"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

import tkinter as tk
from src.core.config import ConfigManager
from src.ui.main_window import MainWindow

def main():
    config = ConfigManager.load()
    root = tk.Tk()
    MainWindow(root, config)
    root.mainloop()

if __name__ == "__main__":
    main()