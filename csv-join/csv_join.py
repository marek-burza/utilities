#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This joins columns in CSV file.
"""

import sys

import pandas


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 6:
        print('USAGE: csv_join.py CSV_FILE DELIMITER COLUMN_1 COLUMN_2 ... COLUMN_JOINED')  # noqa: E501 pylint: disable=unidiomatic-typecheck
    else:
        csv = pandas.read_csv(sys.argv[1])
        delimiter = sys.argv[2]
        columns = sys.argv[3:-1]
        column_joinded = sys.argv[-1]
        columns = csv[columns]
        csv[column_joinded] = columns.apply(delimiter.join, axis=1)
        csv.to_csv(sys.argv[1], index=False)


if __name__ == '__main__':
    main()
