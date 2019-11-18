#!/bin/sh

set -e

pip3 --disable-pip-version-check install bandit==1.6.2 flake8==3.7.8 pycodestyle==2.5.0 pylint==2.3.1

find . -iname "*.py" | xargs pylint --disable=R0801
pycodestyle .
flake8 *.py
bandit -r .
