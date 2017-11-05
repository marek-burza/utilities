# Lab Environment [![Build Status][travis-img]][travis-url]

[travis-url]: https://travis-ci.org/altermarkive/Lab-Environment
[travis-img]: https://travis-ci.org/altermarkive/Lab-Environment.svg?branch=master

Environment for experimenting with Python 3, ML, etc.

To use the environment:

    docker build -t lab .
    docker run -it --rm -v $PWD:/shared -w /shared lab

