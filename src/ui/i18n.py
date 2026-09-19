import json
import os
import sys
from pathlib import Path
from typing import Optional

class I18nManager:
    def __init__(self, default_lang: str = "vi"):
        self.current_lang = default_lang
        self.translations: dict = {}
        self.locales_dir = self._resolve_locales_path()
        self.load_all_translations()

    def _resolve_locales_path(self) -> Path:
        if getattr(sys, "frozen", False):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).resolve().parent.parent.parent
        return base_path / "locales"

    def load_all_translations(self) -> None:
        self.translations.clear()
        if not self.locales_dir.exists():
            return

        for locale_path in self.locales_dir.iterdir():
            if locale_path.is_dir():
                lang_code = locale_path.name
                self.translations[lang_code] = {}
                for json_file in locale_path.glob("*.json"):
                    try:
                        with open(json_file, "r", encoding="utf-8") as f:
                            self._merge_dicts(self.translations[lang_code], json.load(f))
                    except Exception as err:
                        print(f"[I18n] Error loading {json_file}: {err}")

    def _merge_dicts(self, base: dict, overlay: dict) -> None:
        for k, v in overlay.items():
            if isinstance(v, dict) and k in base and isinstance(base[k], dict):
                self._merge_dicts(base[k], v)
            else:
                base[k] = v

    def set_language(self, lang: str) -> None:
        self.current_lang = lang

    def t(self, key_path: str, **kwargs) -> str:
        val = self._resolve_key(self.current_lang, key_path)
        if val is None and self.current_lang != "en":
            val = self._resolve_key("en", key_path)

        if val is None:
            return key_path

        if kwargs:
            try:
                return val.format(**kwargs)
            except KeyError:
                return val
        return str(val)

    def _resolve_key(self, lang: str, key_path: str) -> Optional[str]:
        current = self.translations.get(lang, {})
        for k in key_path.split("."):
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        return current if isinstance(current, str) else None
