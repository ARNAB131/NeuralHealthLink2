from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

APP_NAME = "Neural Health Link"
VERSION = "1.0"
AUTHOR = "Doctigo"
DEFAULT_COUNTRY = "India"

HOST = "0.0.0.0"
PORT = 8080
DEBUG = False

DATA_DIR = BASE_DIR / "data"
PATIENTS_CSV = "data/patients.csv"
DISEASES_CSV = "data/diseases.csv"
RELATIONS_JSON = "data/relations.json"
STATE_DISEASES_JSON = "data/state_diseases.json"
