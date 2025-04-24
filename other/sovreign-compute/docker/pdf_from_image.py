#!/usr/bin/python3

import os
import sys


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)
    os.system(f'convert {sys.argv[1]} {sys.argv[2]}')
