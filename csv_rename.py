#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script renames columns in CSV file.
"""

import sys
import pandas as pd


def data_rename(data, translation):
    """
    Renames columns.
    """
    data.rename(columns=translation, inplace=True)
    return data


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 5 and len(sys.argv) % 2 == 0:
        print('USAGE: csv_rename.py CSV_FILE_IN CSV_FILE_OUT COLUMN_1_FROM COLUMN_2_FROM ... COLUMN_1_TO COLUMN_2_TO ...')  # noqa: E501 pylint: disable=C0301
    else:
        csv = pd.read_csv(sys.argv[1], low_memory=False)
        flat = sys.argv[3:]
        half = len(flat) // 2
        before = flat[:half]
        after = flat[half:]
        translation = dict(zip(before, after))
        csv = data_rename(csv, translation)
        csv.to_csv(sys.argv[2], index=False)
