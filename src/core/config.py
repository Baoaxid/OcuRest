import json
import os
from dataclasses import dataclass, asdict

CONFIG_FILE = "config.json"

@dataclass
class AppConfig:
    lang: str = "vi"
    custom_sound: str = ""
    muted: bool = False
    work_limit: int = 20 * 60       # Standard work duration in seconds (20 minutes)
    rest_limit: int = 20            # Standard rest duration in seconds (20 seconds)
    afk_timeout: int = 20           # Absence duration triggering work progress reset (20 seconds)
    ear_threshold: float = 0.18     # Eye Aspect Ratio threshold for open-eye classification

class ConfigManager:
    @staticmethod
    def load() -> AppConfig:
        """Loads configuration from disk, falling back to default values if unavailable."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    valid_keys = {k: v for k, v in data.items() if k in AppConfig.__annotations__}
                    return AppConfig(**valid_keys)
            except Exception:
                return AppConfig()
        return AppConfig()

    @staticmethod
    def save(config: AppConfig) -> None:
        """Serializes current configuration state to disk."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(asdict(config), f, ensure_ascii=False, indent=2)
        except Exception as err:
            print(f"[ConfigManager] Failed to persist configuration: {err}")