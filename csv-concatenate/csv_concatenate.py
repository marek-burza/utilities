#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script concatenates two CSV files.
"""

import sys

import pandas


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) <= 1:
        print('USAGE: csv_concatenate.py CSV_1 CSV_2 ... CSV_CONCATENATED')
    else:
        concatenated = pandas.DataFrame()
        separate = sys.argv[1:-1]
        for csv in separate:
            csv = pandas.read_csv(csv)
            concatenated = concatenated.append(csv, sort=False)
        concatenated.to_csv(sys.argv[-1], index=False)


if __name__ == '__main__':
    main()
