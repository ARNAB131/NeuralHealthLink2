# backend/__init__.py
from flask import Flask, g, session
from config import settings
from backend.routes.main_routes import main_bp
from backend.routes.api_routes import api_bp
from backend.utils.i18n import translate


def create_app():
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.before_request
    def set_language():
        lang = session.get("lang", settings.DEFAULT_LANGUAGE)
        if lang not in settings.SUPPORTED_LANGUAGES:
            lang = settings.DEFAULT_LANGUAGE
        g.lang = lang

    @app.context_processor
    def inject_globals():
        from flask import request

        def t(key: str):
            return translate(key, getattr(g, "lang", settings.DEFAULT_LANGUAGE))

        return {
            "t": t,
            "current_language": getattr(g, "lang", settings.DEFAULT_LANGUAGE),
            "supported_languages": settings.SUPPORTED_LANGUAGES,
            "app_name": settings.APP_NAME,
            "request": request,
        }

    return app
