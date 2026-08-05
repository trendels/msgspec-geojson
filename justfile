# Format, typecheck and test code
all: format typecheck test doctest

# Run all checks (for CI)
check: check-format typecheck

# Lint and format all code
format:
    uv run ruff check --fix
    uv run ruff format

# Check that code is linted and formatted
check-format:
    uv run ruff check
    uv run ruff format --check --diff

# Run typechecker
typecheck:
    uv run pyright

# Run tests and measure code coverage
test:
    uv run coverage run -m pytest
    uv run coverage report
    uv run coverage html

# Run doctests
doctest:
    uv run python -m doctest -o ELLIPSIS README.md

# Run tests when code changes (requires "watchexec")
watch:
    watchexec -w src -w tests -e py -c -- 'uv run pytest --exitfirst --failed-first'
