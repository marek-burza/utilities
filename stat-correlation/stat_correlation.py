#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script computes pairwise correlation of columns.
"""

import json
import re
import sys

import pandas


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 2:
        print('USAGE: stat_correlation.py JSON_ARGUMENTS')
    else:
        arguments = {'method': 'pearson', 'min_periods': 1}
        arguments.update(json.loads(sys.argv[1]))
        data = pandas.read_csv(arguments['input_file'])
        if isinstance(arguments['columns'], list):
            columns = arguments['columns']
        if isinstance(arguments['columns'], str):
            pattern = re.compile(arguments['columns'])
            columns = list(filter(pattern.search, data.columns))
        data = data[columns].corr()
        data.to_csv(arguments['output_file'], index=False)


if __name__ == '__main__':
    main()
