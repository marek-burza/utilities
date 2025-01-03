#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Diastolic more important before 50

import glob
import os
import time
from apple_health_to_csv import *
from data_aggregate import *
from data_interpolate import *
from data_join import *
from data_select import *
from data_rename import *
from data_split_by_time_of_day import *
from data_timestamp_from_local import *
from data_timestamp_to_local import *
from data_timestamp_range_label import *
from data_timestamp_to_season import *
from data_timestamp_to_weekend import *
from plot_boxplot_grouped import *
from plot_boxplot_versus import *
from plot_scatterplot import *


if __name__ == '__main__':
    before = time.time()

    for path in glob.glob('apple.*'):
        os.remove(path)
    for path in glob.glob('health*'):
        os.remove(path)
    for path in glob.glob('*png'):
        os.remove(path)
    for path in glob.glob('*timestamped.csv'):
        os.remove(path)

    apple_health_to_csv('export.zip', 'apple.raw.csv')
    apple_selected = data_select(
        'apple.raw.csv',
        [
            'HKQuantityTypeIdentifierBloodPressureDiastolicendDate',
            'HKQuantityTypeIdentifierBloodPressureDiastolicvalue',
            'HKQuantityTypeIdentifierBloodPressureSystolicendDate',
            'HKQuantityTypeIdentifierBloodPressureSystolicvalue',
            'HKQuantityTypeIdentifierHeartRateendDate',
            'HKQuantityTypeIdentifierHeartRatesourceName',
            'HKQuantityTypeIdentifierHeartRatevalue',
            'HKQuantityTypeIdentifierDistanceWalkingRunningendDate',
            'HKQuantityTypeIdentifierDistanceWalkingRunningvalue',
            'HKQuantityTypeIdentifierStepCountendDate',
            'HKQuantityTypeIdentifierStepCountvalue',
            'HKQuantityTypeIdentifierBodyMassendDate',
            'HKQuantityTypeIdentifierBodyMassvalue',
            'HKQuantityTypeIdentifierBodyMassIndexendDate',
            'HKQuantityTypeIdentifierBodyMassIndexvalue',
        ]
    )

    apple_stamped = data_timestamp_from_local(
        apple_selected,
        'HKQuantityTypeIdentifierBloodPressureDiastolicendDate',
        'Timestamp',
        '%Y-%m-%d %H:%M:%S %z'
    )
    apple_stamped = data_timestamp_from_local(
        apple_stamped,
        'HKQuantityTypeIdentifierBloodPressureSystolicendDate',
        'Timestamp',
        '%Y-%m-%d %H:%M:%S %z'
    )
    apple_stamped = data_timestamp_from_local(
        apple_stamped,
        'HKQuantityTypeIdentifierHeartRateendDate',
        'Timestamp',
        '%Y-%m-%d %H:%M:%S %z'
    )
    apple_stamped = data_timestamp_from_local(
        apple_stamped,
        'HKQuantityTypeIdentifierDistanceWalkingRunningendDate',
        'Timestamp',
        '%Y-%m-%d %H:%M:%S %z'
    )
    apple_stamped = data_timestamp_from_local(
        apple_stamped,
        'HKQuantityTypeIdentifierStepCountendDate',
        'Timestamp',
        '%Y-%m-%d %H:%M:%S %z'
    )
    apple_stamped = data_timestamp_from_local(
        apple_stamped,
        'HKQuantityTypeIdentifierBodyMassendDate',
        'Timestamp',
        '%Y-%m-%d %H:%M:%S %z'
    )
    apple_stamped = data_timestamp_from_local(
        apple_stamped,
        'HKQuantityTypeIdentifierBodyMassIndexendDate',
        'Timestamp',
        '%Y-%m-%d %H:%M:%S %z'
    )

    apple_renamed = data_rename(
        apple_stamped,
        {
            'HKQuantityTypeIdentifierBloodPressureDiastolicvalue': 'Diastolic',
            'HKQuantityTypeIdentifierBloodPressureSystolicvalue': 'Systolic',
            'HKQuantityTypeIdentifierHeartRatesourceName': 'Heart Monitor',
            'HKQuantityTypeIdentifierHeartRatevalue': 'Heart Rate',
            'HKQuantityTypeIdentifierDistanceWalkingRunningvalue': 'Walking Distance',
            'HKQuantityTypeIdentifierStepCountvalue': 'Step Count',
            'HKQuantityTypeIdentifierBodyMassvalue': 'Weight',
            'HKQuantityTypeIdentifierBodyMassIndexvalue': 'BMI',
        }
    )
    columns = [
        'Timestamp',
        'Diastolic',
        'Systolic',
        'Heart Monitor',
        'Heart Rate',
        'Walking Distance',
        'Step Count',
        'Weight',
        'BMI',
    ]
    health_raw = apple_renamed.loc[:, columns]

    health_dated = data_timestamp_to_local(
        health_raw,
        'Timestamp',
        'Date',
        '%Y.%m.%d'
    )

    health_splitted = data_split_by_time_of_day(
        health_dated,
        'Timestamp',
        ['Heart Rate', 'Diastolic', 'Systolic']
    )

    aspects = [
        'count', 'first', 'last', 'min', 'max', 'mean', 'median', 'std', 'var'
    ]
    health_grouped = data_aggregate(
        health_splitted,
        'Date',
        {
            'Heart Monitor': ['collect'],
            'Walking Distance': ['sum'],
            'Step Count': ['sum'],
            'BMI': aspects,
            'Weight': aspects,
            'Heart Rate': aspects,
            'Diastolic': aspects,
            'Systolic': aspects,
            'Heart Rate Night': aspects,
            'Heart Rate Morning': aspects,
            'Heart Rate Afternoon': aspects,
            'Heart Rate Evening': aspects,
            'Diastolic Night': aspects,
            'Diastolic Morning': aspects,
            'Diastolic Afternoon': aspects,
            'Diastolic Evening': aspects,
            'Systolic Night': aspects,
            'Systolic Morning': aspects,
            'Systolic Afternoon': aspects,
            'Systolic Evening': aspects,
        }
    )

    health_timestamped = data_timestamp_from_local(
        health_grouped,
        'Date',
        'Timestamp',
        '%Y.%m.%d'
    )
    health_seasons = data_timestamp_to_season(
        health_timestamped,
        'Timestamp',
        'Season',
        ['1. Spring', '2. Summer', '3. Autumn', '4. Winter']
    )
    health_weekends = data_timestamp_to_weekend(
        health_seasons,
        'Timestamp',
        'Weekend'
    )
    health_months = data_timestamp_to_local(
        health_weekends,
        'Timestamp',
        'Month',
        '%m. %B'
    )
    health_weekdays = data_timestamp_to_local(
        health_months,
        'Timestamp',
        'Weekday',
        '%w. %A'
    )

    apart = pd.read_csv('apart.csv', low_memory=False)
    apart_timestamped = data_timestamp_from_local(apart, 'From', 'From', '%Y.%m.%d')
    apart_timestamped = data_timestamp_from_local(apart_timestamped, 'To', 'To', '%Y.%m.%d')
    health_together = data_timestamp_range_label(
        health_weekdays,
        'Timestamp',
        apart_timestamped,
        'From',
        'To',
        [('', 'Together', 'Label', 'Together')]
    )

    medication = pd.read_csv('medication.csv', low_memory=False)
    medication_timestamped = data_timestamp_from_local(medication, 'From', 'From', '%Y.%m.%d')
    medication_timestamped = data_timestamp_from_local(medication_timestamped, 'To', 'To', '%Y.%m.%d')
    health_medications = data_timestamp_range_label(
        health_together,
        'Timestamp',
        medication_timestamped,
        'From',
        'To',
        [('', '', 'Medication', 'Medication')]
    )

    switch = pd.read_csv('switch.csv', low_memory=False)
    switch_timestamped = data_timestamp_from_local(switch, 'From', 'From', '%Y.%m.%d')
    switch_timestamped = data_timestamp_from_local(switch_timestamped, 'To', 'To', '%Y.%m.%d')
    health_switch = data_timestamp_range_label(
        health_medications,
        'Timestamp',
        switch_timestamped,
        'From',
        'To',
        [('', 'No Switch', 'Label', 'Switch')]
    )

    vacation = pd.read_csv('vacation.csv', low_memory=False)
    vacation_timestamped = data_timestamp_from_local(vacation, 'From', 'From', '%Y.%m.%d')
    vacation_timestamped = data_timestamp_from_local(vacation_timestamped, 'To', 'To', '%Y.%m.%d')
    health_vacation = data_timestamp_range_label(
        health_switch,
        'Timestamp',
        vacation_timestamped,
        'From',
        'To',
        [('', 'No Vacation', 'Label', 'Vacation')]
    )

    planning = pd.read_csv('planning.csv', low_memory=False)
    planning_timestamped = data_timestamp_from_local(planning, 'From', 'From', '%Y.%m.%d')
    planning_timestamped = data_timestamp_from_local(planning_timestamped, 'To', 'To', '%Y.%m.%d')
    health_planning = data_timestamp_range_label(
        health_vacation,
        'Timestamp',
        planning_timestamped,
        'From',
        'To',
        [
            ('', 'No Planning', 'Planning', 'Planning'),
            ('', 'No Planning', 'Planning Detailed', 'Planning Detailed'),
        ]
    )

    health_combined = data_timestamp_to_weekend(
        health_planning,
        'Timestamp',
        'Combined'
    )
    health_combined = data_timestamp_range_label(
        health_combined,
        'Timestamp',
        vacation_timestamped,
        'From',
        'To',
        [('', '', 'Label', 'Combined')]
    )
    health_combined = data_timestamp_range_label(
        health_combined,
        'Timestamp',
        planning_timestamped,
        'From',
        'To',
        [('', '', 'Planning Detailed', 'Combined')]
    )

    health_interpolated = data_interpolate(health_combined, 'Timestamp', 'BMI first', 'BMI first')
    health_interpolated = data_interpolate(health_interpolated, 'Timestamp', 'Weight first', 'Weight first')

    boxplot_grouped(health_interpolated, 'Diastolic first', 'Together', '01.DiastolicTogether.png')
    boxplot_grouped(health_interpolated, 'Diastolic first', 'Weekday', '02.DiastolicWeekday.png')
    boxplot_grouped(health_interpolated, 'Diastolic first', 'Weekend', '03.DiastolicWeekend.png')
    boxplot_grouped(health_interpolated, 'Diastolic first', 'Month', '04.DiastolicMonth.png')
    boxplot_grouped(health_interpolated, 'Diastolic first', 'Season', '05.DiastolicSeason.png')
    boxplot_grouped(health_interpolated, 'Diastolic first', 'Planning Detailed', '06.DiastolicPlanning.png')
    boxplot_grouped(health_interpolated, 'Diastolic first', 'Medication', '07.DiastolicMedication.png')
    boxplot_grouped(health_interpolated, 'Diastolic first', 'Vacation', '08.DiastolicVacation.png')
    boxplot_grouped(health_interpolated, 'Diastolic first', 'Switch', '09.DiastolicSwitch.png')
    boxplot_grouped(health_interpolated, 'Diastolic first', 'Combined', '10.DiastolicCombined.png')

    boxplot_versus(health_interpolated, ['Diastolic Morning first', 'Diastolic Evening last'], '11.DiastolicMorningVsEvening.png')

    scatterplot(health_interpolated, 'Walking Distance total', 'Diastolic Evening last', '12.WalkingDiastolic.png')
    scatterplot(health_interpolated, 'Step Count total', 'Diastolic Evening last', '13.StepDiastolic.png')
    scatterplot(health_interpolated, 'BMI first', 'Diastolic Morning last', '14.BMIDiastolic.png')
    scatterplot(health_interpolated, 'Weight first', 'Diastolic Morning last', '15.WeightDiastolic.png')

    after = time.time()
    print(int(after - before))
