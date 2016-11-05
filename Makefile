#
# Project:   xonotic-map-manager
# Copyright: (c) 2016 by Tyler Mulligan <z@xnz.me> and contributors
# License:   MIT, see the LICENSE file for more details
#
# A GNU Makefile for the project.
#

.PHONY: help clean lint docs tests tests-coverage

help:
	@echo "Use \`make <target>', where <target> is one of the following:"
	@echo "  clean          - remove all generated files"
	@echo "  lint           - check code style with flake8"
	@echo "  docs           - make docs"
	@echo "  tests          - run tests"
	@echo "  tests-coverage - obtain test coverage"

clean:
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.py[co]' -exec rm -f {} +
	@rm -rf .tox

lint:
	@flake8 --ignore=E221,E501,F401,F841,E128 xmm/*.py

docs: docs/
	@cd docs && $(MAKE) html

tests:
	@py.test

tests-coverage:
	@tox