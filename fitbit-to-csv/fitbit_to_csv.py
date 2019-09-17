#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts the Fitbit data export to a denormalized CSV format.
"""

import functools
import json
import logging
import sys
import zipfile


def logger():
    """
    Initiates a logger to be used by the script
    """
    pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=pattern, level=logging.INFO)
    return logging.getLogger('fitbit-to-csv')


def extract_hr_zones(structured, prefix, entry):
    """
    Extracts a HR zone information.
    """
    for zone in structured:
        name = zone['name']
        minutes = zone['minutes']
        entry[f'{prefix}.activityLevel.{name}.minutes'] = minutes


def extract_core(structured, ignored, prefix, entry, log):
    """
    Flattens a nested dictionary.
    """
    for key in structured:
        item = structured[key]
        if key in ignored:
            continue
        elif isinstance(item, dict):
            extract_core(item, ignored, f'{prefix}.{key}', entry, log)
        elif key == 'memberSince':
            '-'.join([str(item) for item in structured[key]])
        elif key == 'heartRateZones':
            extract_hr_zones(item, prefix, entry)
        else:
            entry[f'{prefix}.{key}'] = item


def extract_basic(listed, ignored, prefix, flat, log):
    """
    Extract the information with a basic nested format.
    """
    for structured in listed:
        entry = {}
        extract_core(structured, ignored, prefix, entry, log)
        flat.append(entry)


def extract_user_profile(structured, flat, log):
    """
    Extract the user profile information.
    """
    entry = {}
    extract_core(structured, ['topBadges'], 'UserProfile', entry, log)
    flat.append(entry)


def extract_sleep(listed, flat, log):
    """
    Extract the sleep information.
    """
    extract_basic(listed, ['data'], 'Sleep', flat, log)
    for item in listed:
        extract_basic(item['levels']['data'], [], 'SleepBlock', flat, log)


def extract_one_from_fitbit_export(name, structured, flat, log):
    """
    Extracts data into a dictionary entry for CSV.
    """
    lut = {
        'badge': {'prefix': 'Badge', 'ignored': []},
        'calories': {'prefix': 'Calories', 'ignored': []},
        'demographic_vo2_max': {'prefix': 'VO2', 'ignored': []},
        'distance': {'prefix': 'Distance', 'ignored': []},
        'exercise': {'prefix': 'Exercise', 'ignored': []},
        'food_logs': {'prefix': 'Food', 'ignored': ['unit', 'units']},
        'heart_rate': {'prefix': 'HR', 'ignored': []},
        'height': {'prefix': 'Height', 'ignored': []},
        'lightly_active_minutes': {'prefix': 'Lightly', 'ignored': []},
        'moderately_active_minutes': {'prefix': 'Moderately', 'ignored': []},
        'resting_heart_rate': {'prefix': 'HRResting', 'ignored': []},
        'sedentary_minutes': {'prefix': 'Sedentary', 'ignored': []},
        'steps': {'prefix': 'Steps', 'ignored': []},
        'swim_lengths_data': {'prefix': 'Swim', 'ignored': []},
        'time_in_heart_rate_zones': {'prefix': 'HRZones', 'ignored': []},
        'very_active_minutes': {'prefix': 'Very', 'ignored': []},
        'weight': {'prefix': 'Weight', 'ignored': []}
    }
    if '/user-profile/User-Profile.json' in name:
        extract_user_profile(structured, flat, log)
    elif 'sleep' in name:
        extract_sleep(structured, flat, log)
    else:
        matched = False
        for match in lut:
            if match in name:
                prefix = lut[match]['prefix']
                ignored = lut[match]['ignored']
                extract_basic(structured, ignored, prefix, flat, log)
                matched = True
                break
        if not matched:
            log.warning(f'Skipping {name}')


def extract_all_from_fitbit_export(export, flat, log):
    """
    Extracts data into a list of dictionary entries for CSV.
    """
    for name in export.namelist():
        if not name.endswith('.json'):
            continue
        with export.open(name) as handle:
            structured = json.loads(handle.read().decode('utf-8'))
            extract_one_from_fitbit_export(name, structured, flat, log)


def load_fitbit_export(path, flat, log):
    """
    Loads a ZIP file with Fitbit data export.
    """
    with zipfile.ZipFile(path) as export:
        extract_all_from_fitbit_export(export, flat, log)


def collect_keys(table):
    """
    Collects all names of keys (columns) used throughout the data.
    """
    just_keys = map(lambda entry: set(entry.keys()), table)
    return sorted(list(functools.reduce(set.union, just_keys)))


def stringify(value):
    """
    Escapes a string to be usable as cell content of a CSV formatted data.
    """
    stringified = '' if value is None else str(value)
    if ',' in stringified:
        stringified = stringified.replace('"', '""')
        stringified = f'"{stringified}"'
    return stringified


def store_converted_line(values, csv):
    """
    Convert a list of values into a CSV line.
    """
    values = [stringify(value) for value in values]
    line = ','.join(values)
    line = '%s\n' % line
    csv.write(line.encode('utf-8'))


def store_converted_csv(flat, path):
    """
    Store converted data line by line in CSV format.
    """
    keys = collect_keys(flat)
    with open(path, 'wb') as csv:
        store_converted_line(keys, csv)
        for entry in flat:
            values = [entry.get(key, None) for key in keys]
            store_converted_line(values, csv)


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 3:
        print('USAGE: fitbit_to_csv.py FITBIT_ZIP CONVERTED_CSV')
    else:
        log = logger()
        flat = []
        load_fitbit_export(sys.argv[1], flat, log)
        store_converted_csv(flat, sys.argv[2])


if __name__ == '__main__':
    main()
