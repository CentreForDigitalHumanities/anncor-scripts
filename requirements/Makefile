objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

all: $(outputs)
deploy.txt: conversion.txt selection.txt
develop.txt: deploy.txt

%.txt: %.in
	pip-compile -v --output-file $@ $<

check:
	@which pip-compile > /dev/null

clean: check
	- rm *.txt
