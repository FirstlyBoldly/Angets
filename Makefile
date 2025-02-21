.PHONY: deps upgrade test

deps:
	python -m pip install -r requirements_dev.txt

upgrade:
	python -m pip install --upgrade angets

test:
	python -m pytest tests/
