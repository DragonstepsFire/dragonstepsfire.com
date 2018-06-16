.PHONY: clean clean-build clean-pyc clean-test docs lint type-check test
	.DEFAULT_GOAL := help

help: ## show Makefile help (default target)
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-ivy clean-pyc clean-docs ## remove all build, test, coverage, docs, and Python file artifacts

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage

clean-docs:  ## remove docs artifacts
	$(MAKE) -C docs clean

check-origin-remote:
	# A remote named origin MUST exist.
	@git remote show origin

tag-release: check-origin-remote
	# This doesn't have help text because it's intended to be a release helper.
	$(eval VERSION := "v$(shell sed -rn "s/__version__ = [\'\"](.*)[\'\"]/\1/p" $(SRC))")
	git tag -a $(VERSION) -m "Release $(VERSION)"
	git push origin $(VERSION)
