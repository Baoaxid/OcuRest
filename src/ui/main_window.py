import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image
import pystray

from src.core.config import AppConfig, ConfigManager
from src.core.resources import resolve_resource_path
from src.ui.i18n import I18nManager
from src.vision.tracker import VisionTracker
from src.platform.win32_idle import get_system_idle_seconds
from src.audio.player import AudioPlayer

class MainWindow:
    def __init__(self, root: tk.Tk, config: AppConfig):
        self.root = root
        self.config = config
        self.i18n = I18nManager(default_lang=self.config.lang)
        self.audio = AudioPlayer()
        self.tracker = VisionTracker(ear_threshold=self.config.ear_threshold)

        # Execution mode toggle: Camera tracking vs. Input idle fallback
        self.use_camera_mode = self.tracker.has_camera

        self.root.title(self.i18n.t("app.title"))
        self.root.geometry("400x310")
        self.root.resizable(False, False)

        # Apply application icon
        self._apply_window_icon()

        # State machine identifiers: WORKING, WORK_DONE, RESTING, REST_DONE
        self.state = "WORKING"
        self.work_accumulated = 0.0
        self.rest_accumulated = 0.0
        self.afk_duration = 0.0

        self.setup_ui()

        # System tray setup
        self.tray_icon = None
        self.setup_tray_icon()

        # Intercept window close event to hide into tray instead of exiting
        self.root.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

        # Background monitoring thread
        self.running = True
        self.worker_thread = threading.Thread(target=self.tracking_loop, daemon=True)
        self.worker_thread.start()

    def _apply_window_icon(self) -> None:
        """Sets application window icon handling multi-environment resolution."""
        icon_path = resolve_resource_path("assets/icon.ico")
        if icon_path.exists():
            try:
                self.root.iconbitmap(default=str(icon_path))
            except Exception as err:
                print(f"[MainWindow] Failed to set window icon: {err}")

    def setup_tray_icon(self) -> None:
        """Initializes system tray icon running in a detached background thread."""
        icon_path = resolve_resource_path("assets/icon.ico")
        image = Image.open(icon_path) if icon_path.exists() else Image.new("RGBA", (64, 64), "#0f766e")

        menu = pystray.Menu(
            pystray.MenuItem("Mở OcuRest", self.show_window, default=True),
            pystray.MenuItem("Thoát", self.quit_application)
        )
        self.tray_icon = pystray.Icon("OcuRest", image, "OcuRest - 20-20-20 Guardian", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def hide_to_tray(self) -> None:
        """Hides the main window from the screen and taskbar."""
        self.root.withdraw()

    def show_window(self, icon=None, item=None) -> None:
        """Restores and focuses the main window from system tray."""
        self.root.after(0, self._restore_window)

    def _restore_window(self) -> None:
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def quit_application(self, icon=None, item=None) -> None:
        """Completely terminates the application process."""
        self.running = False
        if self.tray_icon:
            self.tray_icon.stop()
        self.audio.stop()
        self.tracker.release()
        self.root.after(0, self.root.destroy)
        sys.exit(0)

    def setup_ui(self) -> None:
        """Initializes and arranges GUI components."""
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=6)

        tk.Label(top_frame, text="Language / Ngôn ngữ:").pack(side=tk.LEFT)
        self.combo_lang = ttk.Combobox(top_frame, values=["Tiếng Việt", "English"], state="readonly", width=12)
        self.combo_lang.set("Tiếng Việt" if self.config.lang == "vi" else "English")
        self.combo_lang.bind("<<ComboboxSelected>>", self.on_change_language)
        self.combo_lang.pack(side=tk.RIGHT)

        self.lbl_status = tk.Label(self.root, text=self.i18n.t("mode.work"), font=("Segoe UI", 12, "bold"))
        self.lbl_status.pack(pady=4)

        self.lbl_timer = tk.Label(self.root, text="00:00 / 20:00", font=("Consolas", 18))
        self.lbl_timer.pack(pady=2)

        self.lbl_subtext = tk.Label(self.root, text=self.i18n.t("subtext.work_active"), fg="#555555", font=("Segoe UI", 9))
        self.lbl_subtext.pack(pady=2)

        self.btn_toggle_source = tk.Button(
            self.root, 
            text=self.get_source_label(), 
            command=self.toggle_tracking_mode, 
            fg="#0055aa", 
            relief=tk.FLAT, 
            font=("Segoe UI", 8, "underline")
        )
        self.btn_toggle_source.pack(pady=4)

        audio_frame = tk.Frame(self.root)
        audio_frame.pack(pady=6)

        mute_key = "controls.sound_off" if self.config.muted else "controls.sound_on"
        self.btn_mute = tk.Button(audio_frame, text=self.i18n.t(mute_key), command=self.toggle_mute, width=15)
        self.btn_mute.pack(side=tk.LEFT, padx=4)

        self.btn_sound_file = tk.Button(audio_frame, text=self.i18n.t("controls.choose_sound"), command=self.pick_sound_file, width=15)
        self.btn_sound_file.pack(side=tk.LEFT, padx=4)

        sound_name = os.path.basename(self.config.custom_sound) if self.config.custom_sound else self.i18n.t("controls.default_sound")
        self.lbl_sound_name = tk.Label(self.root, text=f"File: {sound_name}", fg="#444444", font=("Segoe UI", 8))
        self.lbl_sound_name.pack(pady=2)

    def get_source_label(self) -> str:
        if self.use_camera_mode and self.tracker.has_camera:
            return self.i18n.t("source.camera") + " [Nhấn để đổi]"
        return self.i18n.t("source.fallback") + " [Nhấn để đổi]"

    def toggle_tracking_mode(self) -> None:
        """Toggles between Camera Vision and Keyboard/Mouse input tracking."""
        if not self.use_camera_mode and not self.tracker.has_camera:
            messagebox.showwarning("Warning", "No operational webcam detected on this system.")
            return
        self.use_camera_mode = not self.use_camera_mode
        self.btn_toggle_source.config(text=self.get_source_label())

    def on_change_language(self, _) -> None:
        selected = self.combo_lang.get()
        self.config.lang = "vi" if selected == "Tiếng Việt" else "en"
        self.i18n.set_language(self.config.lang)
        ConfigManager.save(self.config)
        self.refresh_ui()

    def refresh_ui(self) -> None:
        """Synchronizes GUI labels with updated localization settings."""
        self.root.title(self.i18n.t("app.title"))
        status_key = "mode.work" if self.state in ["WORKING", "WORK_DONE"] else "mode.rest"
        self.lbl_status.config(text=self.i18n.t(status_key))
        self.btn_toggle_source.config(text=self.get_source_label())
        mute_key = "controls.sound_off" if self.config.muted else "controls.sound_on"
        self.btn_mute.config(text=self.i18n.t(mute_key))
        self.btn_sound_file.config(text=self.i18n.t("controls.choose_sound"))
        sound_name = os.path.basename(self.config.custom_sound) if self.config.custom_sound else self.i18n.t("controls.default_sound")
        self.lbl_sound_name.config(text=f"File: {sound_name}")

    def toggle_mute(self) -> None:
        self.config.muted = not self.config.muted
        ConfigManager.save(self.config)
        mute_key = "controls.sound_off" if self.config.muted else "controls.sound_on"
        self.btn_mute.config(text=self.i18n.t(mute_key))
        if self.config.muted:
            self.audio.stop()

    def pick_sound_file(self) -> None:
        selected_file = filedialog.askopenfilename(
            title="Select Alert Audio",
            filetypes=[("Audio Files", "*.wav;*.mp3"), ("All Files", "*.*")]
        )
        if selected_file:
            self.config.custom_sound = selected_file
            ConfigManager.save(self.config)
            self.lbl_sound_name.config(text=f"File: {os.path.basename(selected_file)}")

    def tracking_loop(self) -> None:
        """Periodic monitoring thread executed at 1.0 Hz."""
        while self.running:
            loop_start = time.time()
            idle_sec = get_system_idle_seconds()

            if self.state == "WORKING":
                user_active = False
                if self.use_camera_mode and self.tracker.has_camera:
                    is_facing, is_open = self.tracker.inspect_frame()
                    user_active = is_facing and is_open
                else:
                    user_active = idle_sec < 5.0

                if user_active:
                    self.work_accumulated += 1.0
                    self.afk_duration = 0.0
                    self.lbl_subtext.config(text=self.i18n.t("subtext.work_active"))
                else:
                    self.afk_duration += 1.0
                    if self.afk_duration >= self.config.afk_timeout:
                        self.work_accumulated = 0.0
                        self.afk_duration = 0.0
                    self.lbl_subtext.config(text=self.i18n.t("subtext.work_paused", sec=int(self.afk_duration)))

                mins, secs = divmod(int(self.work_accumulated), 60)
                self.lbl_timer.config(text=f"{mins:02d}:{secs:02d} / 20:00")

                if self.work_accumulated >= self.config.work_limit:
                    self.state = "WORK_DONE"
                    self.root.after(0, self.trigger_break_prompt)

            elif self.state == "RESTING":
                is_resting = False
                if self.use_camera_mode and self.tracker.has_camera:
                    is_facing, is_open = self.tracker.inspect_frame()
                    is_resting = (not is_facing) or (not is_open)
                else:
                    is_resting = idle_sec >= 1.0

                if is_resting:
                    self.rest_accumulated += 1.0
                else:
                    self.rest_accumulated = 0.0

                self.lbl_timer.config(text=f"{int(self.rest_accumulated):02d}s / 20s")
                rule_key = "subtext.rest_camera" if (self.use_camera_mode and self.tracker.has_camera) else "subtext.rest_fallback"
                self.lbl_subtext.config(text=self.i18n.t(rule_key))

                if self.rest_accumulated >= self.config.rest_limit:
                    self.state = "REST_DONE"
                    self.root.after(0, self.trigger_resume_prompt)

            elapsed = time.time() - loop_start
            time.sleep(max(0.0, 1.0 - elapsed))

    def trigger_break_prompt(self) -> None:
        """Displays modal dialogue when work interval is completed."""
        self._restore_window()
        self.audio.start_loop(self.config.custom_sound, self.config.muted)
        self.root.attributes("-topmost", True)
        
        using_cam = self.use_camera_mode and self.tracker.has_camera
        msg_key = "alert.work_camera" if using_cam else "alert.work_fallback"
        messagebox.showinfo(self.i18n.t("alert.work_title"), self.i18n.t(msg_key))
        
        self.audio.stop()
        self.root.attributes("-topmost", False)

        self.work_accumulated = 0.0
        self.rest_accumulated = 0.0
        self.afk_duration = 0.0
        self.state = "RESTING"
        self.lbl_status.config(text=self.i18n.t("mode.rest"))

    def trigger_resume_prompt(self) -> None:
        """Displays modal dialogue when rest interval is completed."""
        self._restore_window()
        self.audio.start_loop(self.config.custom_sound, self.config.muted)
        self.root.attributes("-topmost", True)
        messagebox.showinfo(self.i18n.t("alert.rest_title"), self.i18n.t("alert.rest_msg"))
        self.audio.stop()
        self.root.attributes("-topmost", False)

        self.rest_accumulated = 0.0
        self.work_accumulated = 0.0
        self.afk_duration = 0.0
        self.state = "WORKING"
        self.lbl_status.config(text=self.i18n.t("mode.work"))