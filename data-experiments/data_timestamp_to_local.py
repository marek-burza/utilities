#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts UNIX-epoch timestamp to local date/time in a CSV file.
"""

import sys
import time
import numpy as np
import pandas as pd


def timestamp_to_local(item, pattern):
    """
    Converts single UNIX-epoch timestamp to local date/time
    """
    return time.strftime(pattern, time.localtime(item))


def data_timestamp_to_local(data, column_from, column_to, pattern):
    """
    Converts UNIX-epoch timestamp to local date/time
    """
    applicable = data[column_from].notnull()
    if column_to not in data:
        data[column_to] = np.nan
    data.loc[applicable, column_to] = data[applicable][column_from].apply(
        lambda item: timestamp_to_local(item, pattern))
    return data


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 6:
        print('USAGE: csv_timestamp_to_local.py CSV_FILE_IN CSV_FILE_OUT COLUMN_FROM COLUMN_TO PATTERN')  # noqa: E501 pylint: disable=C0301
    else:
        csv = pd.read_csv(sys.argv[1], low_memory=False)
        column_from = sys.argv[3]
        column_to = sys.argv[4]
        pattern = sys.argv[5]
        csv = data_timestamp_to_local(csv, column_from, column_to, pattern)
        csv.to_csv(sys.argv[2], index=False)
