# backend/__init__.py
from flask import Flask, g, session, request
from config import settings

# Blueprints
from backend.routes.main_routes import main_bp
from backend.routes.api_routes import api_bp

# Translation helper
from backend.utils.i18n import translate


def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    # -----------------------------
    # Base config
    # -----------------------------
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    # -----------------------------
    # Register routes
    # -----------------------------
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # -----------------------------
    # Language handling
    # -----------------------------
    @app.before_request
    def set_language():
        """
        Ensures language is attached to global context (g.lang)
        so templates always receive the correct translation.
        """
        lang = session.get("lang", settings.DEFAULT_LANGUAGE)
        if lang not in settings.SUPPORTED_LANGUAGES:
            lang = settings.DEFAULT_LANGUAGE
        g.lang = lang

    # -----------------------------
    # Inject globals into templates
    # -----------------------------
    @app.context_processor
    def inject_globals():
        """
        Makes the `_t()` translation function and language data globally
        available inside all Jinja templates.
        """

        def t(key: str):
            lang = getattr(g, "lang", settings.DEFAULT_LANGUAGE)
            return translate(key, lang)

        return {
            "t": t,
            "current_language": getattr(g, "lang", settings.DEFAULT_LANGUAGE),
            "supported_languages": settings.SUPPORTED_LANGUAGES,
            "app_name": settings.APP_NAME,
            "version": settings.VERSION,
            "request": request,
        }

    return app
