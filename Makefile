# Variables
PYTHON=python3
PIP=pip3
PYTEST=pytest
BLACK=black
ISORT=isort
FLAKE8=flake8

# Default target
.PHONY: all
all: help

# Run tests
.PHONY: test
test:
	$(PYTEST) -v tests/

# Run tests with coverage
.PHONY: coverage
coverage:
	$(PYTEST) --cov=src --cov-report=term-missing

# Format code with black
.PHONY: format
format:
	$(BLACK) src tests

# Sort imports with isort
.PHONY: sort
sort:
	$(ISORT) src tests

# Lint code with flake8
.PHONY: lint
lint:
	$(FLAKE8) src tests

# Clean pyc and __pycache__
.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +

# Show help
.PHONY: help
help:
	@echo "Available make targets:"
	@echo "  make test       - Run all tests"
	@echo "  make coverage   - Run tests with coverage report"
	@echo "  make format     - Format code with black"
	@echo "  make sort       - Sort imports with isort"
	@echo "  make lint       - Lint code with flake8"
	@echo "  make clean      - Remove pyc files and __pycache__ directories"
