# 0001. Record architecture decisions

- Status: Accepted
- Date: 2026-09-29
- Refs: M1-03

## Context

`kori-ai` is built across short, independent sessions, some of them AI-assisted. Nobody carries
the full history of a decision in their head. The `kori` repo already solves this with ADRs
([kori ADR-0001](https://github.com/monjurul0007/kori/blob/main/docs/adr/0001-record-architecture-decisions.md)).

## Decision

We follow the same practice here: significant, hard-to-reverse decisions that only concern
`kori-ai` are recorded in `docs/adr/` in the Nygard format, with sequential numbers that are never
reused. Decisions that span both repos stay in kori's `docs/adr/`. A new ADR supersedes an old one
rather than editing it.

## Consequences

- New sessions can learn why things are as they are by reading `docs/adr/`.
- `AGENTS.md` points here, so every AI agent picks up the same constraints.
