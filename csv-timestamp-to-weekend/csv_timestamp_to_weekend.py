#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts UNIX-epoch timestamp to weekend in a CSV file.
"""

import sys
import time

import pandas


def timestamp_to_weekend(item):
    """
    Converts UNIX-epoch timestamp to weekend.
    """
    when = time.localtime(item)
    return 'Weekend' if when.tm_wday in [5, 6] else 'Weekday'


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 5:
        print('USAGE: csv_timestamp_to_weekend.py CSV_FILE_IN CSV_FILE_OUT COLUMN_FROM COLUMN_TO')  # noqa: E501 pylint: disable=unidiomatic-typecheck
    else:
        csv = pandas.read_csv(sys.argv[1])
        column_from = sys.argv[3]
        column_to = sys.argv[4]
        applicable = csv[column_from].notnull()
        if column_to not in csv:
            csv[column_to] = float('nan')
        csv.loc[applicable, column_to] = csv[applicable][column_from].apply(
            timestamp_to_weekend)
        csv.to_csv(sys.argv[2], index=False)


if __name__ == '__main__':
    main()
