MAP ?=
install:
	@uv sync

run: install
	@uv run -m fly_in $(MAP)

debug: install
	@uv run -m pdb -m fly_in $(MAP)

clean:
	rm  -rf .mypy_cache
	rm -rf fly_in/__pycache__

lint: install
	@uv run flake8 . --exclude .venv
	@uv run mypy . --warn-return-any \
	   	--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude .venv
 

lint-strict: install
	@uv run flake8 . --exclude .venv
	@uv run mypy . --strict --exclude .venv
