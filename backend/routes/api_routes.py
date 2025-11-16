from flask import Blueprint, jsonify
from backend.services.data_loader import load_patients, load_relations, load_diseases
from config import settings

# Create blueprint
api_bp = Blueprint("api", __name__)

# Preload mock data
patients = load_patients()
relations = load_relations()
diseases = load_diseases()


@api_bp.route("/patients", methods=["GET"])
def get_patients():
    """Return list of all patients."""
    return jsonify({"patients": patients})


@api_bp.route("/patients/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    """Return single patient details."""
    for p in patients:
        if p["patient_id"] == patient_id:
            return jsonify({"patient": p})
    return jsonify({"error": "Patient not found"}), 404


@api_bp.route("/diseases", methods=["GET"])
def get_diseases():
    """Return all predefined diseases and their symptoms."""
    return jsonify({"diseases": diseases})


@api_bp.route("/relations/<present>/<previous>", methods=["GET"])
def get_relation(present, previous):
    """Return relation probability and report between diseases."""
    rel = relations.get(present, {}).get(previous)
    if not rel:
        return jsonify({
            "present_disease": present,
            "previous_disease": previous,
            "probability": None,
            "report": "No predefined relation found."
        }), 404

    return jsonify({
        "present_disease": present,
        "previous_disease": previous,
        "probability": rel.get("probability"),
        "report": rel.get("report")
    })


@api_bp.route("/meta", methods=["GET"])
def get_meta():
    """App metadata."""
    return jsonify({
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "author": settings.AUTHOR,
        "country": settings.DEFAULT_COUNTRY,
        "data_source": "static mock files"
    })
