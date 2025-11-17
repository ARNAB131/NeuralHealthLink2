# config/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

APP_NAME = "Neural Health Link"
VERSION = "1.2"

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8080))

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-dev-key")

# ---- Paths ----
DATA_DIR = BASE_DIR / "data"
TRANSLATIONS_DIR = DATA_DIR / "translations"

PATIENTS_CSV = DATA_DIR / "patients.csv"
DISEASES_CSV = DATA_DIR / "diseases.csv"
RELATIONS_JSON = DATA_DIR / "relations.json"
STATE_DISEASES_JSON = DATA_DIR / "state_diseases.json"
MOCK_HISTORY_DISEASES_JSON = DATA_DIR / "mock_history_diseases.json"
PATIENT_HISTORY_JSON = DATA_DIR / "patient_history.json"

UPLOAD_DIR = BASE_DIR / "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---- Languages ----
DEFAULT_LANGUAGE = "en"

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "as": "Assamese",
    "or": "Odia",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "gu": "Gujarati",
    "mr": "Marathi",
    "pa": "Punjabi",
    "ur": "Urdu",
    "kok": "Konkani",
}
