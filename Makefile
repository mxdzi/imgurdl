.PHONY: help
help:
	@echo "lint     - run black, mypy"
	@echo "black    - run black"
	@echo "mypy     - run mypy"

.PHONY: black
black:
	black imgurdl.py

.PHONY: mypy
mypy:
	mypy imgurdl.py

.PHONY: lint
lint: black mypy
