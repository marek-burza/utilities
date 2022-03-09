#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script labels a column depending on given timestamp ranges.
"""

import math
import sys
import numpy as np
import pandas as pd


# pylint: disable-msg=R0913
def labeler(row, timestamps, values, lut, begins, ends, labels):
    """
    Looks up the label for a given timestamp
    """
    for _, lut_row in lut.iterrows():
        begin = lut_row[begins]
        begin = -sys.maxsize - 1 if math.isnan(begin) else begin
        end = lut_row[ends]
        end = sys.maxsize if math.isnan(end) else end
        if begin <= row[timestamps] <= end:
            return lut_row[labels]
    return row[values]


def prepare_labeling(column_from, column_label_default, column_to, data):
    """
    Prepares the data for labeling
    """
    if column_label_default == '':
        column_label_default = np.nan
    if column_from != '':
        data[column_to] = data[column_from]
    if column_to not in data:
        data[column_to] = column_label_default
    applicable = data[column_to].isnull()
    data.loc[applicable, column_to] = column_label_default


def apply_labeling(timestamps, timestamps_begin, timestamps_end, column_label_from, column_to, lut, data):  # noqa: E501 pylint: disable=C0301
    """
    Applies labeling
    """
    data[column_to] = data[[timestamps, column_to]].apply(
        lambda row: labeler(
            row, timestamps, column_to,
            lut, timestamps_begin, timestamps_end, column_label_from),
        axis=1)


def data_timestamp_range_label(data, timestamps, lut, timestamps_begin, timestamps_end, column_config):  # noqa: E501 pylint: disable=C0301
    """
    Labels a column depending on given timestamp ranges
    """
    for config in column_config:
        col_from, col_label_default, col_label_from, col_to = config
        prepare_labeling(
            col_from, col_label_default, col_to, data)
        apply_labeling(
            timestamps, timestamps_begin, timestamps_end,
            col_label_from, col_to, lut, data)
    return data


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 9 or (len(sys.argv) - 7) % 4 != 0:
        print('USAGE: csv_timestamp_range_label.py CSV_FILE_IN CSV_FILE_OUT TIMESTAMPS CSV_FILE_LABELS TIMESTAMPS_BEGIN TIMESTAMPS_END COLUMN_FROM_1 COLUMN_LABEL_DEFAULT_1 COLUMN_LABEL_FROM_1 COLUMN_TO_1 ...')  # noqa: E501 pylint: disable=C0301
    else:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
        timestamps = sys.argv[3]
        file_labels = sys.argv[4]
        timestamps_begin = sys.argv[5]
        timestamps_end = sys.argv[6]
        lut = pd.read_csv(file_labels, low_memory=False)
        data = pd.read_csv(file_in, low_memory=False)
        column_config = []
        for offset in range(7, len(sys.argv), 4):
            col_from = sys.argv[offset + 0]
            col_label_default = sys.argv[offset + 1]
            col_label_from = sys.argv[offset + 2]
            col_to = sys.argv[offset + 3]
            column_config.append(
                (col_from, col_label_default, col_label_from, col_to)
            )
        data = data_timestamp_range_label(
            data,
            timestamps,
            lut,
            timestamps_begin,
            timestamps_end,
            column_config
        )
        data.to_csv(file_out, index=False)
