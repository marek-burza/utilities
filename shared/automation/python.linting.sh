#!/bin/sh

set -e

SELF=$0
BASE=$(dirname "$0")

DEBIAN_FRONTEND=noninteractive apt-get install build-essential python3-dev

pip3 install $(find $BASE/../.. -name "*.requirements.txt" -exec cat {} \; | sort | uniq)

pip3 install bandit==1.6.2 flake8==3.7.8 pylint==2.3.1 pycodestyle==2.5.0

find . -iname "*.py" | xargs pylint --disable=R0801
pycodestyle .
flake8 *.py
bandit -r .
