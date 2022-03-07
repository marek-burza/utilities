#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script selects columns in CSV file.
"""

import sys
import dask.dataframe as dd
import pandas as pd


def csv_select(in_file, columns):
    """
    Selects columns in CSV file.
    """
    data = pd.read_csv(in_file, usecols=columns, low_memory=False)
    data = data[columns].dropna(how='all')
    return data


def csv_select_dask(in_file, columns):
    """
    Selects columns in CSV file (using Dask).
    """
    data = pd.read_csv(in_file, usecols=columns, low_memory=False)
    data = dd.from_pandas(data, npartitions=1)
    data = data[columns].dropna(how='all')
    return data


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('USAGE: csv_select.py CSV_FILE_IN CSV_FILE_OUT COLUMN_1 COLUMN_2 ...')  # noqa: E501 pylint: disable=C0301
    else:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
        columns = sys.argv[3:]
        data = csv_select(in_file, columns)
        data.to_csv(sys.argv[2], index=False)
