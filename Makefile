# Set python variables required by package
OUTPUT_DIR=dist
REQUIREMENTS=requirements.txt
SOURCE=crs_normalizer
PACKAGE=true
OUTPUT_FILENAME=crs-normalizer-layer

# Set default target for make > 3.80
.DEFAULT_GOAL := default

define PRINT_HELP_PYSCRIPT
import re, sys

for f in sys.argv[1:]:
    with open(f, 'r') as handle:
        for line in handle.readlines():
            match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
            if match:
                target, help = match.groups()
                print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

.PHONY: help
help: ## Show this help message
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" $(MAKEFILE_LIST)

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

include $(current_dir)/internal-utils.mk

eq = $(and $(findstring $(1),$(2)),$(findstring $(2),$(1)))

SHELL := /bin/bash
PYTHON := python
SETUP := setup.py

SOURCE ?= src
COV_FAIL_UNDER ?= 100

USE_DOCKER ?= $(if $(call eq,$(CI),true),false,true)
DOCKER_IMAGE ?= $(shell basename $$PWD)
DOCKER_FILE ?= Dockerfile

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
    from urllib import pathname2url
except:
    from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef

BROWSER := $(PYTHON) -c "$$BROWSER_PYSCRIPT"

#
# Beginning of targets

.PHONY: all
all: clean check lint test type-check package ## Run all targets

.PHONY: start
start: CMD=bash
start: build-container ## Run the development docker container
	@$(call run,$(CMD))

.PHONY: build-container
build-container: ## Build the development docker container
	@docker build -t $(DOCKER_IMAGE) --build-arg LOCAL_UID=$$(id -u) --build-arg LOCAL_GID=$$(id -g) -f $(DOCKER_FILE) .

define run
if [ "$(USE_DOCKER)" == "true" ]; then \
    $(MAKE) build-container; \
    docker run -it -v $$PWD:/home/python/app -w /home/python/app -u $$(id -u):$$(id -g) -e USE_DOCKER=false $(DOCKER_IMAGE) /bin/bash -c "$1"; \
else \
    $1; \
fi
endef

.PHONY: lint
lint: CMD=set -o pipefail ; $(PYTHON) -m pylint -f parseable $(SOURCE) tests | tee pylint.log
lint: ## Run linting for the project
	@$(call run,$(CMD))

.PHONY: test
test: CMD=$(PYTHON) -m pytest --verbose --junitxml=test-report.xml
test: ## Run project test suite
	@$(call run,$(CMD))

.PHONY: coverage
coverage: CMD=$(PYTHON) -m pytest \
	--cov-report=term \
	--cov-report=xml \
	--cov-report=html \
	--cov-fail-under=$(COV_FAIL_UNDER) \
	--cov=$(SOURCE) tests
coverage: ## Check code coverage quickly with the default Python
	@$(call run,$(CMD))

.PHONY: check
check: CMD=$(PYTHON) $(SETUP) check
check: ## Run the projects setup.py check
	@$(call run,$(CMD))

# Package python wheel
.PHONY: package
package: CMD=mkdir -p dist && \
	$(PYTHON) $(SETUP) sdist && \
	$(PYTHON) $(SETUP) bdist_wheel
package: check ## Package the project wheel
	@$(call run,$(CMD))

.PHONY: clean
clean: CMD=$(PYTHON) $(SETUP) clean && \
	find . \( -name '__pycache__' -or -name '__pycache__' \) -exec rm -rf {} + || \
	rm -f .coverage || \
	rm -fr htmlcov/ || \
	rm -fr coverage.xml || \
	rm -fr .pytest_cache || \
	true
clean: ## Clean the project directory
	@$(call run,$(CMD))

.PHONY: type-check
type-check: CMD=$(PYTHON) -m mypy --ignore-missing-imports \
	--disallow-untyped-defs $(SOURCE)
type-check: ## Run a type check over all project Type Hints.
	@$(call run,$(CMD))

.PHONY: serve-coverage
serve-coverage: USE_DOCKER=false
serve-coverage: htmlcov/index.html ## serve the coverage stats in a browser that are produced by `make coverage`
	$(BROWSER) htmlcov/index.html
