# Development Guide

Please run the following before committing:

* `./check.sh`
* `uv run pytest -vv --capture=sys`
* `./prettify.sh`

## Dependencies

Dependencies are managed with [uv](https://docs.astral.sh/uv/). After changing them in `pyproject.toml`, run `uv lock` and commit `uv.lock`. The Docker image installs the locked versions with `uv sync --frozen`.

## Releases

Run `./release.py patch` (or `minor`, `major`). Use `-n` for a dry run.
