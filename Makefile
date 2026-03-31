.PHONY: venv sync compile lint test security precommit

venv:
	python -m venv .venv

compile:
	. .venv/bin/activate && python -m pip install -U pip setuptools wheel pip-tools
	. .venv/bin/activate && pip-compile requirements.in -o requirements.txt
	. .venv/bin/activate && pip-compile requirements-dev.in -o requirements-dev.txt

sync:
	. .venv/bin/activate && python -m pip install -U pip setuptools wheel
	. .venv/bin/activate && pip-sync requirements.txt requirements-dev.txt

lint:
	. .venv/bin/activate && ruff check .
	. .venv/bin/activate && ruff format --check .

test:
	. .venv/bin/activate && pytest

security:
	. .venv/bin/activate && bandit -q -r .github/scripts
	. .venv/bin/activate && XDG_CACHE_HOME=/tmp/.cache pip-audit --no-deps --disable-pip --ignore-vuln CVE-2026-4539 -r requirements.txt -r requirements-dev.txt

precommit:
	. .venv/bin/activate && pre-commit run --all-files
