#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script selects columns in CSV file.
"""

import sys

import pandas


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 4:
        print('USAGE: csv_select.py CSV_FILE_IN CSV_FILE_OUT COLUMN_1 COLUMN_2 ...')  # noqa: E501 pylint: disable=C0301
    else:
        csv = pandas.read_csv(sys.argv[1])
        columns = sys.argv[3:]
        csv = csv[columns]
        csv.to_csv(sys.argv[2], index=False)


if __name__ == '__main__':
    main()
