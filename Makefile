.PHONY: help install dev test lint format clean run api docs

help:
	@echo "Auditoria-CS-IA Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install       Install dependencies"
	@echo "  make dev           Install dev dependencies"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code"
	@echo "  make clean         Remove build artifacts"
	@echo "  make run           Run audit CLI"
	@echo "  make api           Start REST API server"
	@echo "  make docs          Build documentation"

install:
	pip install -e .

dev:
	pip install -e ".[dev,api]"

test:
	pytest tests/

test-cov:
	pytest --cov=auditoria --cov-report=html tests/
	@echo "Coverage report: htmlcov/index.html"

lint:
	flake8 auditoria/ tests/
	mypy auditoria/

format:
	black auditoria/ tests/
	isort auditoria/ tests/

clean:
	rm -rf build dist *.egg-info .eggs
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage
	rm -rf data/audit-results/* data/reports/* data/logs/*

run:
	auditoria audit --target localhost

api:
	python scripts/run_api.py

docs:
	@echo "Documentation is in docs/ directory"
	@echo "Start with: docs/README.md"

.DEFAULT_GOAL := help
