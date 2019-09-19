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
    if len(sys.argv) < 4 and len(sys.argv) % 2 != 0:
        print('USAGE: csv_rename.py CSV_FILE COLUMN_1_FROM COLUMN_2_FROM ... COLUMN_1_TO COLUMN_2_TO ...')  # noqa: E501 pylint: disable=C0301
    else:
        csv = pandas.read_csv(sys.argv[1])
        flat = sys.argv[2:]
        half = len(flat) // 2
        before = flat[:half]
        after = flat[half:]
        translation = dict(zip(before, after))
        csv.rename(columns=translation, inplace=True)
        csv.to_csv(sys.argv[1], index=False)


if __name__ == '__main__':
    main()
