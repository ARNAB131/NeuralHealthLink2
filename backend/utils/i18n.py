# backend/utils/i18n.py
import json
from functools import lru_cache
from pathlib import Path
from config import settings


@lru_cache(maxsize=32)
def _load_lang(lang_code: str) -> dict:
    lang_file = Path(settings.TRANSLATIONS_DIR) / f"{lang_code}.json"
    if not lang_file.exists():
        lang_file = Path(settings.TRANSLATIONS_DIR) / "en.json"
    try:
        with open(lang_file, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def translate(key: str, lang: str) -> str:
    data = _load_lang(lang)
    return data.get(key, key)
