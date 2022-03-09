#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script statistically aggregates a CSV file.
"""

import json
import sys
import numpy as np
import pandas as pd


def count(series):
    """
    Count of non-Nan elements of a series
    """
    return series.dropna().size


def first(series):
    """
    First non-Nan element of a series or NaN if an empty series
    """
    series = series.dropna()
    if series.size == 0:
        return np.nan
    return series.iloc[0]


def last(series):
    """
    Last non-Nan element of a series or NaN if an empty series
    """
    series = series.dropna()
    if series.size == 0:
        return np.nan
    return series.iloc[-1]


def minimum(series):
    """
    Minimum of a series or NaN if an empty series
    """
    series = series.dropna()
    if series.size == 0:
        return np.nan
    return np.nanmin(series)


def maximum(series):
    """
    Maximum of a series or NaN if an empty series
    """
    series = series.dropna()
    if series.size == 0:
        return np.nan
    return np.nanmax(series)


def mean(series):
    """
    Mean of a series or NaN if an empty series
    """
    series = series.dropna()
    if series.size == 0:
        return np.nan
    return np.nanmean(series)


def median(series):
    """
    Median of a series or NaN if an empty series
    """
    series = series.dropna()
    if series.size == 0:
        return np.nan
    return np.nanmedian(series)


def std(series):
    """
    Standard deviation of a series or NaN if an empty series
    """
    series = series.dropna()
    if series.size == 0:
        return np.nan
    return np.nanstd(series)


def variance(series):
    """
    Variance of a series or NaN if an empty series
    """
    series = series.dropna()
    if series.size == 0:
        return np.nan
    return np.nanvar(series)


def total(series):
    """
    Sum of a series or NaN if an empty series
    """
    series = series.dropna()
    if series.size == 0:
        return np.nan
    return np.nansum(series)


def collect(series):
    """
    Collects a set of all possible values
    """
    collected = set(series.dropna())
    collected = sorted([str(item) for item in collected])
    return ' '.join(collected)


def translate_name_to_function(name):
    """
    Translates name of a function into a function
    """
    lut = {
        'count': count,
        'first': first,
        'last': last,
        'min': minimum,
        'max': maximum,
        'mean': mean,
        'median': median,
        'std': std,
        'var': variance,
        'sum': total,
        'collect': collect
    }
    return lut[name]


def translate_all_names_to_function(aggregation):
    """
    Parses the aggregation
    """
    for key in aggregation.keys():
        names = aggregation[key]
        functions = [translate_name_to_function(name) for name in names]
        aggregation[key] = functions
    return aggregation


def data_aggregate(data, index, aggregation):
    """
    Statistically aggregates data
    """
    values = list(data.columns)
    values.remove(index)
    aggregation = translate_all_names_to_function(aggregation)
    data = pd.pivot_table(
        data,
        index=index,
        values=values,
        aggfunc=aggregation)
    data.columns = data.columns.map(' '.join).str.strip()
    data.reset_index(level=0, inplace=True)
    return data


if __name__ == '__main__':
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 5:
        print('USAGE: csv_aggregate.py CSV_RAW CSV_AGGREGATED INDEX_COLUMN AGGREGATION_JSON')  # noqa: E501 pylint: disable=C0301
    else:
        data = pd.read_csv(sys.argv[1], low_memory=False)
        index = sys.argv[3]
        aggregation = json.loads(sys.argv[4])
        data = data_aggregate(data, index, aggregation)
        data.to_csv(sys.argv[2])
