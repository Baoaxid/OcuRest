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
