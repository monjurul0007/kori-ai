# Architecture Decision Records

We record significant, hard-to-reverse decisions as short ADRs in the
[Michael Nygard format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions):
Status, Context, Decision and Consequences.

Decisions that span both repos live in kori's
[docs/adr](https://github.com/monjurul0007/kori/tree/main/docs/adr), for example
[ADR-0003 (two-repo split)](https://github.com/monjurul0007/kori/blob/main/docs/adr/0003-two-repo-split.md)
and [ADR-0004 (money and dates)](https://github.com/monjurul0007/kori/blob/main/docs/adr/0004-money-and-dates.md).
ADRs here cover decisions that only concern `kori-ai`.

| # | Title | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |

## Writing a new ADR

1. Copy the template below to `NNNN-short-title.md`, using the next number.
2. Keep it to about one page. Link the Trello card or spike that prompted it.
3. Open a PR with the `docs` scope, e.g. `docs: add ADR-0002 parser interface`.
4. To change a decision, add a new ADR that supersedes the old one, and mark the old one
   `Superseded by NNNN`. Don't rewrite accepted ADRs.

```markdown
# NNNN. Title

- Status: Proposed | Accepted | Superseded by NNNN
- Date: YYYY-MM-DD
- Refs: <card or spike>

## Context
## Decision
## Consequences
```
