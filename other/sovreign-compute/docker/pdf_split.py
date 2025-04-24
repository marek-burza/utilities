#!/usr/bin/python3

import os
import sys


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    os.system(f'pdfseparate -f 1 -l 1 {sys.argv[1]} %03d.{sys.argv[1]}')
