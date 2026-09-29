from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from kori_ai.config import Env, Settings
from kori_ai.main import create_app


@pytest.fixture
def app() -> FastAPI:
    return create_app(Settings(env=Env.TEST))


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
