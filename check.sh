#!/bin/sh
echo "running isort" && poetry run isort vplaylist/
echo "running black" && poetry run black vplaylist/
echo "running ruff"  && poetry run ruff check vplaylist/
echo "running mypy" && poetry run mypy vplaylist/
