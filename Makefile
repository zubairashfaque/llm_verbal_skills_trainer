.PHONY: install install-dev lint format type-check test test-cov clean run setup help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	poetry install

install-dev: ## Install all dependencies including dev tools
	poetry install --with dev
	poetry run pre-commit install

setup: install-dev ## Complete development setup
	cp -n .env.example .env || true
	@echo "Setup complete! Edit .env file with your configuration."

lint: ## Run linting checks
	poetry run ruff check .

lint-fix: ## Run linting and auto-fix issues
	poetry run ruff check --fix .

format: ## Format code with ruff
	poetry run ruff format .

type-check: ## Run type checking with mypy
	poetry run mypy src/

test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage report
	poetry run pytest --cov=src --cov-report=term-missing --cov-report=html

test-watch: ## Run tests in watch mode
	poetry run pytest-watch

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
	@echo "Cleaned up generated files"

run: ## Run the application
	poetry run python main.py

check: lint type-check test ## Run all checks (lint, type-check, test)

pre-commit: ## Run pre-commit hooks on all files
	poetry run pre-commit run --all-files

update: ## Update dependencies
	poetry update

security: ## Run security audit
	poetry run pip-audit || pip install pip-audit && poetry run pip-audit
