# config/settings.py
import os
from pathlib import Path

# -------------------------------------------------------
# BASIC APP INFO
# -------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

APP_NAME = "Neural Health Link"
VERSION = "2.0"
AUTHOR = "Arnab Deb"
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
# PLATFORM DETECTION
# -------------------------------------------------------
IS_VERCEL = os.getenv("VERCEL") == "1"

# -------------------------------------------------------
# READ-ONLY SOURCE DATA PATHS
# -------------------------------------------------------
DATA_DIR = BASE_DIR / "data"
PATIENTS_CSV = DATA_DIR / "patients.csv"
DISEASES_CSV = DATA_DIR / "diseases.csv"
RELATIONS_JSON = DATA_DIR / "relations.json"
STATE_DISEASES_JSON = DATA_DIR / "state_diseases.json"
MOCK_HISTORY_DISEASES_JSON = DATA_DIR / "mock_history_diseases.json"
PATIENT_HISTORY_JSON = DATA_DIR / "patient_history.json"

# -------------------------------------------------------
# WRITABLE RUNTIME PATHS
# -------------------------------------------------------
if IS_VERCEL:
    RUNTIME_DIR = Path("/tmp/neural_health_link")
else:
    RUNTIME_DIR = BASE_DIR / "runtime"

RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

WRITABLE_PATIENTS_CSV = RUNTIME_DIR / "patients.csv"
WRITABLE_PATIENT_HISTORY_JSON = RUNTIME_DIR / "patient_history.json"

# -------------------------------------------------------
# TRANSLATIONS
# -------------------------------------------------------
TRANSLATIONS_DIR = DATA_DIR / "translations"
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
    "lep": "Lepcha"
}

# -------------------------------------------------------
# FILE UPLOADS
# -------------------------------------------------------
UPLOAD_DIR = RUNTIME_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# -------------------------------------------------------
# OCR CONFIG
# -------------------------------------------------------
TESSERACT_CMD = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")

# -------------------------------------------------------
# RANDOM MOCK HISTORY GENERATION
# -------------------------------------------------------
RANDOM_HISTORY_COUNT = 5
RANDOM_HISTORY_MIN_DAYS = 30
RANDOM_HISTORY_MAX_DAYS = 1200

# -------------------------------------------------------
# LOGGING
# -------------------------------------------------------
LOG_FILE = RUNTIME_DIR / "app.log"
