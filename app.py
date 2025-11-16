# /app.py
import os
from backend import create_app
from config import settings

# Initialize Flask app
app = create_app()

if __name__ == "__main__":
    # Render (and other PaaS) provide port via environment variable
    port = int(os.environ.get("PORT", settings.PORT or 8080))

    print(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"Author: {settings.AUTHOR} | Country: {settings.DEFAULT_COUNTRY}")
    print(f"Server running on 0.0.0.0:{port}")

    # Run Flask on public interface for Render/Cloud
    app.run(
        host="0.0.0.0",
        port=port,
        debug=settings.DEBUG
    )
