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
3. Tag: `git tag -a v1.0.2 -m "Release 1.0.2" && git push --tags`
3. Run `poetry build && poetry publish`

## PyPI authentication

```
poetry config pypi-token.pypi your-api-token
```