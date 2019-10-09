#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script selects columns in CSV file.
"""

import csv
import operator
import sys

import pandas


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 4:
        print('USAGE: csv_select.py CSV_FILE_IN CSV_FILE_OUT COLUMN_1 COLUMN_2 ...')  # noqa: E501 pylint: disable=C0301
    else:
        with open(sys.argv[1], 'r') as handle_in:
            reader = csv.DictReader(handle_in)
            columns = sys.argv[3:]
            values = operator.itemgetter(*columns)
            with open(sys.argv[2], 'w') as handle_out:
                writer = csv.DictWriter(handle_out, fieldnames=columns)
                writer.writeheader()
                for row in reader:
                    writer.writerow(dict(zip(columns, values(row))))
        data = pandas.read_csv(sys.argv[2])
        data = data[columns].dropna(how='all')
        data.to_csv(sys.argv[2], index=False)


if __name__ == '__main__':
    main()
