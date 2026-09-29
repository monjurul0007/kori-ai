# Contributing

kori-ai follows the same conventions as kori. See
[kori's CONTRIBUTING.md](https://github.com/monjurul0007/kori/blob/main/CONTRIBUTING.md) for
branches, Conventional Commits, PR size, review labels and the Definition of Done.

Local checks before pushing:

```bash
uv sync
make lint
make test
pre-commit run --all-files
```
