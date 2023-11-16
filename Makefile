# Author: Filip Hajdyła
# Date of creation: 15/11/2023
# Description: Automation of common tasks for the project

.PHONY: help test format lint clean

help:
	@echo "help - display this help message"
	@echo "test - measure code coverage with pytest"
	@echo "format - format package with black and isort"
	@echo "lint - static code analysis with flake8 and mypy"
	@echo "clean - remove common artifacts from the directory tree"

test:
	@coverage run -m pytest -x -v --log-level=DEBUG && \
		echo "" && \
		echo "COVERAGE REPORT:" && \
		echo "" && \
		coverage report -m;\

format:
	@echo "Sorting imports..."
	@isort --profile black scripts/ tests/
	@echo "Formatting code..."
	@black -l 79 -t py312 --safe scripts/ tests/

lint:
	@flake8 scripts/ tests/
	@mypy scripts/ tests/

clean:
	@rm -rf .coverage .pytest-monitor .pytest_cache .mypy_cache
	@rm -rf \
		scripts/__pycache__ \
		tests/__pycache__