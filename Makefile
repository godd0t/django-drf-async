lint:
	 bash ./scripts/lint.sh

format:
	bash ./scripts/format.sh

test:
	bash ./scripts/test.sh

test-cov:
	bash ./scripts/test-cov.sh

run-docs:
	bash ./scripts/run-docs.sh

deploy-docs:
	bash ./scripts/build-docs.sh

all help:
	@echo "$$HELP"


COMMANDS := $(wildcard python\ manage.py*)
.PHONY: $(COMMANDS)
