import os
import time
import threading
import ctypes
import winsound

winmm = ctypes.windll.winmm

class AudioPlayer:
    def __init__(self):
        self.is_playing = False

    def start_loop(self, sound_path: str, is_muted: bool) -> None:
        if is_muted or self.is_playing:
            return
        self.is_playing = True

        target_fn = self._play_mci_loop if (sound_path and os.path.exists(sound_path)) else self._play_beep_loop
        threading.Thread(target=target_fn, args=(sound_path,), daemon=True).start()

    def stop(self) -> None:
        self.is_playing = False
        winmm.mciSendStringW('stop ocurest_audio', None, 0, None)
        winmm.mciSendStringW('close ocurest_audio', None, 0, None)

    def _play_mci_loop(self, sound_path: str) -> None:
        safe_path = sound_path.replace("\\", "/")
        winmm.mciSendStringW('close ocurest_audio', None, 0, None)
        open_cmd = f'open "{safe_path}" type mpegvideo alias ocurest_audio'
        if winmm.mciSendStringW(open_cmd, None, 0, None) == 0:
            while self.is_playing:
                winmm.mciSendStringW('play ocurest_audio from 0', None, 0, None)
                status = ctypes.create_unicode_buffer(128)
                while self.is_playing:
                    winmm.mciSendStringW('status ocurest_audio mode', status, 128, None)
                    if status.value == "stopped":
                        break
                    time.sleep(0.3)
            self.stop()
        else:
            self._play_beep_loop(sound_path)

    def _play_beep_loop(self, _) -> None:
        while self.is_playing:
            winsound.Beep(1000, 300)
            time.sleep(0.2)
