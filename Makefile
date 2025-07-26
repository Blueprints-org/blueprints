# Makefile

#─────────────────────────────────────────────────────────────────────────────
# Variables
#─────────────────────────────────────────────────────────────────────────────
UV      		:= uv
PYTHON_VERSION  := 3.12
VENV    		:= $(UV) venv --python $(PYTHON_VERSION)
ALL    			:= --all-groups
TESTS 			:= --group test
NO_TESTS 		:= --no-group test
DEV 		    := --dev
NO_DEV		  	:= --no-dev
DOCS 			:= --group docs
NO_DOCS  		:= --no-group docs
SYNC			:= $(UV) sync --locked
RUN     		:= $(UV) run
BUILD 			:= $(UV) build
PYTEST  		:= $(RUN) $(NO_DEV) pytest
COVERAGE		:= $(PYTEST) --cov=./blueprints
MYPY    		:= $(RUN) mypy
RUFF    		:= $(RUN) ruff

#─────────────────────────────────────────────────────────────────────────────
# Default target
#─────────────────────────────────────────────────────────────────────────────
.PHONY: help
help:                           ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

#─────────────────────────────────────────────────────────────────────────────
# Environment setup
#─────────────────────────────────────────────────────────────────────────────
.PHONY: install
install:                       ## Create venv and sync all dependencies

	$(VENV)
	$(SYNC) $(ALL)

.PHONY: ci-install
ci-install:                    ## Sync dependencies for CI/CD tests

	$(SYNC) $(NO_DEV)

#─────────────────────────────────────────────────────────────────────────────
# Code quality targets
#─────────────────────────────────────────────────────────────────────────────
.PHONY: lint
lint:                          ## Lint with Ruff
	$(RUFF) check .

.PHONY: format
format:                        ## Check the formatting with Ruff
	$(RUFF) format . --check

.PHONY: typecheck
typecheck:                     ## Run static type checks with mypy
	$(MYPY) -p blueprints

#─────────────────────────────────────────────────────────────────────────────
# Testing targets
#─────────────────────────────────────────────────────────────────────────────
.PHONY: test
test:                          ## Run tests with pytest (parallel execution)
	$(PYTEST) tests/ -n auto

.PHONY: test-verbose
test-verbose:                  ## Run tests with pytest (verbose output)
	$(PYTEST) tests/ --verbose -n auto

.PHONY: test-light
test-light:                    ## Run tests with pytest (lightweight, excludes slow tests)
	$(PYTEST) tests/ --verbose -m "not slow"

.PHONY: check-coverage
check-coverage:                ## Run tests and check 100% coverage
	$(COVERAGE) --cov-report term-missing:skip-covered --cov-fail-under=100

.PHONY: coverage-report
coverage-report:               ## Run tests and generate coverage reports
	$(COVERAGE) --cov-report=xml

.PHONY: coverage-html
coverage-html:                 ## Run tests and generate an html coverage report
	$(COVERAGE) --cov-report html

#─────────────────────────────────────────────────────────────────────────────
# Build targets
#─────────────────────────────────────────────────────────────────────────────
.PHONY: build
build:                         ## Build the project
	$(BUILD)

#─────────────────────────────────────────────────────────────────────────────
# Cleanup
#─────────────────────────────────────────────────────────────────────────────
.PHONY: clean
clean:                         ## Remove venv and all build/test artifacts
	@rm -rf .venv htmlcov .pytest_cache .mypy_cache .ruff_cache .coverage;\
	echo "Cleaned up all build/test artifacts and virtual environment"
