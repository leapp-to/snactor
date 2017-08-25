install:
	pip install .

test:
	PYTHONPATH=$(PYTHONPATH):$(PWD) python -m unittest discover -vs tests/

.PHONY: init test
