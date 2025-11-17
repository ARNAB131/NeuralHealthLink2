# backend/services/data_loader.py
import csv
import json
from pathlib import Path
from config import settings


def _resolve(path) -> Path:
    return Path(path)


def load_patients():
    patients = []
    path = _resolve(settings.PATIENTS_CSV)
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            patients.append(
                {
                    "patient_id": row.get("patient_id", "").strip(),
                    "name": row.get("name", "").strip(),
                    "age": row.get("age", "").strip(),
                    "gender": row.get("gender", "").strip(),
                    "city": row.get("city", "").strip(),
                    "state": row.get("state", "").strip(),
                    "last_visit": row.get("last_visit", "").strip(),
                    "present_disease": row.get("present_disease", "").strip(),
                    "previous_diseases": row.get("previous_diseases", "").strip(),
                }
            )
    return patients


def append_patient(patient: dict):
    path = _resolve(settings.PATIENTS_CSV)
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
    row = [patient.get(col, "") for col in header]
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def load_diseases():
    diseases = []
    path = _resolve(settings.DISEASES_CSV)
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            diseases.append(
                {
                    "disease_name": row.get("disease_name", "").strip(),
                    "category": row.get("category", "").strip(),
                    "common_symptoms": row.get("common_symptoms", "").strip(),
                    "description": row.get("description", "").strip(),
                }
            )
    return diseases


def load_relations():
    path = _resolve(settings.RELATIONS_JSON)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_state_diseases():
    path = _resolve(settings.STATE_DISEASES_JSON)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_mock_history_diseases():
    path = _resolve(settings.MOCK_HISTORY_DISEASES_JSON)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data.get("diseases", [])
    except Exception:
        return []


def load_patient_history():
    path = _resolve(settings.PATIENT_HISTORY_JSON)
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_patient_history(history: dict):
    path = _resolve(settings.PATIENT_HISTORY_JSON)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
