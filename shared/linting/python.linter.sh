#!/bin/sh
# USAGE: docker run -it -v $PWD/shared/linting/python.linter.sh:/python.linter.sh -w /app --entrypoint=/bin/sh $IMAGE /python.linter.sh

set -e

apk add --update --no-cache build-base
pip3 install bandit==1.6.2 flake8==3.7.8 pylint==2.3.1 pycodestyle==2.5.0

cd /app

find . -iname "*.py" | xargs pylint --disable=R0801
pycodestyle .
flake8 *.py
bandit -r .
