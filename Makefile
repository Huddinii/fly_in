MAP ?=
install:
	@uv sync

run: install
	@uv run fly_in $(MAP)
