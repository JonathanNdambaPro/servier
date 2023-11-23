.PHONY: poetry_install
poetry_install:
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: env
env:
	poetry shell

.PHONY: install
install:
	poetry install

.PHONY: build
build:
	poetry build -f wheel

.PHONY: pre_commit
pre_commit:
	pre-commit install

.PHONY: test
test:
	pytest --cov=app/ --cov-report term-missing

.PHONY: requirements
requirements:
	poetry export --without-hashes --without=dev,test --format=requirements.txt > requirements.txt

.PHONY: requirements-test
requirements-test:
	poetry export --without-hashes --only=test --format=requirements.txt > requirements-test.txt

.PHONY: requirements-dev
requirements-dev:
	poetry export --without-hashes --only=dev --format=requirements.txt > requirements-dev.txt

.PHONY: docs
docs:
	pdoc app -o docs -d numpy