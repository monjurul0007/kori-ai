"""Route registration. To add a feature, import its router and append it to `ROUTERS`."""

from fastapi import APIRouter, FastAPI

from kori_ai.health.router import router as health_router
from kori_ai.parse.router import router as parse_router

API_PREFIX = "/v1"

# The health check stays unversioned so probes never depend on the API version.
UNVERSIONED_ROUTERS: list[APIRouter] = [health_router]
ROUTERS: list[APIRouter] = [parse_router]


def register_routes(app: FastAPI) -> None:
    for router in UNVERSIONED_ROUTERS:
        app.include_router(router)
    for router in ROUTERS:
        app.include_router(router, prefix=API_PREFIX)
