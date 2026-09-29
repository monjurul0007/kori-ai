from fastapi import FastAPI
from fastapi.testclient import TestClient

from kori_ai.config import Env, Settings
from kori_ai.main import create_app


def test_unknown_route_is_problem_json(client: TestClient) -> None:
    r = client.get("/nope")
    assert r.status_code == 404
    assert r.headers["content-type"].startswith("application/problem+json")
    assert r.json()["request_id"] == r.headers["X-Request-ID"]


def test_inbound_request_id_is_echoed(client: TestClient) -> None:
    r = client.get("/healthz", headers={"X-Request-ID": "abc-123"})
    assert r.headers["X-Request-ID"] == "abc-123"


def test_unhandled_error_hides_internals() -> None:
    app: FastAPI = create_app(Settings(env=Env.TEST))

    @app.get("/boom")
    def boom() -> None:
        raise RuntimeError("secret internal detail")

    r = TestClient(app, raise_server_exceptions=False).get("/boom")
    assert r.status_code == 500
    assert r.headers["content-type"].startswith("application/problem+json")
    assert "secret" not in r.text
    assert r.json()["request_id"] == r.headers["X-Request-ID"]
