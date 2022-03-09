#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates a scatter plot for given columns.
"""

import sys
import matplotlib.pyplot
import numpy as np
import pandas as pd


def scatterplot(data, column_x, column_y, file_out):
    """
    Creates a scatter plot for given columns
    """
    figure, axes = matplotlib.pyplot.subplots()
    figure.set_figwidth(12.80)
    figure.set_figheight(7.20)
    figure.set_dpi(100)
    columns = [column_x, column_y]
    data = data[columns]
    data = data[~np.isnan(data).any(axis=1)]
    matplotlib.pyplot.scatter(data[column_x], data[column_y])
    axes.set_xlabel(column_x)
    axes.set_ylabel(column_y)
    matplotlib.pyplot.title(
        '%s vs. %s (n=%d)' % (column_x, column_y, data.shape[0]))
    matplotlib.pyplot.tight_layout()
    figure.savefig(file_out)
    matplotlib.pyplot.close()


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) != 5:
        print('USAGE: plot_scatterplot.py CSV_FILE_IN PNG_FILE_OUT COLUMN_X COLUMN_Y')  # noqa: E501 pylint: disable=C0301
    else:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
        column_x = sys.argv[3]
        column_y = sys.argv[4]
        data = pd.read_csv(file_in, low_memory=False)
        scatterplot(data, column_x, column_y, file_out)
