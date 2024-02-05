.DEFAULT_GOAL := help

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

lint:
	ruff check .

lint-fix:
	ruff check . --fix

fmt-check:
	poetry run isort . --check-only
	poetry run black . --check
	poetry run autoflake -r . --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	poetry run ruff format . --check

fmt:
	poetry run isort .
	poetry run black .
	poetry run autoflake -r -i . --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	poetry run ruff format . 

typecheck:
	poetry run mypy .