# Development

## Setup

```bash
poetry install
```

## Tests

```bash
poetry run pytest
```

## Release

1. Update `CHANGELOG.md`
2. Update version in `pyproject.toml`
3. Run `poetry build && poetry publish`
