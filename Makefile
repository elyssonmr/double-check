runserver:
	@python -m aiohttp.web -H localhost -P 8080 main:main

install-dev:
	@pip install -r requirements_dev.txt

install:
	@pip install -r requirements.txt

flake8:
	@flake8 --max-complexity 7 --statistics

fix-import-order:
	@isort . -q --fass

test:
	@pytest -x --cov=double_check --cov-config=.coveragerc --cov-report=term .
