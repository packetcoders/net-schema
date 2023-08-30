.DEFAULT_GOAL := help

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

### Format (Check only) ###

fmt-chk-black:
	@echo "## black (check) ##"
	@-black . --check
	@echo

fmt-chk-autoflake:
	@echo "## autoflake (check) ##"
	@-autoflake -r . --exclude venv --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	@echo

fmt-chk-isort:
	@echo "## isort (check) ##"
	@-isort . -c
	@echo

fmt-chk: ## Format (check)
fmt-chk:   fmt-chk-black fmt-chk-isort fmt-chk-autoflake

### Format ###

fmt-black:
	@echo "## black ##"
	@-black .
	@echo

fmt-autoflake:
	@echo "## autoflake ##"
	@-autoflake -vri . --exclude venv --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	@echo

fmt-isort:
	@echo "## isort ##"
	@-isort .
	@echo

fmt: ## Format
fmt:  fmt-black fmt-isort fmt-autoflake

### Linting ###

lint-bandit:
	@echo "## bandit ##"
	@-bandit -r . -c "pyproject.toml"
	@echo

lint-flake8:
	@echo "## flake8 ##"
	@-flake8 . 
	@echo

lint-pydoc:
	@echo "## pydocstyle ##"
	@-pydocstyle .
	@echo

lint-yaml:
	@echo "## yamllint ##"
	@-yamllint .
	@echo ""

lint-mypy:
	@echo "## mypy ##"
	@-mypy . 
	@echo ""

lint: ## Lint
lint:  lint-bandit lint-flake8 lint-pydoc lint-yaml lint-mypy

all: ## Test, migrate and dev server up
all:  web-test migrate server
