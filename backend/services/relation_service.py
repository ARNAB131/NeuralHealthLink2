# /backend/services/relation_service.py
import hashlib
from backend.services.data_loader import load_relations

# Preload all relation data once
_relations = load_relions = load_relations()


def _normalize(name: str) -> str:
    """Normalize disease names to title case, strip quotes and spaces."""
    if not name:
        return ""
    return name.strip().strip('"').strip("'").title()


def _safe_float(value):
    """Safely convert any value to float, return 0.0 if conversion fails."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def get_relation(present_disease: str, previous_disease: str):
    """
    Return the predefined relation info between two diseases.
    """
    present = _normalize(present_disease)
    previous = _normalize(previous_disease)

    rel = _relations.get(present, {}).get(previous)
    if not rel:
        return {
            "present_disease": present,
            "previous_disease": previous,
            "probability": 0.0,
            "report": "No relation data found between these diseases in mock dataset."
        }

    prob = _safe_float(rel.get("probability", 0))
    report = rel.get("report", "No data available.")

    return {
        "present_disease": present,
        "previous_disease": previous,
        "probability": prob,
        "report": report
    }


def get_all_relations_for_disease(present_disease: str):
    """
    Return all relations for a single present disease.
    key = previous_disease, value = {"probability": float, "report": str}
    """
    present = _normalize(present_disease)
    relations = _relations.get(present, {})
    formatted = {}

    for prev, info in relations.items():
        formatted[_normalize(prev)] = {
            "probability": _safe_float(info.get("probability", 0)),
            "report": info.get("report", "No data available.")
        }

    return formatted


def relation_exists(present_disease: str, previous_disease: str) -> bool:
    """
    Check if a relation pair exists in the dataset.
    """
    present = _normalize(present_disease)
    previous = _normalize(previous_disease)
    return previous in _relations.get(present, {})


def build_state_causal_context(present_disease: str,
                               state: str,
                               state_disease_list,
                               patient_id: str):
    """
    For a given patient, build mock causal percentages between state diseases and present disease.
    Returns a list of dicts:
      [{"disease": "Dengue", "probability": 0.37, "report": "..."}]
    """
    present = _normalize(present_disease)
    results = []

    # Limit to 5 diseases per state for the mock panel
    for sd in state_disease_list[:5]:
        sd_norm = _normalize(sd)

        # Try to get real relation if present
        base_rel = _relations.get(present, {}).get(sd_norm)
        base_prob = _safe_float(base_rel.get("probability", 0)) if base_rel else 0.0
        base_report = base_rel.get("report") if base_rel else None

        # Deterministic pseudo-random component per (patient, state_disease, present_disease)
        key = f"{patient_id}:{state}:{sd_norm}:{present}"
        h = hashlib.sha256(key.encode("utf-8")).hexdigest()
        # Take first few hex chars to generate a number between 0 and 1
        rand_component = int(h[:6], 16) / 0xFFFFFF  # 0–1

        # Blend base relation probability and random component
        # If base_rel exists, bias around it; else just use random
        if base_prob > 0:
            final_prob = 0.5 * base_prob + 0.5 * rand_component
        else:
            final_prob = rand_component

        if base_report:
            report = base_report
        else:
            report = (
                f"In {state}, historical patterns suggest that {sd_norm} can "
                f"contribute to the risk of {present} in certain clinical scenarios (mock model)."
            )

        results.append({
            "disease": sd_norm,
            "probability": final_prob,
            "report": report
        })

    return results
