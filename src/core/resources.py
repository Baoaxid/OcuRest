import sys
from pathlib import Path

def resolve_resource_path(relative_path: str) -> Path:
    """
    Resolves absolute path to resource, handling both development 
    and PyInstaller runtime environments.
    """
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent.parent
    return base_path / relative_path