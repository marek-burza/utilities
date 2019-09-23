#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts UNIX-epoch timestamp to weekend in a CSV file.
"""

import math
import sys
import time

import pandas


def timestamp_to_weekend(item):
    """
    Converts UNIX-epoch timestamp to weekend.
    """
    if isinstance(item, float) and math.isnan(item):
        return float('nan')
    when = time.localtime(item)
    return 'Weekend' if when.tm_wday in [5, 6] else 'Weekday'


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 4:
        print('USAGE: csv_timestamp_to_weekend.py CSV_FILE COLUMN_FROM COLUMN_TO')  # noqa: E501 pylint: disable=unidiomatic-typecheck
    else:
        csv = pandas.read_csv(sys.argv[1])
        column_from = sys.argv[2]
        column_to = sys.argv[3]
        csv[column_to] = csv[column_from].apply(timestamp_to_weekend)
        csv.to_csv(sys.argv[1], index=False)


if __name__ == '__main__':
    main()
