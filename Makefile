MAP ?=
LINT := --warn-return-any \
	   	--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude .venv
install:
	@uv sync

run: install
	@uv run -m fly_in $(MAP)

debug: install
	@uv run -m pdb -m fly_in $(MAP)

clean:
	rm  -r ./.mypy_cache

lint: install
	uv run flake8 . --exclude .venv
	uv run mypy . $(LINT) 

lint-strict: install
	uv run flake8 . --exclude .venv
	uv run mypy . --strict --exclude .venv
