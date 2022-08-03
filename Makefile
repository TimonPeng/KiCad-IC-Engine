install:
	pip install -r requirements.txt

compile:
	pip-compile --output-file=requirements.txt requirements.in && make install

format:
	isort src
	black --line-length=120 src

lint:
	black --check --diff --line-length=120 src
	flake8 src
	mypy src
	pylint --rcfile=.pylintrc src
