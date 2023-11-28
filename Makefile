# Author: Filip Hajdyła
# Date of creation: 15/11/2023
# Description: Automation of common tasks for the project

.PHONY: help test format lint clean checksum verify

help:
	@echo "help - display this help message"
	@echo "test - measure code coverage with pytest"
	@echo "format - format package with black and isort"
	@echo "lint - static code analysis with flake8 and mypy"
	@echo "clean - remove common artifacts from the directory tree"
	@echo "checksum - generate md5 checksum of the repository"
	@echo "verify - verify md5 checksum of the repository (if stdout is empty then checksums are equal)"

test:
	@coverage run -m pytest -x -v --log-level=DEBUG && \
		echo "" && \
		echo "COVERAGE REPORT:" && \
		echo "" && \
		coverage report -m;

format:
	@echo "Sorting imports..."
	@isort --profile black -l 79 modules/ tests/ transfold.py
	@echo "Formatting code..."
	@black -l 79 -t py312 --safe modules/ tests/ transfold.py

lint:
	@flake8 modules/ tests/ transfold.py
	@mypy modules/ tests/ transfold.py

clean:
	@rm -rf .coverage .pytest-monitor .pytest_cache .mypy_cache
	@rm -rf \
		__pycache__ \
		modules/__pycache__ \
		tests/__pycache__ \
		tests/data/CDS/ \
		tests/data/temp

checksum:
	@echo "Generating repository checksum..."
	@find . -type f \
		\! -path "./.vscode/*" \
		\! -path "./.git/*" \
		\! -path "./data/CDS/*" \
		\! -path "./data/temp/*" \
		\! -path "./tests/data/CDS/*" \
		\! -path "./tests/data/temp/*" \
		\! -path "./.pytest_cache/*" \
		\! -path "./.mypy_cache/*" \
		\! -path "./.pytest-monitor/*" \
		\! -path "./.coverage" \
		\! -path "./transfold.md5" \
		\! -path "*__pycache__*" \
		-exec md5sum {} \; | sort -k 2 | md5sum > transfold.md5
	@echo "Checksum generated!"

verify:
	@echo "Verifying repository checksum..."
	@find . -type f \
		\! -path "./.vscode/*" \
		\! -path "./.git/*" \
		\! -path "./data/CDS/*" \
		\! -path "./data/temp/*" \
		\! -path "./tests/data/CDS/*" \
		\! -path "./tests/data/temp/*" \
		\! -path "./.pytest_cache/*" \
		\! -path "./.mypy_cache/*" \
		\! -path "./.pytest-monitor/*" \
		\! -path "./.coverage" \
		\! -path "./transfold.md5" \
		\! -path "*__pycache__*" \
		-exec md5sum {} \; | sort -k 2 | md5sum | diff - transfold.md5
	@echo "Checksums are equal!"