from flask import Blueprint, render_template, request
from backend.services.data_loader import load_patients, load_relations
from config import settings

# Blueprint
main_bp = Blueprint("main", __name__)

# Cached mock data
patients = load_patients()
relations = load_relations()


@main_bp.route("/")
def home():
    """Homepage with patient selector."""
    return render_template(
        "index.html",
        patients=patients,
        app_name=settings.APP_NAME
    )


@main_bp.route("/patient/<patient_id>")
def patient_view(patient_id):
    """Display a single patient's disease relations."""
    patient = next((p for p in patients if p["patient_id"] == patient_id), None)
    if not patient:
        return render_template("error.html", message="Patient not found.")

    present = patient["present_disease"]
    prev_list = patient["previous_diseases"].split("|") if patient["previous_diseases"] else []

    relation_data = {}
    for prev in prev_list:
        prob = relations.get(present, {}).get(prev, {}).get("probability", "N/A")
        report = relations.get(present, {}).get(prev, {}).get("report", "No data available.")
        relation_data[prev] = {"probability": prob, "report": report}

    return render_template(
        "report.html",
        patient=patient,
        relation_data=relation_data,
        app_name=settings.APP_NAME
    )


@main_bp.route("/about")
def about():
    """Simple About page."""
    return render_template(
        "about.html",
        app_name=settings.APP_NAME,
        version=settings.VERSION,
        author=settings.AUTHOR
    )
