
install:
	pip install -r requirements.txt

test:
	pytest

run:
	python src/core/app.py
