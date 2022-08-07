init:
	poetry shell
	make install

install:
	poetry install

format:
	isort src
	black --line-length=120 src

lint:
	black --check --diff --line-length=120 src
	flake8 src
	pylint src
	mypy src
