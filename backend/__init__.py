from flask import Flask
from config import settings
from backend.routes.main_routes import main_bp
from backend.routes.api_routes import api_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    # Load core config
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['DEBUG'] = settings.DEBUG

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Optional root info route
    @app.route("/info")
    def info():
        return {
            "app": settings.APP_NAME,
            "version": settings.VERSION,
            "author": settings.AUTHOR,
            "country": settings.DEFAULT_COUNTRY
        }

    return app
