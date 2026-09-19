import ctypes

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

GetTickCount = ctypes.windll.kernel32.GetTickCount
GetTickCount.restype = ctypes.c_uint32

def get_system_idle_seconds() -> float:
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        current_tick = GetTickCount()
        # Handle 32-bit unsigned overflow
        elapsed_ms = (current_tick - lii.dwTime) & 0xFFFFFFFF
        return elapsed_ms / 1000.0
    return 0.0
