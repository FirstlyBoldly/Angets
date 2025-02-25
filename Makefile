.PHONY: init upgrade test flake8 mypy publish

init:
	python -m pip install -r requirements_dev.txt

upgrade:
	python -m pip install --upgrade angets

test:
	python -m pytest $(flags) tests/

flake8:
	python -m flake8 src

mypy:
	python -m mypy src

publish:
	python -m pip install --upgrade twine
	python -m twine upload dist/*
	rm -fr dist src/angets.egg-info
