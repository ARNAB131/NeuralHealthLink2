# backend/services/relation_service.py
import hashlib
from backend.services.data_loader import load_relations

_relations = load_relations()


def _normalize(name: str) -> str:
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
            "report": "No relation data found between these diseases in mock dataset.",
        }
    return {
        "present_disease": present,
        "previous_disease": previous,
        "probability": _safe_float(rel.get("probability", 0)),
        "report": rel.get("report", "No data available."),
    }


def get_all_relations_for_disease(present_disease: str):
    present = _normalize(present_disease)
    out = {}
    for prev, info in _relations.get(present, {}).items():
        out[_normalize(prev)] = {
            "probability": _safe_float(info.get("probability", 0)),
            "report": info.get("report", "No data available."),
        }
    return out


def relation_exists(present_disease: str, previous_disease: str) -> bool:
    present = _normalize(present_disease)
    previous = _normalize(previous_disease)
    return previous in _relations.get(present, {})


def build_state_causal_context(present_disease: str, state: str, state_diseases, patient_id: str):
    present = _normalize(present_disease)
    results = []
    for sd in state_diseases[:5]:
        sd_norm = _normalize(sd)
        base_rel = _relations.get(present, {}).get(sd_norm)
        base_prob = _safe_float(base_rel.get("probability", 0)) if base_rel else 0.0
        base_report = base_rel.get("report") if base_rel else None

        key = f"state:{patient_id}:{state}:{sd_norm}:{present}"
        h = hashlib.sha256(key.encode("utf-8")).hexdigest()
        rand_component = int(h[:6], 16) / 0xFFFFFF

        if base_prob > 0:
            final_prob = 0.5 * base_prob + 0.5 * rand_component
        else:
            final_prob = rand_component

        if base_report:
            report = base_report
        else:
            report = (
                f"In {state}, {sd_norm} can act as a background contributor to {present} "
                f"under certain clinical scenarios (mock model)."
            )

        results.append(
            {
                "disease": sd_norm,
                "probability": final_prob,
                "report": report,
            }
        )
    return results


def build_mock_causal_probability(present_disease: str, previous_disease: str, patient_id: str, extra_key: str = ""):
    """
    Deterministic pseudo-random probability for auto/report history diseases.
    """
    present = _normalize(present_disease)
    previous = _normalize(previous_disease)
    base_rel = _relations.get(present, {}).get(previous)
    base_prob = _safe_float(base_rel.get("probability", 0)) if base_rel else 0.0

    key = f"hist:{patient_id}:{present}:{previous}:{extra_key}"
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()
    rand_component = int(h[:6], 16) / 0xFFFFFF

    if base_prob > 0:
        final_prob = 0.6 * base_prob + 0.4 * rand_component
    else:
        final_prob = rand_component

    return final_prob
