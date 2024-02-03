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
	ruff format .

fmt:
	ruff format . --fix

typecheck:
	ruff typecheck .