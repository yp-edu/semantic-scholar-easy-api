#Dev
.PHONY: appstart
appstart:
	poetry run uvicorn api.main:app --port 8000 --reload

#CI
.PHONY: install
install:
	pip install --upgrade pip
	pip install uv
	uv sync --dev

.PHONY: checks
checks:
	uv run pre-commit run --all-files

.PHONY: tests
tests:
	uv run pytest api_tests --cov=api --cov-report=term-missing --cov-fail-under=1 -s -vv -rA
