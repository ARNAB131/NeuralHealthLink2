from backend.services.data_loader import load_relations

_relations = load_relations()

def _normalize(name: str) -> str:
    """Normalize disease names to title case and strip extra spaces/quotes."""
    if not name:
        return ""
    return name.strip().strip('"').strip("'").title()

def _safe_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0

def get_relation(present_disease: str, previous_disease: str):
    present = _normalize(present_disease)
    previous = _normalize(previous_disease)
    rel = _relations.get(present, {}).get(previous)
    if not rel:
        return {
            "present_disease": present,
            "previous_disease": previous,
            "probability": 0.0,
            "report": "No data available."
        }
    return {
        "present_disease": present,
        "previous_disease": previous,
        "probability": _safe_float(rel.get("probability", 0)),
        "report": rel.get("report", "No data available.")
    }

def get_all_relations_for_disease(present_disease: str):
    present = _normalize(present_disease)
    results = {}
    for prev, info in _relations.get(present, {}).items():
        results[_normalize(prev)] = {
            "probability": _safe_float(info.get("probability", 0)),
            "report": info.get("report", "No data available.")
        }
    return results

def relation_exists(present_disease: str, previous_disease: str) -> bool:
    present = _normalize(present_disease)
    previous = _normalize(previous_disease)
    return previous in _relations.get(present, {})
