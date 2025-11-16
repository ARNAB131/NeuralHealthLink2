# /backend/services/data_loader.py
import csv
import json
from pathlib import Path
from config import settings


def _resolve(path_str: str) -> Path:
    """Resolve a path relative to project root."""
    return Path(settings.BASE_DIR).joinpath(path_str).resolve()


def load_patients():
    """Load patients from CSV into a list of dicts."""
    patients = []
    path = _resolve(settings.PATIENTS_CSV)
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            patients.append({
                "patient_id": row.get("patient_id", "").strip(),
                "name": row.get("name", "").strip(),
                "age": row.get("age", "").strip(),
                "gender": row.get("gender", "").strip(),
                "city": row.get("city", "").strip(),
                "state": row.get("state", "").strip(),
                "last_visit": row.get("last_visit", "").strip(),
                "present_disease": row.get("present_disease", "").strip(),
                "previous_diseases": row.get("previous_diseases", "").strip()
            })
    return patients


def append_patient(patient: dict):
    """
    Append a new patient row to patients.csv.
    `patient` must contain keys matching CSV header.
    """
    path = _resolve(settings.PATIENTS_CSV)
    # Read header once
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

    # Ensure ordering according to header
    row = [patient.get(col, "") for col in header]

    # Append
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def load_diseases():
    """Load diseases from CSV into a list of dicts."""
    diseases = []
    path = _resolve(settings.DISEASES_CSV)
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            diseases.append({
                "disease_name": row.get("disease_name", "").strip(),
                "category": row.get("category", "").strip(),
                "common_symptoms": row.get("common_symptoms", "").strip(),
                "description": row.get("description", "").strip(),
            })
    return diseases


def load_relations():
    """Load predefined disease relations from JSON."""
    path = _resolve(settings.RELATIONS_JSON)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("[WARN] relations.json not found.")
        return {}
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON in relations.json")
        return {}


def load_state_diseases():
    """
    Load mock state -> [diseases] mapping for all Indian states & UTs.
    """
    path = _resolve(settings.STATE_DISEASES_JSON)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("[WARN] state_diseases.json not found.")
        return {}
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON in state_diseases.json")
        return {}
