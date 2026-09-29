.PHONY: dev test lint fmt

dev:
	uv run uvicorn kori_ai.main:app_factory --factory --reload --port 8001

test:
	uv run pytest --cov-fail-under=85

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy

fmt:
	uv run ruff check --fix .
	uv run ruff format .
