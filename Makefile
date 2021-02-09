.PHONY: bootstrap clean lint
.DEFAULT_GOAL := lint

lint:
	@flake8 .

clean:
	@find . -type f -name '*.pyc' -delete

bootstrap:
	@python3.9 -m pip install -r requirements.txt
	@python3.9 -m pip install -r requirements-test.txt

# Pipelines
p1:
	@python3.9 pipelines/p1_xy_to_stop.py
