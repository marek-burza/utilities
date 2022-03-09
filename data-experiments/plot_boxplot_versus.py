#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates a box plot for given columns.
"""

import sys

import matplotlib.pyplot
import numpy as np
import pandas as pd


def boxplot_versus(data, columns, file_out):
    """
    Creates a box plot for given columns
    """
    figure, axes = matplotlib.pyplot.subplots()
    figure.set_figwidth(12.80)
    figure.set_figheight(7.20)
    figure.set_dpi(100)
    data = data[columns]
    data = data[~np.isnan(data).any(axis=1)]
    data.boxplot(column=columns, ax=axes)
    counts = np.count_nonzero(~np.isnan(data), axis=0)
    labels = []
    for i, label in enumerate(axes.get_xticklabels()):
        text = label.get_text()
        labels.append('%s\n(n=%d)' % (text, counts[i]))
    axes.set_xticklabels(labels, rotation=90)
    matplotlib.pyplot.suptitle('')
    matplotlib.pyplot.title('')
    matplotlib.pyplot.tight_layout()
    figure.savefig(file_out)
    matplotlib.pyplot.close()


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 5:
        print('USAGE: plot_boxplot_versus.py CSV_FILE_IN PNG_FILE_OUT COLUMN_1 ...')  # noqa: E501 pylint: disable=C0301
    else:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
        columns = sys.argv[3:]
        data = pd.read_csv(file_in, low_memory=False)
        boxplot_versus(data, columns, file_out)
