#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts local date/time to UNIX-epoch timestamp in a CSV file.
"""

import math
import sys
import time

import pandas


def timestamp_from_local(item, pattern):
    """
    Converts local date/time to UNIX-epoch timestamp
    """
    if isinstance(item, float) and math.isnan(item):
        return float('nan')
    return time.mktime(time.strptime(item, pattern))


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 4:
        print('USAGE: csv_timestamp_from_local.py CSV_FILE COLUMN_FROM COLUMN_TO PATTERN')  # noqa: E501 pylint: disable=unidiomatic-typecheck
    else:
        csv = pandas.read_csv(sys.argv[1])
        column_from = sys.argv[2]
        column_to = sys.argv[3]
        pattern = sys.argv[4]
        csv[column_to] = csv[column_from].apply(
            lambda item: timestamp_from_local(item, pattern))
        csv.to_csv(sys.argv[1], index=False)


if __name__ == '__main__':
    main()
