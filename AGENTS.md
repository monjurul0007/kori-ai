# AGENTS.md: working agreement for AI coding agents

Read this file first in every session. It is the one set of rules for every AI coding agent
(Claude Code, Codex, Cursor, Copilot, Gemini CLI and others). Tool-specific files such as
[`CLAUDE.md`](CLAUDE.md) only point here.

The workflow, architecture rules and "never" list are shared with the `kori` repo. Read
[kori's AGENTS.md](https://github.com/monjurul0007/kori/blob/main/AGENTS.md) and
[CONTRIBUTING.md](https://github.com/monjurul0007/kori/blob/main/CONTRIBUTING.md) first.
Everything there applies here, including one card, one session, one PR. This file adds only what
is specific to `kori-ai`.

## kori-ai specifics

- **Stubs only for now.** No LLM calls until M4. Don't add any without a card.
- **Proposals, never writes.** This service never writes financial data and never calls kori's
  database. It returns proposals that the user confirms in kori.
- **Money:** amounts are decimal strings in taka with at most 2 decimals (ADR-0004). No floats.
- **Dates:** `occurred_on` is a local date in the request's `timezone`, resolved from `today`.
- **Errors:** RFC 9457 `application/problem+json` with `request_id`, same shape as kori.
- **Docs:** see [docs/architecture.md](docs/architecture.md) and [docs/adr](docs/adr/README.md).

## Layout

- `src/kori_ai/main.py`: app factory. `middleware.py` and `routes.py` are the single places where
  middleware and routers are registered.
- One package per feature (`health/`, `parse/`), each with its own `router.py`.
- `contracts/` (pydantic models), `ports/` (Protocols), `adapters/` (implementations).
- Tests swap the parser with `app.dependency_overrides[get_parser]`.

## Commands

| Task | Command |
|---|---|
| Install deps | `uv sync` |
| Run (dev) | `make dev` |
| Tests (coverage ≥ 85%) | `make test` |
| Lint, format check, types | `make lint` |
| Auto-fix and format | `make fmt` |
| All repo hooks | `pre-commit run --all-files` |
