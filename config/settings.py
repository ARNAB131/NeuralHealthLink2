import os

# === Root directory ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# === Data paths ===
DATA_DIR = os.path.join(BASE_DIR, "data")

PATIENTS_CSV = os.path.join(DATA_DIR, "patients.csv")
DISEASES_CSV = os.path.join(DATA_DIR, "diseases.csv")
RELATIONS_JSON = os.path.join(DATA_DIR, "relations.json")

# === App meta ===
APP_NAME = "Neural Health Link (Mock)"
VERSION = "1.0"
AUTHOR = "Arnab Deb"
DEBUG = True

# === Flask settings ===
HOST = "0.0.0.0"
PORT = 5000
SECRET_KEY = "change_this_for_prod"

# === UI config ===
DEFAULT_THEME = "light"
LOGO_PATH = "/static/images/logo.png"

# === Localization ===
DEFAULT_COUNTRY = "India"
DATE_FORMAT = "%Y-%m-%d"

# === Misc ===
CACHE_TIMEOUT = 300  # seconds
MAX_RELATION_DEPTH = 3  # A, B, C combinations limit
