# CLAUDE.md

The workflow, architecture rules and "never" list live in kori's
[AGENTS.md](https://github.com/monjurul0007/kori/blob/main/AGENTS.md) and
[CONTRIBUTING.md](https://github.com/monjurul0007/kori/blob/main/CONTRIBUTING.md). Read them first.
Everything there applies here, including one card, one session, one PR.

## kori-ai specifics

- **Stubs only for now.** No LLM calls until M4. Don't add any without a card.
- **Proposals, never writes.** This service never writes financial data and never calls kori's
  database. It returns proposals that the user confirms in kori.
- **Money:** amounts are decimal strings in taka with at most 2 decimals (ADR-0004). No floats.
- **Dates:** `occurred_on` is a local date in the request's `timezone`, resolved from `today`.
- **Errors:** RFC 9457 `application/problem+json` with `request_id`, same shape as kori.
- **Layout:** `contracts/` (pydantic models), `ports/` (Protocols), `adapters/` (implementations),
  `routes/` (HTTP). Tests swap the parser with `app.dependency_overrides[get_parser]`.
- **Commands:** `uv sync`, `make dev`, `make test` (coverage ≥ 85%), `make lint`, `make fmt`,
  `pre-commit run --all-files`.
