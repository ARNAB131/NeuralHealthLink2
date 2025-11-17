# config/settings.py
import os
from pathlib import Path

# -------------------------------------------------------
# BASIC APP INFO
# -------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

APP_NAME = "Neural Health Link"
VERSION = "1.1"
AUTHOR = "Doctigo"
DEFAULT_COUNTRY = "India"

# -------------------------------------------------------
# SERVER CONFIG
# -------------------------------------------------------
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8080))
DEBUG = True

# -------------------------------------------------------
# SECURITY
# -------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-dev-key")

# -------------------------------------------------------
# DATA PATHS
# -------------------------------------------------------
DATA_DIR = BASE_DIR / "data"
PATIENTS_CSV = DATA_DIR / "patients.csv"
DISEASES_CSV = DATA_DIR / "diseases.csv"
RELATIONS_JSON = DATA_DIR / "relations.json"
STATE_DISEASES_JSON = DATA_DIR / "state_diseases.json"
MOCK_HISTORY_DISEASES_JSON = DATA_DIR / "mock_history_diseases.json"
PATIENT_HISTORY_JSON = DATA_DIR / "patient_history.json"

# Directory for translation JSON files
TRANSLATIONS_DIR = DATA_DIR / "translations"
TRANSLATIONS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# MULTILINGUAL SETTINGS
# -------------------------------------------------------
# Default UI Language
DEFAULT_LANGUAGE = "en"

# All Indian languages + English
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

    # Additional widely spoken Indian languages
    "raj": "Rajasthani",
    "brx": "Bodo",
    "lmn": "Lambani",
    "hmr": "Hmar",
    "mz": "Mizo",
    "nag": "Nagamese",
    "trp": "Tripuri",
    "gon": "Gondi",
    "kha": "Khasi",
    "grt": "Garo",
    "lep": "Lepcha",
}

# -------------------------------------------------------
# FILE UPLOADS (medical report uploads)
# -------------------------------------------------------
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}

MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# -------------------------------------------------------
# OCR CONFIG (for PDF/JPG medical report reading)
# -------------------------------------------------------
# Path to Tesseract binary (Render/GCP adapt automatically)
TESSERACT_CMD = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")

# -------------------------------------------------------
# EXTRA: PARAMETERS FOR RANDOM MOCK HISTORY GENERATION
# -------------------------------------------------------
RANDOM_HISTORY_COUNT = 5          # generate 5 random past diseases
RANDOM_HISTORY_MIN_DAYS = 30      # at least 30 days older than last visit
RANDOM_HISTORY_MAX_DAYS = 1200    # approx 3 years

# -------------------------------------------------------
# LOGGING (optional, future use)
# -------------------------------------------------------
LOG_FILE = BASE_DIR / "app.log"
