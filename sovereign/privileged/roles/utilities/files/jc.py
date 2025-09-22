#!/usr/bin/python3

import os
import sys


os.system(f'uv run --with jc jc {" ".join(sys.argv[1:])}')
