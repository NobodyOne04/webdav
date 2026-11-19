# webdav (filemanager): run `make help`.
.DEFAULT_GOAL := help
.PHONY: help install run test lint fmt check

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies (uv)
	uv sync

run: ## Run the dev server on http://127.0.0.1:8000
	DJANGO_DEBUG=1 uv run python manage.py runserver 127.0.0.1:8000

test: ## Run the tests
	uv run pytest -q

lint: ## ruff lint + format check
	uv run ruff check .
	uv run ruff format --check .

fmt: ## Format and fix what ruff can
	uv run ruff format .
	uv run ruff check --fix .

check: lint test ## Everything that must pass before a PR
