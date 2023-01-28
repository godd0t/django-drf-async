lint:
	 bash ./scripts/lint.sh

format:
	bash ./scripts/format.sh

test:
	bash ./scripts/test.sh

test-cov:
	bash ./scripts/test-cov.sh

all help:
	@echo "$$HELP"


COMMANDS := $(wildcard python\ manage.py*)
.PHONY: $(COMMANDS)
