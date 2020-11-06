

pylint:
	pylint --rcfile pylintrc fbexp

docker:
	pipenv lock -r > requirements.txt
	docker build -t fbexp:latest .
