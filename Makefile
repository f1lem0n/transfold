# Author: Filip Hajdyła
# Date of creation: 15/11/2023
# Description: Automation of common tasks for the project

.PHONY: help test format lint clean

help:
	@echo "help - display this help message"
	@echo "test - measure code coverage with pytest"
	@echo "format - format package with black"
	@echo "lint - static code analysis with flake8 and mypy"
	@echo "clean - remove common artifacts from the directory tree"

test:
	@# Run unit tests and measure code coverage
	@coverage run -m pytest -x -v --log-level=DEBUG && \
		echo "" && \
		echo "COVERAGE REPORT:" && \
		echo "" && \
		coverage report -m;\

format:
	@# Format the code with black & isort
	@black -l 79 scripts/ tests/
	@isort scripts/ tests/

lint:
	@# Lint the code and docstrings
	@flake8 scripts/ tests/
	@# Perform type check
	@mypy scripts/ tests/

clean:
	@# Remove common artifacts from the directory tree
	@rm -rf .coverage .pytest-monitor .pytest_cache .mypy_cache
	@rm -rf \
		scripts/__pycache__ \
		tests/__pycache__