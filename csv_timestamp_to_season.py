#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts UNIX-epoch timestamp to season in a CSV file.
"""

import datetime
import sys
import time
import numpy as np
import pandas as pd


def overlaps(when, spans):
    """
    Checks an overlap of a datetime with list of datetime spans.
    """
    for start, stop in spans:
        if start <= when <= stop:
            return True
    return False


def season_index(timestamp):
    """
    Checks overlap of the timestamp with each season.
    """
    leap_year = 2000
    when = time.strftime('2000%m%d', time.localtime(timestamp))
    when = time.mktime(time.strptime(when, '%Y%m%d'))
    when = datetime.datetime.fromtimestamp(when).date()
    spring = [(datetime.date(leap_year, 3, 21),
               datetime.date(leap_year, 6, 20))]
    summer = [(datetime.date(leap_year, 6, 21),
               datetime.date(leap_year, 9, 22))]
    autumn = [(datetime.date(leap_year, 9, 23),
               datetime.date(leap_year, 12, 20))]
    winter = [(datetime.date(leap_year, 1, 1),
               datetime.date(leap_year, 3, 20)),
              (datetime.date(leap_year, 12, 21),
               datetime.date(leap_year, 12, 31))]
    seasons = [spring, summer, autumn, winter]
    for index, season in enumerate(seasons):
        if overlaps(when, season):
            return index
    return -1


def timestamp_to_season(item, seasons):
    """
    Converts UNIX-epoch timestamp to season.
    """
    return seasons[season_index(item)]


def data_timestamp_to_season(data, column_from, column_to, seasons):
    """
    Converts UNIX-epoch timestamp to season
    """
    applicable = data[column_from].notnull()
    if column_to not in data:
        data[column_to] = np.nan
    data.loc[applicable, column_to] = data[applicable][column_from].apply(
        lambda item: timestamp_to_season(item, seasons))
    return data


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 9:
        print('USAGE: csv_timestamp_to_season.py CSV_FILE_IN CSV_FILE_OUT COLUMN_FROM COLUMN_TO SPRING_NAME SUMMER_NAME AUTUMN_NAME WINTER_NAME')  # noqa: E501 pylint: disable=C0301
    else:
        csv = pd.read_csv(sys.argv[1], low_memory=False)
        column_from = sys.argv[3]
        column_to = sys.argv[4]
        seasons = sys.argv[5:]
        csv = data_timestamp_to_season(csv, column_from, column_to, seasons)
        csv.to_csv(sys.argv[2], index=False)
