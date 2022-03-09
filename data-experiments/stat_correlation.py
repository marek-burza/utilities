#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script computes pairwise correlation of columns.
"""

import json
import re
import sys
import pandas as pd


ARGUMENTS = {
    'method': 'pearson',
    'min_periods': 1,
}


def stat_correlation(data, arguments):
    """
    Computes pairwise correlation of columns
    """
    default = ARGUMENTS.copy()
    default.update(arguments)
    arguments = default
    if isinstance(arguments['columns'], list):
        columns = arguments['columns']
    if isinstance(arguments['columns'], str):
        pattern = re.compile(arguments['columns'])
        columns = list(filter(pattern.search, data.columns))
    data = data[columns].corr()
    return data


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 2:
        print('USAGE: stat_correlation.py JSON_ARGUMENTS')
    else:
        arguments = json.loads(sys.argv[1])
        data = pd.read_csv(arguments['input_file'], low_memory=False)
        data = stat_correlation(data, arguments)
        data.to_csv(arguments['output_file'], index=False)
