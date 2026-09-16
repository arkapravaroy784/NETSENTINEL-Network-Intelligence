.PHONY: test demo up
test:
	python -m pytest backend/tests agent/tests ml/tests
demo:
	python scripts/run_demo_scenario.py --scenario packet_loss
up:
	docker compose up --build
