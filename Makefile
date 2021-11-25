clean:
	@find . -name "__pycache__" | xargs rm -rf
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name ".pytest_cache" | xargs rm -rf
	@find . -name ".coverage" | xargs rm -rf

runserver:
	@python -m aiohttp.web -H localhost -P 8080 main:main

runbot:
	@python bot_handler.py

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
