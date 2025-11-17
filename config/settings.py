# config/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

APP_NAME = "Neural Health Link"
VERSION = "1.1"
AUTHOR = "Doctigo"
DEFAULT_COUNTRY = "India"

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8080))
DEBUG = True

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-dev-key")

DATA_DIR = BASE_DIR / "data"
PATIENTS_CSV = DATA_DIR / "patients.csv"
DISEASES_CSV = DATA_DIR / "diseases.csv"
RELATIONS_JSON = DATA_DIR / "relations.json"
STATE_DISEASES_JSON = DATA_DIR / "state_diseases.json"
MOCK_HISTORY_DISEASES_JSON = DATA_DIR / "mock_history_diseases.json"
PATIENT_HISTORY_JSON = DATA_DIR / "patient_history.json"

TRANSLATIONS_DIR = DATA_DIR / "translations"
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = {
    "en": "English",

    # 22 Official Indian Languages
    "hi": "Hindi",
    "bn": "Bengali",
    "as": "Assamese",
    "or": "Odia",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "mr": "Marathi",
    "ne": "Nepali",
    "ks": "Kashmiri",
    "kok": "Konkani",
    "mai": "Maithili",
    "sd": "Sindhi",
    "ur": "Urdu",
    "sa": "Sanskrit",
    "bo": "Tibetan",
    "mni": "Manipuri",
    "bho": "Bhojpuri",
    "doi": "Dogri",
    "sat": "Santali",
    "raj": "Rajasthani",   # Widely spoken, not Eighth Schedule but needed

    # Additional Indian languages (non-official but widely spoken)
    "brx": "Bodo",
    "lmn": "Lambani",
    "hmr": "Hmar",
    "mz": "Mizo",
    "nag": "Nagamese",
    "trp": "Tripuri",
    "gon": "Gondi",
    "kha": "Khasi",
    "grt": "Garo",
    "lep": "Lepcha"
}

UPLOAD_DIR = BASE_DIR / "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
