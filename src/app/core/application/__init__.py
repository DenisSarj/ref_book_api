from src.app.core.application.application import RefBookApplication
from src.configs import settings

ref_book_app = RefBookApplication(debug=settings.debug)

__all__ = ("ref_book_app",)
