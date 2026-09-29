# kori-ai

The AI service for [Kori](https://github.com/monjurul0007/kori), a personal expense and budget app.

**Status: stubs only.** There is no LLM code yet. The service defines the `ExpenseParser`
interface and a `POST /v1/parse` endpoint that returns `501 Not implemented`. The real parser
arrives in M4.

## Role

Kori owns the financial data. This service turns free text ("lunch 250 bkash") into a *proposed*
transaction and returns it. It never writes to Kori's data: the user confirms every proposal in
Kori. See [ADR-0003](https://github.com/monjurul0007/kori/blob/main/docs/adr/0003-two-repo-split.md)
and [ADR-0004](https://github.com/monjurul0007/kori/blob/main/docs/adr/0004-money-and-dates.md).

## Endpoints

| Method | Path | Notes |
|---|---|---|
| GET | `/healthz` | `{"status": "ok"}` |
| POST | `/v1/parse` | `ParseRequest` in, `ParseResult` out. 501 until M4 |

The contract is in `src/kori_ai/contracts/parse.py`. Every field's docstring says what a parser
should fill in.

## Run it

```bash
uv sync
make dev            # http://localhost:8001, docs at /docs
make test           # coverage must stay at 85% or above
make lint           # ruff, format check, mypy
```

Or with Docker:

```bash
docker build -t kori-ai .
docker run --rm -p 8001:8001 kori-ai
```

See [docs/architecture.md](docs/architecture.md) for the code layout.

Settings come from `KORI_AI_*` environment variables (see `.env.example`).

## Contributing

See [AGENTS.md](AGENTS.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
