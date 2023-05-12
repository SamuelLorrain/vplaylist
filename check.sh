#!/bin/sh
poetry run black vplaylist/
poetry run ruff check vplaylist/
