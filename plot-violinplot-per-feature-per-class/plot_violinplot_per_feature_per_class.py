#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates a violin plot.
"""

import json
import math
import re
import sys

import matplotlib.pyplot
import pandas


def violinplot(arguments):
    """
    Creates a fiddle plot
    """
    data = pandas.read_csv(arguments['input_file'])
    if isinstance(arguments['feature_columns'], list):
        feature_columns = arguments['feature_columns']
    if isinstance(arguments['feature_columns'], str):
        pattern = re.compile(arguments['feature_columns'])
        feature_columns = list(filter(pattern.search, data.columns))
    feature_count = len(feature_columns)
    class_column = arguments['class_column']
    size = math.ceil(math.sqrt(feature_count))
    figure, axes = matplotlib.pyplot.subplots(
        nrows=size, ncols=size)
    figure.set_figwidth(arguments['width'])
    figure.set_figheight(arguments['height'])
    figure.set_dpi(arguments['dpi'])
    for i, feature_column in enumerate(feature_columns):
        at_x = i % size
        at_y = i // size
        feature_data = data[[feature_column, class_column]]
        feature_data = feature_data.groupby(class_column)
        feature_data = feature_data[feature_column].apply(list)
        axes[at_y, at_x].violinplot(
            feature_data,
            points=arguments['points'],
            widths=0.9,
            showmeans=False,
            showextrema=False,
            showmedians=False,
            bw_method=arguments['bw_method'])
        axes[at_y, at_x].boxplot(
            feature_data,
            notch=arguments['notch'],
            sym=arguments['sym'],
            widths=0.3)
        axes[at_y, at_x].set_title(
            feature_column,
            fontsize=arguments['font_size'],
            fontweight=arguments['font_weight'])
        axes[at_y, at_x].set_xticklabels(feature_data.index)
    for i in range(len(feature_columns), size * size):
        at_x = i % size
        at_y = i // size
        axes[at_y, at_x].axis('off')
    if arguments['title'] is not None:
        figure.suptitle(arguments['title'])
    figure.subplots_adjust(wspace=0.5)
    figure.savefig(arguments['output_file'])
    matplotlib.pyplot.close()


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 2:
        print('USAGE: plot_violinplot_per_feature_per_class.py JSON_ARGUMENTS')
    else:
        arguments = {
            'title': None,
            'width': 12.80,
            'height': 7.20,
            'dpi': 100,
            'font_size': 10,
            'font_weight': 'normal',
            'points': 100,
            'bw_method': None,
            'notch': False,
            'sym': None
        }
        arguments.update(json.loads(sys.argv[1]))
        violinplot(arguments)


if __name__ == '__main__':
    main()
