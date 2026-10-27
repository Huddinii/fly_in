MAP ?=
install:
	@uv sync

run: install
	@uv run -m fly_in $(MAP)
