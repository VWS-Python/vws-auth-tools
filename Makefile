SHELL := /bin/bash -euxo pipefail

include lint.mk

# Treat Sphinx warnings as errors
SPHINXOPTS := -W

.PHONY: lint
lint: \
    actionlint \
    check-manifest \
    deptry \
    doc8 \
    ruff \
    linkcheck \
    mypy \
    pyproject-fmt \
    pyroma \
    pyright \
    pyright-verifytypes \
    spelling \
    vulture \
    pylint

.PHONY: fix-lint
fix-lint: \
    fix-pyproject-fmt \
    fix-ruff

.PHONY: docs
docs:
	make -C docs clean html SPHINXOPTS=$(SPHINXOPTS)

.PHONY: open-docs
open-docs:
	python -c 'import os, webbrowser; webbrowser.open("file://" + os.path.abspath("docs/build/html/index.html"))'
