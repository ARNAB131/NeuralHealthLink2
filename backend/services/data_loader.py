import csv
import json
from config import settings


def load_patients():
    """Load mock Indian patients from CSV."""
    patients = []
    try:
        with open(settings.PATIENTS_CSV, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                patients.append({
                    "patient_id": row["patient_id"],
                    "name": row["name"],
                    "age": row["age"],
                    "gender": row["gender"],
                    "city": row["city"],
                    "state": row["state"],
                    "last_visit": row["last_visit"],
                    "present_disease": row["present_disease"],
                    "previous_diseases": row.get("previous_diseases", "")
                })
    except FileNotFoundError:
        print("[WARN] patients.csv not found.")
    return patients


def load_diseases():
    """Load base disease definitions and symptoms from CSV."""
    diseases = []
    try:
        with open(settings.DISEASES_CSV, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                diseases.append({
                    "disease_name": row["disease_name"],
                    "category": row["category"],
                    "common_symptoms": row["common_symptoms"].split("|"),
                    "description": row["description"]
                })
    except FileNotFoundError:
        print("[WARN] diseases.csv not found.")
    return diseases


def load_relations():
    """Load predefined disease relations from JSON."""
    try:
        with open(settings.RELATIONS_JSON, encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("[WARN] relations.json not found.")
        return {}
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON in relations.json")
        return {}
