#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts UNIX-epoch timestamp to season in a CSV file.
"""

import datetime
import math
import sys
import time

import pandas


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
    if isinstance(item, float) and math.isnan(item):
        return float('nan')
    return seasons[season_index(item)]


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 8:
        print('USAGE: csv_timestamp_to_season.py CSV_FILE COLUMN_FROM COLUMN_TO SPRING_NAME SUMMER_NAME AUTUMN_NAME WINTER_NAME')  # noqa: E501 pylint: disable=C0301
    else:
        csv = pandas.read_csv(sys.argv[1])
        column_from = sys.argv[2]
        column_to = sys.argv[3]
        seasons = sys.argv[4:]
        csv[column_to] = csv[column_from].apply(
            lambda item: timestamp_to_season(item, seasons))
        csv.to_csv(sys.argv[1], index=False)


if __name__ == '__main__':
    main()
