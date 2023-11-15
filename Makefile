.PHONY: help test format lint clean

help:
	@echo "help - display this message"
	@echo "test - measure code coverage with pytest engine"
	@echo "format - format package with black"
	@echo "lint - static code analysis"
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