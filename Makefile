.PHONY: bootstrap clean lint
.DEFAULT_GOAL := lint

lint:
	@flake8 .

clean:
	@find . -type f -name '*.pyc' -delete

bootstrap:
	@python3.9 -m pip install -r requirements.txt
	@python3.9 -m pip install -r requirements-test.txt
	@python3.9 -m pip install -e .
	@find . -type d -name '*.egg-info' -prune -exec rm -rf {} \;

# Pipelines

p1:
	@python3.9 pipelines/p1_orca_by_stop.py

p2:
	@python3.9 pipelines/p2_aggregate_orca.py

p3:
	@python3.9 pipelines/p3_prep_apc.py

p4:
	@python3.9 pipelines/p4_aggregate_apc.py

p5:
	@python3.9 pipelines/p5_orca_rates.py

# Run all pipelines
all:
	@python3.9 pipelines/all.py
