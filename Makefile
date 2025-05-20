.PHONY: test

.venv:  # creates .venv folder if does not exist
	python3.10 -m venv .venv

pip: .venv # installs latest pip
	.venv/bin/pip install --quiet --upgrade pip wheel setuptools poetry

install: pip
	.venv/bin/poetry install

lint:
	pre-commit run --all-files

build:
	docker build -t shared-resources:latest .

shell: build
	docker run --rm -it shared-resources:latest bash

test: build
	docker run --rm shared-resources:latest bash -c "poetry run pytest -slv --cov"
