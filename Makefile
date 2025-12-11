# Default Shell to use
SHELL := /bin/bash

# Absolute path of the directory of this script
root_dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: help run-container

help:
	@echo "Makefile commands:"
	@echo "  run-container - Run an interactive Python 3.11 container"

run-container:
	docker run --rm -it \
	  --volume="$(root_dir):/app:Z" \
	  --workdir=/app \
	  python:3.11-slim \
	  /bin/bash
