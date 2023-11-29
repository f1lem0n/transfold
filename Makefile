# Author: Filip Hajdyła
# Date of creation: 15/11/2023
# Description: Automation of common tasks for the project

SHELL := /bin/bash

.PHONY: help test format lint clean checksum verify install

help:
	@echo
	@echo "MAKE TARGETS ARE FOR DEVELOPMENT PURPOSES ONLY."
	@echo "PLEASE USE CONDA ENV FOR RUNNING ANY OF THE MAKE TARGETS."
	@echo
	@echo "Available targets:"
	@echo "help - display this help message"
	@echo "test - measure code coverage with pytest"
	@echo "format - format package with black and isort"
	@echo "lint - static code analysis with flake8 and mypy"
	@echo "clean - remove common artifacts from the directory tree"
	@echo "checksum - generate md5 checksum of the repository"
	@echo "verify - verify md5 checksum of the repository (if stdout is empty then checksums are equal)"
	@echo "build - build python package"

test:
	@coverage run -m pytest -x -v --log-level=DEBUG && \
		echo "" && \
		echo "COVERAGE REPORT:" && \
		echo "" && \
		coverage report -m;

format:
	@echo "Sorting imports..."
	@isort --profile black -l 79 transfold/ tests/ setup.py
	@echo "Formatting code..."
	@black -l 79 -t py312 --safe transfold/ tests/ setup.py

lint:
	@flake8 transfold/ tests/ setup.py
	@mypy transfold/ tests/ setup.py

clean:
	@rm -rf .coverage .pytest-monitor .pytest_cache .mypy_cache
	@rm -rf \
		transfold/__pycache__ \
		transfold/modules/__pycache__ \
		tests/__pycache__ \
		tests/data/CDS/ \
		tests/data/temp \
		transfold-test-venv/ \
		transfold.egg-info/ \
		dist/

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
		\! -path "*__pycache__*" \
		\! -path "./.checksum.md5" \
		\! -path "./transfold-test-venv/*" \
		\! -path "./transfold.egg-info/*" \
		\! -path "./dist/*" \
		-exec md5sum {} \; | sort -k 2 | md5sum > .checksum.md5
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
		\! -path "*__pycache__*" \
		\! -path "./.checksum.md5" \
		\! -path "./transfold-test-venv/*" \
		\! -path "./transfold.egg-info/*" \
		\! -path "./dist/*" \
		-exec md5sum {} \; | sort -k 2 | md5sum | diff - .checksum.md5
	@echo "Checksums are equal!"

install:
	@echo "BUILDING PACKAGE..."
	@python3 -m build
	@echo "INSTALLING PACKAGE IN VENV..."
	@python3 -m venv transfold-test-venv
	@source transfold-test-venv/bin/activate && \
		pip install dist/transfold-*.whl && \
		deactivate
