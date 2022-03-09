#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script splits the value from a given column into separate ones
depending on time of day (night, morning, afternoon, evening).
"""

import sys
import time
import numpy as np
import pandas as pd


def copy_if_hour_in_range(item, timestamps, column, from_hour, to_hour):
    """
    Returns the value from given value if timestamp in given range
    or Nan otherwise
    """
    hour = time.localtime(item[timestamps]).tm_hour
    in_range = from_hour <= hour < to_hour
    return item[column] if in_range else np.nan


# pylint: disable-msg=R0913
def split_off(data, name, applicable, timestamps, column, from_hour, to_hour):
    """
    Splits off given column based on hour range
    """
    splitted = f'{column} {name}'
    data[splitted] = np.nan
    origin = data[applicable][[timestamps, column]]
    data.loc[applicable, splitted] = origin.apply(
        lambda item: copy_if_hour_in_range(
            item, timestamps, column, from_hour, to_hour), axis=1)


def data_split_by_time_of_day(data, timestamps, splitting):
    """
    Splits the value from a given column into separate ones
    depending on time of day (night, morning, afternoon, evening).
    """
    applicable = data[timestamps].notnull()
    for column in splitting:
        split_off(
            data, 'Night', applicable, timestamps, column, 0, 6)
        split_off(
            data, 'Morning', applicable, timestamps, column, 6, 12)
        split_off(
            data, 'Afternoon', applicable, timestamps, column, 12, 18)
        split_off(
            data, 'Evening', applicable, timestamps, column, 18, 24)
    return data


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 5:
        print('USAGE: csv_split_by_time_of_day.py CSV_FILE_IN CSV_FILE_OUT TIMESTAMP_COLUMN SPLIT_COLUMN_1 ...')  # noqa: E501 pylint: disable=C0301
    else:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
        timestamps = sys.argv[3]
        splitting = sys.argv[4:]
        data = pd.read_csv(file_in, low_memory=False)
        data = data_split_by_time_of_day(data, timestamps, splitting)
        data.to_csv(file_out, index=False)
