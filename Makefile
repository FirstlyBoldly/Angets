.PHONY: init upgrade test mypy flake8 black publish distclean

init:
	python -m pip install -r requirements_dev.txt

upgrade:
	python -m pip install --upgrade angets

test:
	python -m pytest -v --no-header --cov=angets tests/

mypy:
	python -m mypy src

flake8:
	python -m flake8 src

black:
	python -m black src

publish:
	python -m pip install --upgrade twine
	python -m twine upload dist/*
	rm -fr dist src/angets.egg-info

distclean:
	rm -fr dist src/angets.egg-info
