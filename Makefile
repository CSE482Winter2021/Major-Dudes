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
	@python3.9 pipelines/p1_xy_to_stop.py

p2:
	@python3.9 pipelines/p2_prep_apc.py
