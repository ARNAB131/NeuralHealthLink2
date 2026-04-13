# backend/routes/main_routes.py
from pathlib import Path

from flask import Blueprint, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

from backend.services.data_loader import (
    load_patients,
    load_state_diseases,
    append_patient,
    load_mock_history_diseases,
    load_patient_history,
    save_patient_history,
)
from backend.services.relation_service import (
    get_all_relations_for_disease,
    build_state_causal_context,
    build_mock_causal_probability,
)
from backend.utils.helpers import (
    get_next_patient_id,
    generate_mock_vitals,
    vitals_to_scores,
    generate_auto_history,
)
from config import settings

main_bp = Blueprint("main", __name__, template_folder="../../frontend/templates")


@main_bp.route("/")
def home():
    patients = load_patients()
    return render_template("index.html", patients=patients)


@main_bp.route("/register", methods=["GET", "POST"])
def register_patient():
    if request.method == "POST":
        patients = load_patients()
        new_id = get_next_patient_id(patients)

        name = request.form.get("name", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        present_disease = request.form.get("present_disease", "").strip()
        last_visit = request.form.get("last_visit", "").strip() or "2025-01-01"
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()

        # Auto history from mock 50+ diseases
        master_diseases = load_mock_history_diseases()
        auto_history = generate_auto_history(
            patient_id=str(new_id),
            present_disease=present_disease,
            last_visit_str=last_visit,
            master_diseases=master_diseases,
            count=5,
        )

        # Upload parsing: store temporary file in writable UPLOAD_DIR (/tmp on Vercel)
        report_file = request.files.get("report_file")
        report_history = []

        if report_file and report_file.filename:
            filename = secure_filename(report_file.filename)
            ext = filename.lower().rsplit(".", 1)[-1]

            if ext in settings.ALLOWED_EXTENSIONS:
                upload_path = Path(settings.UPLOAD_DIR) / f"{new_id}_{filename}"
                report_file.save(upload_path)

                if ext == "pdf":
                    try:
                        reader = PdfReader(str(upload_path))
                        text = ""
                        for page in reader.pages:
                            text += "\n" + (page.extract_text() or "")

                        lower_text = text.lower()
                        for d in master_diseases:
                            if d.lower() in lower_text:
                                report_history.append(
                                    {
                                        "disease": d,
                                        "diagnosed_on": last_visit,
                                        "source": "upload",
                                    }
                                )
                    except Exception:
                        pass

                elif ext in ("jpg", "jpeg", "png"):
                    # OCR intentionally skipped in this lightweight Vercel-safe patch.
                    # You can add OCR later using an external service or /tmp flow.
                    pass

        previous_disease_names = [h["disease"] for h in auto_history + report_history]

        row = {
            "patient_id": str(new_id),
            "name": name,
            "age": age,
            "gender": gender,
            "city": city,
            "state": state,
            "last_visit": last_visit,
            "present_disease": present_disease,
            "previous_diseases": "|".join(previous_disease_names),
        }

        append_patient(row)

        history_all = load_patient_history()
        history_all[str(new_id)] = {
            "auto_history": auto_history,
            "report_history": report_history,
        }
        save_patient_history(history_all)

        return redirect(url_for("main.patient_view", patient_id=new_id))

    return render_template("register.html")


@main_bp.route("/patient/<patient_id>")
def patient_view(patient_id):
    patients = load_patients()
    patient = next((p for p in patients if str(p.get("patient_id")) == str(patient_id)), None)
    if not patient:
        abort(404)

    present = patient.get("present_disease", "")
    prev_list = [
        d.strip()
        for d in (patient.get("previous_diseases") or "").split("|")
        if d.strip()
    ]

    all_rel = get_all_relations_for_disease(present)
    relation_data = {}

    for prev in prev_list:
        key = prev.title()
        rel = all_rel.get(key)
        if rel:
            relation_data[key] = rel
        else:
            relation_data[key] = {
                "probability": 0.0,
                "report": "No data available for this pair in base dataset.",
            }

    history_all = load_patient_history()
    history_info = history_all.get(str(patient_id), {})
    auto_history = history_info.get("auto_history", [])
    report_history = history_info.get("report_history", [])

    auto_context = []
    for h in auto_history:
        dname = h["disease"]
        prob = build_mock_causal_probability(
            present_disease=present,
            previous_disease=dname,
            patient_id=str(patient_id),
            extra_key=h.get("diagnosed_on", ""),
        )
        auto_context.append(
            {
                "disease": dname,
                "diagnosed_on": h.get("diagnosed_on"),
                "probability": prob,
                "source": "auto",
                "report": f"Previously recorded {dname} on {h.get('diagnosed_on')} may influence the current {present} (mock).",
            }
        )
        relation_data[dname.title()] = {
            "probability": prob,
            "report": f"Auto-history linkage: {dname} on {h.get('diagnosed_on')} → {present}.",
        }

    report_context = []
    for h in report_history:
        dname = h["disease"]
        prob = build_mock_causal_probability(
            present_disease=present,
            previous_disease=dname,
            patient_id=str(patient_id),
            extra_key=f"report-{h.get('diagnosed_on', '')}",
        )
        report_context.append(
            {
                "disease": dname,
                "diagnosed_on": h.get("diagnosed_on"),
                "probability": prob,
                "source": "upload",
                "report": f"Disease {dname} from uploaded report dated {h.get('diagnosed_on')} may still contribute to {present} (mock).",
            }
        )
        relation_data[dname.title()] = {
            "probability": prob,
            "report": f"Report-derived linkage: {dname} ({h.get('diagnosed_on')}) → {present}.",
        }

    state_map = load_state_diseases()
    state_raw = (patient.get("state") or "").strip()
    state_diseases = state_map.get(state_raw) or state_map.get(state_raw.title()) or []
    state_context = build_state_causal_context(
        present_disease=present,
        state=state_raw or "Unknown",
        state_diseases=state_diseases,
        patient_id=str(patient_id),
    )

    vitals = generate_mock_vitals(str(patient_id))
    vital_scores = vitals_to_scores(vitals)

    chart_values = (
        [c["probability"] for c in auto_context]
        + [c["probability"] for c in report_context]
        + [c["probability"] for c in state_context]
        + vital_scores
    )

    return render_template(
        "report.html",
        patient=patient,
        relation_data=relation_data,
        state_context=state_context,
        vitals=vitals,
        auto_history=auto_context,
        report_history=report_context,
        chart_values=chart_values,
    )
