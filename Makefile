clean:
	@rm -rf build/ dist/ *.egg-info
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +

install:
	pip install -r requirements.txt
	pip install .

test:
	py.test --flake8 --cov=snactor

test-all:
	tox

.PHONY: clean install test test-all
