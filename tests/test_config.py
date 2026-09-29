import pytest

from kori_ai.config import Env, Settings, get_settings


def test_defaults() -> None:
    s = Settings(_env_file=None)
    assert s.env is Env.DEVELOPMENT
    assert s.log_level == "INFO"


def test_reads_prefixed_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KORI_AI_ENV", "production")
    assert Settings(_env_file=None).env is Env.PRODUCTION


def test_get_settings_is_cached() -> None:
    assert get_settings() is get_settings()
