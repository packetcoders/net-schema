.DEFAULT_GOAL := help

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

lint:
	poetry run black . --check
	poetry run autoflake -r . --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	poetry run ruff format . --check
	poetry run ruff check .
	poetry run mypy .

fmt:
	poetry run black .
	poetry run autoflake -r -i . --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	poetry run ruff format .
	poetry run ruff check . --fix

test:
	poetry run pytest tests -v --tb=short -s
