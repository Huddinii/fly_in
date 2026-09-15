MAP ?=
install:
	@uv sync

run: install
	@uv run main.py $(MAP)
