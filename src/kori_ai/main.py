from fastapi import FastAPI

from kori_ai.common.errors import register_error_handlers
from kori_ai.config import Settings, get_settings
from kori_ai.logging import configure_logging
from kori_ai.middleware import register_middleware
from kori_ai.routes import register_routes


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the app. Each concern is registered by its own function."""
    settings = settings or get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(title="Kori AI", version="0.1.0")
    app.state.settings = settings
    register_middleware(app)
    register_error_handlers(app)
    register_routes(app)
    return app


def app_factory() -> FastAPI:
    """Entry point for `uvicorn kori_ai.main:app_factory --factory`."""
    return create_app()
