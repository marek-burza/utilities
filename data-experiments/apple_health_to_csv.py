#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script converts the Apple Health data export to a denormalized CSV format.
The scripts expects the HealthKit Export version 8 format.
"""

import logging
import functools
import sys
import zipfile

import defusedxml.minidom


def logger():
    """
    Initiates a logger to be used by the script
    """
    pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=pattern, level=logging.INFO)
    return logging.getLogger('apple-health-to-csv')


def collect_attributes(prefix, element, entry, log):
    """
    Collects all attributes of XML element in a dictionary.
    The attribute names are also prefixed.
    """
    for key in element.attributes.keys():
        value = element.attributes[key].value
        key = f'{prefix}{key}'
        if key in entry:
            log.warning(f'Overwriting {entry[key]} with {value} for {key}')
        entry[key] = value


def collect_metadata(prefix, element, entry, log):
    """
    Collects all metadata entries in a dictionary.
    The attribute names are also prefixed.
    """
    for child in element.childNodes:
        if child.nodeType == child.TEXT_NODE:
            continue
        if child.tagName == 'MetadataEntry':
            key = child.attributes['key'].value
            key = f'{prefix}{key}'
            value = child.attributes['value'].value
            if key in entry:
                log.warning(f'Overwriting {entry[key]} with {value} for {key}')
            entry[key] = value


def extract_simple_entry(element, flat, log):
    """
    Turns a simple (non-nested) XML element into a dictionary entry for CSV.
    """
    entry = {}
    collect_attributes(element.tagName, element, entry, log)
    flat.append(entry)


def extract_bpm_entries(prefix, record, flat, log):
    """
    Extracts 'InstantaneousBeatsPerMinute' element
    into dictionary entries for CSV.
    """
    prefix = f'{prefix}InstantaneousBeatsPerMinute'
    for element in record.getElementsByTagName('InstantaneousBeatsPerMinute'):
        entry = {}
        collect_attributes(prefix, element, entry, log)
        flat.append(entry)


def extract_record_entry(prefix, record, flat, log):
    """
    Extracts 'Record' element into a dictionary entry for CSV.
    """
    record_type = record.attributes['type'].value
    record_prefix = f'{prefix}{record_type}'
    entry = {}
    collect_attributes(record_prefix, record, entry, log)
    collect_metadata(record_prefix, record, entry, log)
    flat.append(entry)
    extract_bpm_entries(prefix, record, flat, log)


def extract_correlation_entry(correlation, flat, log):
    """
    Extracts 'Correlation' element into a dictionary entry for CSV.
    """
    prefix = 'Correlation'
    entry = {}
    collect_attributes(prefix, correlation, entry, log)
    collect_metadata(prefix, correlation, entry, log)
    flat.append(entry)
    elements = correlation.getElementsByTagName('InstantaneousBeatsPerMinute')
    for element in elements:
        extract_record_entry(prefix, element, flat, log)


def extract_route_entry(route, flat, log):
    """
    Extracts 'WorkoutRoute' element into a dictionary entry for CSV.
    """
    prefix = 'WorkoutRoute'
    entry = {}
    collect_attributes(prefix, route, entry, log)
    collect_metadata(prefix, route, entry, log)
    flat.append(entry)
    for element in route.getElementsByTagName('Location'):
        extract_simple_entry(element, flat, log)


def extract_workout_entry(correlation, flat, log):
    """
    Extracts 'Workout' element into a dictionary entry for CSV.
    """
    prefix = 'Workout'
    entry = {}
    collect_attributes(prefix, correlation, entry, log)
    collect_metadata(prefix, correlation, entry, log)
    flat.append(entry)
    for element in correlation.getElementsByTagName('WorkoutEntry'):
        extract_simple_entry(element, flat, log)
    for element in correlation.getElementsByTagName('WorkoutRoute'):
        extract_route_entry(element, flat, log)


def extract_all_from_apple_export(export, flat, log):
    """
    Extracts data into a list of dictionary entries for CSV.
    """
    with export.open('apple_health_export/export.xml') as handle:
        structured = defusedxml.minidom.parse(handle)
        for child in structured.documentElement.childNodes:
            if child.nodeType == child.TEXT_NODE:
                continue
            if child.tagName == 'ExportDate':
                extract_simple_entry(child, flat, log)
            elif child.tagName == 'Me':
                extract_simple_entry(child, flat, log)
            elif child.tagName == 'Record':
                extract_record_entry('', child, flat, log)
            elif child.tagName == 'Correlation':
                extract_correlation_entry(child, flat, log)
            elif child.tagName == 'ActivitySummary':
                extract_simple_entry(child, flat, log)
            elif child.tagName == 'ClinicalRecord':
                extract_simple_entry(child, flat, log)


def load_apple_export(path, flat, log):
    """
    Loads a ZIP file with Apple Health data export.
    """
    with zipfile.ZipFile(path) as export:
        extract_all_from_apple_export(export, flat, log)


def collect_keys(table):
    """
    Collects all names of keys (columns) used throughout the data
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


def apple_health_to_csv(apple_health, csv):
    """
    Converts Apple Health data export to CSV
    """
    log = logger()
    flat = []
    load_apple_export(apple_health, flat, log)
    store_converted_csv(flat, csv)


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 3:
        print('USAGE: apple-health-to-csv.py APPLE_HEALTH_ZIP CONVERTED_CSV')
    else:
        apple_health_to_csv(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
