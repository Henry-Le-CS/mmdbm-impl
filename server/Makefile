.PHONY: run-api

run-api:
	python3 main.py

.PHONY: run-worker

run-worker:
	celery -A worker.app worker --loglevel=INFO --pool threads