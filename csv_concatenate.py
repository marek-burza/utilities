#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script concatenates multiple CSV files.
"""

import sys
import pandas as pd


def data_concatenate(data, concatenated):
    """
    Concatenates multiple data frames
    """
    for item in data:
        concatenated = concatenated.append(item, sort=False)
    return concatenated


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) <= 1:
        print('USAGE: csv_concatenate.py CSV_1 CSV_2 ... CSV_CONCATENATED')
    else:
        concatenated = pd.DataFrame()
        separate = sys.argv[1:-1]
        data = [pd.read_csv(csv, low_memory=False) for csv in separate]
        data = data_concatenate(data, concatenated)
        data.to_csv(sys.argv[-1], index=False)
