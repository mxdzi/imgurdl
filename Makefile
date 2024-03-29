.PHONY: help
help:
	@echo "lint     - run black, mypy"
	@echo "black    - run black"
	@echo "mypy     - run mypy"
	@echo "test     - run pytest with code coverage"

.PHONY: black
black:
	black *.py

.PHONY: mypy
mypy:
	mypy imgurdl.py

.PHONY: lint
lint: black mypy

.PHONY: test
test:
	pytest -v --cov imgurdl --cov-report html --cov-report term
