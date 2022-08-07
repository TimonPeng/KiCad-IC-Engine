init:
	poetry shell
	make install

install:
	poetry install

format:
	poetry run isort src
	poetry run black --line-length=120 src

lint:
	poetry run black --check --diff --line-length=120 src
	poetry run flake8 src
	poetry run pylint src
	poetry run mypy src
