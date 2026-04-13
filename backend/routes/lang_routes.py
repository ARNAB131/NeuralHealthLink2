# backend/routes/lang_routes.py
from flask import Blueprint, request, session, redirect
from config import settings

lang_bp = Blueprint("lang", __name__)

@lang_bp.route("/set-language", methods=["POST"])
def set_language_route():
    lang = request.form.get("lang", settings.DEFAULT_LANGUAGE)

    if lang not in settings.SUPPORTED_LANGUAGES:
        lang = settings.DEFAULT_LANGUAGE

    session["lang"] = lang
    return redirect(request.referrer or "/")
