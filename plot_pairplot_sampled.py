#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates a sampled pair plot for given columns.
"""

import json
import re
import sys

import matplotlib.pyplot
import pandas


def pairplot_sampled(arguments):
    """
    Creates a sampled pair plot for given columns
    """
    data = pandas.read_csv(arguments['input_file'])
    if isinstance(arguments['feature_columns'], list):
        feature_columns = arguments['feature_columns']
    if isinstance(arguments['feature_columns'], str):
        pattern = re.compile(arguments['feature_columns'])
        feature_columns = list(filter(pattern.search, data.columns))
    feature_count = len(feature_columns)
    class_column = arguments['class_column']
    figure, axis = matplotlib.pyplot.subplots(
        nrows=feature_count, ncols=feature_count)
    figure.set_figwidth(arguments['width'])
    figure.set_figheight(arguments['height'])
    figure.set_dpi(arguments['dpi'])
    data = data.sample(n=arguments['n'])
    for i in range(feature_count):
        for j in range(feature_count):
            if i == j:
                axis[i, j].hist(data[feature_columns[i]])
            else:
                axis[i, j].scatter(
                    data[feature_columns[i]], data[feature_columns[j]],
                    c=data[class_column], marker='.')
            axis[i, j].set_xticklabels([])
            axis[i, j].set_xticks([])
            axis[i, j].set_yticklabels([])
            axis[i, j].set_yticks([])
    figure.savefig(arguments['output_file'])


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 2:
        print('USAGE: plot_pairplot_sampled.py JSON_ARGUMENTS')
    else:
        arguments = {
            'title': '',
            'width': 28.8,
            'height': 28.8,
            'dpi': 100
            }
        arguments.update(json.loads(sys.argv[1]))
        pairplot_sampled(arguments)


if __name__ == '__main__':
    main()
