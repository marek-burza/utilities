#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script joins columns in CSV file.
"""

import sys
import pandas as pd


def join(items, delimiter):
    """
    Custom join which skips NaN values
    """
    return delimiter.join(items.dropna())


def data_join(data, delimiter, columns, column_joinded):
    """
    Joins columns
    """
    columns = data[columns]
    data[column_joinded] = columns.apply(
        lambda item: join(item, delimiter), axis=1)
    return data


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 7:
        print('USAGE: csv_join.py CSV_FILE_IN CSV_FILE_OUT DELIMITER COLUMN_1 COLUMN_2 ... COLUMN_JOINED')  # noqa: E501 pylint: disable=C0301
    else:
        csv = pd.read_csv(sys.argv[1])
        delimiter = sys.argv[3]
        columns = sys.argv[4:-1]
        column_joinded = sys.argv[-1]
        csv = data_join(csv, delimiter, columns, column_joinded)
        csv.to_csv(sys.argv[2], index=False)
