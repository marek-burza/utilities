#!/bin/sh

set -e

find . -iname "*.py" | xargs pylint
pycodestyle .
flake8 *.py
bandit -r .
