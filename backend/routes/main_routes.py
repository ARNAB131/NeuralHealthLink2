# /backend/routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, abort
from backend.services.data_loader import (
    load_patients,
    load_state_diseases,
    append_patient,
)
from backend.services.relation_service import (
    get_all_relations_for_disease,
    build_state_causal_context,
)
from backend.utils.helpers import get_next_patient_id, generate_mock_vitals, vitals_to_scores
from config import settings

main_bp = Blueprint("main", __name__, template_folder="../../frontend/templates")


@main_bp.route("/")
def home():
    patients = load_patients()
    return render_template(
        "index.html",
        app_name=settings.APP_NAME,
        patients=patients,
    )


@main_bp.route("/register", methods=["GET", "POST"])
def register_patient():
    if request.method == "POST":
        patients = load_patients()
        new_id = get_next_patient_id(patients)

        name = request.form.get("name", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        present_disease = request.form.get("present_disease", "").strip()
        # For mock: we start with empty previous diseases & last_visit
        last_visit = request.form.get("last_visit", "").strip() or "2025-01-01"
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()

        row = {
            "patient_id": str(new_id),
            "name": name,
            "age": age,
            "gender": gender,
            "city": city,
            "state": state,
            "last_visit": last_visit,
            "present_disease": present_disease,
            "previous_diseases": "",
        }

        append_patient(row)
        return redirect(url_for("main.patient_view", patient_id=new_id))

    # GET
    return render_template(
        "register.html",
        app_name=settings.APP_NAME,
    )


@main_bp.route("/patient/<patient_id>")
def patient_view(patient_id):
    # Load latest patients each request
    patients = load_patients()
    patient = None
    for p in patients:
        if str(p.get("patient_id")) == str(patient_id):
            patient = p
            break

    if not patient:
        abort(404)

    # Previous diseases list
    prev_list = [
        d.strip() for d in (patient.get("previous_diseases") or "").split("|") if d.strip()
    ]

    # Core relations between present disease and previous diseases
    all_rel = get_all_relations_for_disease(patient.get("present_disease", ""))
    relation_data = {}
    for prev in prev_list:
        rel = all_rel.get(prev.title())
        if rel:
            relation_data[prev.title()] = rel
        else:
            relation_data[prev.title()] = {
                "probability": 0.0,
                "report": "No data available for this pair in mock dataset."
            }

    # State-based disease context
    state_map = load_state_diseases()
    state_raw = (patient.get("state") or "").strip()
    # Try exact, else title-cased
    state_diseases = (
        state_map.get(state_raw)
        or state_map.get(state_raw.title())
        or []
    )
    state_context = build_state_causal_context(
        present_disease=patient.get("present_disease", ""),
        state=state_raw or "Unknown",
        state_disease_list=state_diseases,
        patient_id=str(patient.get("patient_id")),
    )

    # Vitals (mock prediction system)
    vitals = generate_mock_vitals(str(patient.get("patient_id")))
    vital_scores = vitals_to_scores(vitals)

    # Values for bell-curve chart: probabilities + vital risk scores
    chart_values = [c["probability"] for c in state_context] + vital_scores

    return render_template(
        "report.html",
        app_name=settings.APP_NAME,
        patient=patient,
        relation_data=relation_data,
        state_context=state_context,
        vitals=vitals,
        chart_values=chart_values,
    )
