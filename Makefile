.PHONY: list requirements test flake
.DEFAULT_GOAL := venv

SHELL := /bin/bash

list:
	@(grep -oe '^[[:lower:][:digit:]_\-]\{1,\}' Makefile | uniq)

venv:
	virtualenv -p python3 --no-site-packages ./venv
	./venv/bin/pip install --quiet --upgrade pip pip-tools

requirements: venv
	./venv/bin/pip-compile --upgrade \
		--output-file requirements.txt \
		requirements.in

test: venv
	./venv/bin/pip install --quiet --upgrade \
		-r ./requirements.txt -e .[test]

	./venv/bin/pytest --cov servitor/ -v .

flake: MAXLINELEN := 79
flake: venv
	@(./venv/bin/flake8 servitor \
		--max-line-length=$(MAXLINELEN) \
		--exit-zero --statistics)
