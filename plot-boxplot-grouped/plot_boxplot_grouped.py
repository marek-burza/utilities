#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script interpolates labels a column.
"""

import sys

import matplotlib.pyplot
import pandas


def boxplot_grouped(file_in, column, column_groups, file_out):
    """
    Creates a box plot for the given value and group columns
    """
    data = pandas.read_csv(file_in)
    figure, axes = matplotlib.pyplot.subplots()
    figure.set_figwidth(12.80)
    figure.set_figheight(7.20)
    figure.set_dpi(100)
    data[[column, column_groups]].boxplot(
        column=[column], by=column_groups, ax=axes)
    grouped = data[[column, column_groups]].groupby([column_groups]).count()
    labels = []
    for i, label in enumerate(axes.get_xticklabels()):
        text = label.get_text()
        count = grouped[column][i]
        labels.append('%s\n(n=%d)' % (text, count))
    axes.set_xticklabels(labels, rotation=90)
    matplotlib.pyplot.ylabel(column)
    matplotlib.pyplot.xlabel(column_groups)
    matplotlib.pyplot.suptitle('')
    matplotlib.pyplot.title('')
    matplotlib.pyplot.tight_layout()
    figure.savefig(file_out)
    matplotlib.pyplot.close()


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 5:
        print('USAGE: plot_boxplot_grouped.py CSV_FILE_IN PNG_FILE_OUT COLUMN_VALUES COLUMN_GROUPS')  # noqa: E501 pylint: disable=C0301
    else:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
        column_values = sys.argv[3]
        column_groups = sys.argv[4]
        boxplot_grouped(file_in, column_values, column_groups, file_out)


if __name__ == '__main__':
    main()
