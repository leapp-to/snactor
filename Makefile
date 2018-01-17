clean:
	@rm -rf build/ dist/ *.egg-info
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +

build:
	true

install-deps:
	# WORKAROUND FOR: https://github.com/ansible/ansible/issues/31741
	pip install --upgrade setuptools
	pip install -r requirements-tests.txt

install:
	pip install .


test:
	py.test --flake8 --cov=snactor

test-all:
	tox

.PHONY: clean build install-deps install test test-all
