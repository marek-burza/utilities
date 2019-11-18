#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script interpolates across gaps in a column.
"""

import sys

import numpy
import pandas


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 5:
        print('USAGE: csv_interpolate.py CSV_FILE_IN CSV_FILE_OUT COLUMN_REFERENCE COLUMN_IN COLUMN_OUT')  # noqa: E501 pylint: disable=C0301
    else:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
        column_reference = sys.argv[3]
        column_in = sys.argv[4]
        column_out = sys.argv[5]
        data = pandas.read_csv(file_in)
        reference = data[column_reference]
        values = data[column_in]
        nans = numpy.isnan(values)
        values = numpy.interp(reference[nans], reference[~nans], values[~nans])
        data.loc[nans, column_out] = values
        data.to_csv(file_out, index=False)


if __name__ == '__main__':
    main()
