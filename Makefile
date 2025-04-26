run:
	uvicorn app:app --port 8080 --reload

run2:
	hypercorn app:app --bind [::]:8080

frezze:
	python -m pip freeze > requirements.txt

build:
	pip install -r requirements.txt