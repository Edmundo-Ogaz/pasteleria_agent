run:
	uvicorn app:app --port 8081 --reload

run2:
	hypercorn app:app --bind [::]:8081

frezze:
	python -m pip freeze > requirements.txt

build:
	pip install -r requirements.txt