.DEFAULT_GOAL := help

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

lint:
	uv run black . --check
	uv run autoflake -r . --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	uv run ruff format . --check
	uv run ruff check .
	uv run mypy --install-types
	uv run mypy .

fmt:
	uv run black .
	uv run autoflake -r -i . --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	uv run ruff format .
	uv run ruff check . --fix

test:
	uv run pytest tests -v --tb=short -s
