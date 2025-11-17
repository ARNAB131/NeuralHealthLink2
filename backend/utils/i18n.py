# backend/utils/i18n.py
import json
from functools import lru_cache
from config import settings

@lru_cache(maxsize=64)
def load_language(lang: str) -> dict:
    lang_file = settings.TRANSLATIONS_DIR / f"{lang}.json"
    if not lang_file.exists():
        lang_file = settings.TRANSLATIONS_DIR / "en.json"

    try:
        return json.loads(lang_file.read_text(encoding="utf-8"))
    except:
        return {}

def translate(key: str, lang: str = "en") -> str:
    table = load_language(lang)
    return table.get(key, key)
