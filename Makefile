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
		coverage report -m;\

format:
	@echo "Sorting imports..."
	@isort --profile black -l 79 modules/ tests/
	@echo "Formatting code..."
	@black -l 79 -t py312 --safe modules/ tests/

lint:
	@flake8 modules/ tests/
	@mypy modules/ tests/

clean:
	@rm -rf .coverage .pytest-monitor .pytest_cache .mypy_cache
	@rm -rf \
		modules/__pycache__ \
		tests/__pycache__
	@rm -rf \
		tests/data/CDS/ \
		tests/data/temp

checksum:
	@echo "Generating repository checksum..."
	@find . -type f \
		\! -path "./.git/*" \
		\! -path "./data/CDS/*" \
		\! -path "./data/temp/*" \
		\! -path "./tests/data/CDS/*" \
		\! -path "./tests/data/temp/*" \
		\! -path "./.pytest_cache/*" \
		\! -path "./.mypy_cache/*" \
		\! -path "./.pytest-monitor/*" \
		\! -path "./.coverage" \
		\! -path "./checksum.md5" \
		\! -path "*__pycache__*" \
		-exec md5sum {} \; | sort -k 2 | md5sum > checksum.md5
	@echo "Checksum generated!"

verify:
	@echo "Verifying repository checksum..."
	@find . -type f \
		\! -path "./.git/*" \
		\! -path "./data/CDS/*" \
		\! -path "./data/temp/*" \
		\! -path "./tests/data/CDS/*" \
		\! -path "./tests/data/temp/*" \
		\! -path "./.pytest_cache/*" \
		\! -path "./.mypy_cache/*" \
		\! -path "./.pytest-monitor/*" \
		\! -path "./.coverage" \
		\! -path "./checksum.md5" \
		\! -path "*__pycache__*" \
		-exec md5sum {} \; | sort -k 2 | md5sum | diff - checksum.md5
	@echo "Checksums are equal!"