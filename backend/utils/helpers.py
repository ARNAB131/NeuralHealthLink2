import math
from datetime import datetime
from config import settings


def format_percentage(prob_value):
    """
    Convert a float probability (0–1) to a clean percentage string.
    """
    if prob_value is None or prob_value == "N/A":
        return "N/A"
    try:
        return f"{float(prob_value) * 100:.1f}%"
    except (ValueError, TypeError):
        return "N/A"


def normalize_disease_name(name: str) -> str:
    """
    Normalize disease names for consistent lookups.
    Example: ' fever ' -> 'Fever'
    """
    return name.strip().title() if isinstance(name, str) else name


def format_date(date_str):
    """
    Format YYYY-MM-DD into a readable date (e.g., 2025-10-24 → 24 Oct 2025)
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%d %b %Y")
    except Exception:
        return date_str


def combine_relations(relations_dict):
    """
    Prepare a user-friendly list from relation dict {disease: {prob, report}}
    """
    formatted = []
    for disease, info in relations_dict.items():
        formatted.append({
            "previous_disease": disease,
            "probability": format_percentage(info.get("probability")),
            "report": info.get("report", "")
        })
    return formatted


def get_state_flag(state_name):
    """
    Return a placeholder flag icon path for Indian states (mock).
    """
    base = "/static/images/icons/states/"
    safe_name = state_name.lower().replace(" ", "_")
    return f"{base}{safe_name}.png"


def round_up(num, decimals=2):
    """
    Round a numeric value safely upward to given decimals.
    """
    try:
        factor = 10 ** decimals
        return math.ceil(num * factor) / factor
    except Exception:
        return num


def get_app_info():
    """
    Return app metadata for templates or APIs.
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "author": settings.AUTHOR,
        "country": settings.DEFAULT_COUNTRY
    }
