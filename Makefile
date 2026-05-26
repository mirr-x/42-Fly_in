PYTHON = python3
PIP = pip3
MAP ?= maps/easy/01_linear_path.txt

.PHONY: install run debug clean lint lint-strict

install:
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy
	$(PIP) install pygame-ce

run:
	$(PYTHON) -m flyin.main $(MAP)

debug:
	$(PYTHON) -m pdb -m flyin.main $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	flake8 . --exclude=./.venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs --exclude ./.venv

lint-strict:
	flake8 . --exclude ./.venv
	mypy . --strict --exclude ./.venv
