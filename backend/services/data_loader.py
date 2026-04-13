# backend/services/data_loader.py
import csv
import json
import shutil
from pathlib import Path
from config import settings


def _ensure_seed_file(source_path: Path, writable_path: Path, empty_default: str = "") -> Path:
    """
    Ensure a writable runtime copy exists.
    If not present, copy from bundled read-only source.
    If source is missing, create empty_default.
    """
    writable_path.parent.mkdir(parents=True, exist_ok=True)

    if writable_path.exists():
        return writable_path

    if source_path.exists():
        shutil.copyfile(source_path, writable_path)
        return writable_path

    writable_path.write_text(empty_default, encoding="utf-8")
    return writable_path


def _patients_runtime_path() -> Path:
    return _ensure_seed_file(
        source_path=settings.PATIENTS_CSV,
        writable_path=settings.WRITABLE_PATIENTS_CSV,
        empty_default=(
            "patient_id,name,age,gender,city,state,last_visit,present_disease,previous_diseases\n"
        ),
    )


def _patient_history_runtime_path() -> Path:
    return _ensure_seed_file(
        source_path=settings.PATIENT_HISTORY_JSON,
        writable_path=settings.WRITABLE_PATIENT_HISTORY_JSON,
        empty_default="{}",
    )


def load_patients():
    """
    Load patients from writable runtime CSV.
    On first run, this is seeded from data/patients.csv.
    """
    patients = []
    path = _patients_runtime_path()

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
    """
    Append a new patient row to the writable runtime CSV.
    """
    path = _patients_runtime_path()

    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            header = [
                "patient_id",
                "name",
                "age",
                "gender",
                "city",
                "state",
                "last_visit",
                "present_disease",
                "previous_diseases",
            ]

    row = [patient.get(col, "") for col in header]

    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def load_diseases():
    """
    Load diseases from bundled read-only CSV.
    """
    diseases = []
    path = Path(settings.DISEASES_CSV)

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
    """
    Load bundled read-only relations JSON.
    """
    path = Path(settings.RELATIONS_JSON)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_state_diseases():
    """
    Load bundled read-only state disease JSON.
    """
    path = Path(settings.STATE_DISEASES_JSON)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_mock_history_diseases():
    """
    Load bundled read-only 50+ disease pool.
    """
    path = Path(settings.MOCK_HISTORY_DISEASES_JSON)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data.get("diseases", [])
    except Exception:
        return []


def load_patient_history():
    """
    Load writable runtime patient history JSON.
    """
    path = _patient_history_runtime_path()
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_patient_history(history: dict):
    """
    Save patient history to writable runtime JSON.
    """
    path = _patient_history_runtime_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
