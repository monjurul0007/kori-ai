from fastapi import FastAPI

from kori_ai.common.errors import register_error_handlers
from kori_ai.common.request_id import RequestIdMiddleware
from kori_ai.config import Settings, get_settings
from kori_ai.logging import configure_logging
from kori_ai.routes import health, parse


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the app. Each concern is registered by its own call."""
    settings = settings or get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(title="Kori AI", version="0.1.0")
    app.state.settings = settings
    app.add_middleware(RequestIdMiddleware)
    register_error_handlers(app)
    app.include_router(health.router)
    app.include_router(parse.router, prefix="/v1")
    return app


def app_factory() -> FastAPI:
    """Entry point for `uvicorn kori_ai.main:app_factory --factory`."""
    return create_app()
