# backend/utils/helpers.py
from typing import List, Dict
from datetime import datetime, timedelta
from pathlib import Path
import json
import random


def get_next_patient_id(patients: List[Dict]) -> int:
    if not patients:
        return 1
    max_id = 0
    for p in patients:
        try:
            pid = int(str(p.get("patient_id", "0")).strip())
            if pid > max_id:
                max_id = pid
        except ValueError:
            continue
    return max_id + 1


def generate_mock_vitals(patient_id: str) -> Dict:
    pid = int(str(patient_id) or "0")

    heart_rate = 60 + (pid * 7) % 40
    bp_systolic = 100 + (pid * 3) % 40
    bp_diastolic = 60 + (pid * 2) % 25
    spo2 = 94 + (pid * 5) % 6
    temperature = 36.5 + ((pid * 11) % 8) / 10.0

    heart_rate_pred = heart_rate + ((pid * 13) % 5 - 2)
    bp_systolic_pred = bp_systolic + ((pid * 17) % 6 - 3)
    bp_diastolic_pred = bp_diastolic + ((pid * 19) % 5 - 2)
    spo2_pred = max(90, min(99, spo2 + ((pid * 23) % 3 - 1)))
    temperature_pred = round(temperature + ((pid * 29) % 3 - 1) * 0.1, 1)

    return {
        "current": {
            "heart_rate": heart_rate,
            "bp_systolic": bp_systolic,
            "bp_diastolic": bp_diastolic,
            "spo2": spo2,
            "temperature": round(temperature, 1),
        },
        "predicted": {
            "heart_rate": heart_rate_pred,
            "bp_systolic": bp_systolic_pred,
            "bp_diastolic": bp_diastolic_pred,
            "spo2": spo2_pred,
            "temperature": temperature_pred,
        },
    }


def vitals_to_scores(vitals: Dict) -> List[float]:
    cur = vitals.get("current", {})
    scores: List[float] = []

    hr = cur.get("heart_rate")
    if hr is not None:
        scores.append(min(max((hr - 50) / 80.0, 0.0), 1.0))

    sys = cur.get("bp_systolic")
    if sys is not None:
        scores.append(min(max((sys - 90) / 70.0, 0.0), 1.0))

    dia = cur.get("bp_diastolic")
    if dia is not None:
        scores.append(min(max((dia - 60) / 30.0, 0.0), 1.0))

    spo2 = cur.get("spo2")
    if spo2 is not None:
        scores.append(min(max((100 - spo2) / 20.0, 0.0), 1.0))

    temp = cur.get("temperature")
    if temp is not None:
        scores.append(min(max((temp - 36.5) / 2.0, 0.0), 1.0))

    return scores


def generate_auto_history(
    patient_id: str,
    present_disease: str,
    last_visit_str: str,
    master_diseases: List[str],
    count: int = 5,
) -> List[Dict]:
    if not master_diseases:
        return []

    try:
        last_visit = datetime.strptime(last_visit_str, "%Y-%m-%d")
    except Exception:
        last_visit = datetime.now()

    random.seed(f"auto-history-{patient_id}-{present_disease}-{last_visit_str}")
    choices = random.sample(master_diseases, k=min(count, len(master_diseases)))

    history: List[Dict] = []
    for idx, d in enumerate(choices, start=1):
        days_back = random.randint(30 * idx, 180 * idx)
        diag_date = last_visit - timedelta(days=days_back)
        history.append(
            {
                "disease": d,
                "diagnosed_on": diag_date.strftime("%Y-%m-%d"),
                "source": "auto",
            }
        )

    return history
