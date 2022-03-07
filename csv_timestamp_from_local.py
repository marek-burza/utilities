#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts local date/time to UNIX-epoch timestamp in a CSV file.
"""

import sys
import time

import pandas


def timestamp_from_local(item, pattern):
    """
    Converts local date/time to UNIX-epoch timestamp
    """
    return time.mktime(time.strptime(item, pattern))


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 5:
        print('USAGE: csv_timestamp_from_local.py CSV_FILE_IN CSV_FILE_OUT COLUMN_FROM COLUMN_TO PATTERN')  # noqa: E501 pylint: disable=C0301
    else:
        csv = pandas.read_csv(sys.argv[1])
        column_from = sys.argv[3]
        column_to = sys.argv[4]
        pattern = sys.argv[5]
        applicable = csv[column_from].notnull()
        if column_to not in csv:
            csv[column_to] = float('nan')
        csv.loc[applicable, column_to] = csv[applicable][column_from].apply(
            lambda item: timestamp_from_local(item, pattern))
        csv.to_csv(sys.argv[2], index=False)


if __name__ == '__main__':
    main()
