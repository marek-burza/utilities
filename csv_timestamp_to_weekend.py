#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts UNIX-epoch timestamp to weekend in a CSV file.
"""

import sys
import time
import numpy as np
import pandas as pd


def timestamp_to_weekend(item):
    """
    Converts UNIX-epoch timestamp to weekend.
    """
    when = time.localtime(item)
    return 'Weekend' if when.tm_wday in [5, 6] else 'Weekday'


def data_timestamp_to_weekend(data, column_from, column_to):
    """
    Converts UNIX-epoch timestamp to weekend
    """
    applicable = data[column_from].notnull()
    if column_to not in data:
        data[column_to] = np.nan
    data.loc[applicable, column_to] = data[applicable][column_from].apply(
        timestamp_to_weekend)
    return data


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 5:
        print('USAGE: csv_timestamp_to_weekend.py CSV_FILE_IN CSV_FILE_OUT COLUMN_FROM COLUMN_TO')  # noqa: E501 pylint: disable=unidiomatic-typecheck
    else:
        csv = pd.read_csv(sys.argv[1], low_memory=False)
        column_from = sys.argv[3]
        column_to = sys.argv[4]
        csv = data_timestamp_to_weekend(csv, column_from, column_to)
        csv.to_csv(sys.argv[2], index=False)
