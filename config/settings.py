import os

# Base application settings
APP_NAME = "Neural Health Link"
VERSION = "1.0"

# Hosting / Server config
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8080))
DEBUG = True

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-dev-key")  # <-- ADD THIS

# Default metadata
AUTHOR = "Doctigo"
DEFAULT_COUNTRY = "India"

# Data paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

PATIENTS_CSV = os.path.join(DATA_DIR, "patients.csv")
DISEASES_CSV = os.path.join(DATA_DIR, "diseases.csv")
RELATIONS_JSON = os.path.join(DATA_DIR, "relations.json")
STATE_DISEASES_JSON = os.path.join(DATA_DIR, "state_diseases.json")  # new
