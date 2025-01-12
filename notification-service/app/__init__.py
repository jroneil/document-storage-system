# notification-service/app/__init__.py

# Expose the main FastAPI app
from .main import app

# Expose services for easier imports
from .services.notification import send_email

# Optional: Define what should be exposed when the package is imported
__all__ = ["app", "send_email"]