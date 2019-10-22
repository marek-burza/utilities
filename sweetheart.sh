#!/bin/sh
# Diastolic more important before 50

set -e

export MSYS_NO_PATHCONV=1
export DATA=$(cygpath -w $PWD)

rm apple* fitbit* health* *png *timestamped.csv 2> /dev/null || true

docker run --rm -it -v $DATA:/data altermarkive/apple-health-to-csv /data/export.zip /data/apple.raw.csv
docker run --rm -it -v $DATA:/data altermarkive/csv-select /data/apple.raw.csv /data/apple.selected.csv HKQuantityTypeIdentifierBloodPressureDiastolicendDate HKQuantityTypeIdentifierBloodPressureDiastolicvalue HKQuantityTypeIdentifierBloodPressureSystolicendDate HKQuantityTypeIdentifierBloodPressureSystolicvalue HKQuantityTypeIdentifierHeartRateendDate HKQuantityTypeIdentifierHeartRatesourceName HKQuantityTypeIdentifierHeartRatevalue HKQuantityTypeIdentifierDistanceWalkingRunningendDate HKQuantityTypeIdentifierDistanceWalkingRunningvalue HKQuantityTypeIdentifierStepCountendDate HKQuantityTypeIdentifierStepCountvalue
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.selected.csv /data/apple.stamped.1.csv HKQuantityTypeIdentifierBloodPressureDiastolicendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.stamped.1.csv /data/apple.stamped.2.csv HKQuantityTypeIdentifierBloodPressureSystolicendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.stamped.2.csv /data/apple.stamped.3.csv HKQuantityTypeIdentifierHeartRateendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.stamped.3.csv /data/apple.stamped.4.csv HKQuantityTypeIdentifierDistanceWalkingRunningendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.stamped.4.csv /data/apple.stamped.csv HKQuantityTypeIdentifierStepCountendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-rename /data/apple.stamped.csv /data/apple.renamed.csv HKQuantityTypeIdentifierBloodPressureDiastolicvalue HKQuantityTypeIdentifierBloodPressureSystolicvalue HKQuantityTypeIdentifierHeartRatesourceName HKQuantityTypeIdentifierHeartRatevalue HKQuantityTypeIdentifierDistanceWalkingRunningvalue HKQuantityTypeIdentifierStepCountvalue Diastolic Systolic 'Heart Monitor' 'Heart Rate' 'Walking Distance' 'Step Count'
docker run --rm -it -v $DATA:/data altermarkive/csv-select /data/apple.renamed.csv /data/apple.ready.csv Timestamp Diastolic Systolic 'Heart Monitor' 'Heart Rate' 'Walking Distance' 'Step Count'

docker run --rm -it -v $DATA:/data altermarkive/fitbit-to-csv /data/MyFitbitData.zip /data/fitbit.raw.csv
docker run --rm -it -v $DATA:/data altermarkive/csv-select /data/fitbit.raw.csv /data/fitbit.selected.csv Weight.bmi Weight.date Weight.time Weight.weight
docker run --rm -it -v $DATA:/data altermarkive/csv-join /data/fitbit.selected.csv /data/fitbit.local.csv ' ' Weight.date Weight.time Local
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/fitbit.local.csv /data/fitbit.stamped.csv Local Timestamp '%m/%d/%y %H:%M:%S'
docker run --rm -it -v $DATA:/data altermarkive/csv-rename /data/fitbit.stamped.csv /data/fitbit.renamed.csv Weight.bmi Weight.weight BMI Weight
docker run --rm -it -v $DATA:/data altermarkive/csv-select /data/fitbit.renamed.csv /data/fitbit.ready.csv Timestamp BMI Weight

docker run --rm -it -v $DATA:/data altermarkive/csv-concatenate /data/apple.ready.csv /data/fitbit.ready.csv /data/health.raw.csv

docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-to-local /data/health.raw.csv /data/health.dated.csv Timestamp Date '%Y.%m.%d'

docker run --rm -it -v $DATA:/data altermarkive/csv-split-by-time-of-day /data/health.dated.csv /data/health.splitted.csv Timestamp 'Heart Rate' Diastolic Systolic

docker run --rm -it -v $DATA:/data altermarkive/csv-aggregate /data/health.splitted.csv /data/health.grouped.csv Date '{"Heart Monitor": ["collect"], "Walking Distance": ["sum"], "Step Count": ["sum"], "BMI": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Weight": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Heart Rate": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Diastolic": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Systolic": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Heart Rate Night": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Heart Rate Morning": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Heart Rate Afternoon": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Heart Rate Evening": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Diastolic Night": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Diastolic Morning": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Diastolic Afternoon": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Diastolic Evening": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Systolic Night": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Systolic Morning": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Systolic Afternoon": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"], "Systolic Evening": ["count", "first", "last", "min", "max", "mean", "median", "std", "var"]}'

docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/health.grouped.csv /data/health.timestamped.csv Date Timestamp '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-to-season /data/health.timestamped.csv /data/health.seasons.csv Timestamp Season '1. Spring' '2. Summer' '3. Autumn' '4. Winter'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-to-weekend /data/health.seasons.csv /data/health.weekends.csv Timestamp Weekend
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-to-local /data/health.weekends.csv /data/health.months.csv Timestamp Month '%m. %B'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-to-local /data/health.months.csv /data/health.weekdays.csv Timestamp Weekday '%w. %A'

docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apart.csv /data/apart.timestamped.csv From From '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apart.timestamped.csv /data/apart.timestamped.csv To To '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-range-label /data/health.weekdays.csv /data/health.together.csv Timestamp /data/apart.timestamped.csv From To '' Together Label Together

docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/medication.csv /data/medication.timestamped.csv From From '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/medication.timestamped.csv /data/medication.timestamped.csv To To '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-range-label /data/health.together.csv /data/health.medications.csv Timestamp /data/medication.timestamped.csv From To '' '' Medication Medication

docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/switch.csv /data/switch.timestamped.csv From From '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/switch.timestamped.csv /data/switch.timestamped.csv To To '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-range-label /data/health.medications.csv /data/health.switch.csv Timestamp /data/switch.timestamped.csv From To '' 'No Switch' Label Switch

docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/vacation.csv /data/vacation.timestamped.csv From From '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/vacation.timestamped.csv /data/vacation.timestamped.csv To To '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-range-label /data/health.switch.csv /data/health.vacations.csv Timestamp /data/vacation.timestamped.csv From To '' 'No Vacation' Label Vacation

docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/planning.csv /data/planning.timestamped.csv From From '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/planning.timestamped.csv /data/planning.timestamped.csv To To '%Y.%m.%d'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-range-label /data/health.vacations.csv /data/health.planning.csv Timestamp /data/planning.timestamped.csv From To '' 'No Planning' 'Planning' 'Planning' '' 'No Planning' 'Planning Detailed' 'Planning Detailed'

docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-to-weekend /data/health.planning.csv /data/health.combined.1.csv Timestamp Combined
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-range-label /data/health.combined.1.csv /data/health.combined.2.csv Timestamp /data/apart.timestamped.csv From To '' '' Label Combined
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-range-label /data/health.combined.2.csv /data/health.combined.3.csv Timestamp /data/vacation.timestamped.csv From To '' '' Label Combined
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-range-label /data/health.combined.3.csv /data/health.combined.csv Timestamp /data/planning.timestamped.csv From To '' '' 'Planning Detailed' Combined

docker run --rm -it -v $DATA:/data altermarkive/csv-interpolate /data/health.combined.csv /data/health.interpolated.1.csv Timestamp 'BMI first' 'BMI first'
docker run --rm -it -v $DATA:/data altermarkive/csv-interpolate /data/health.interpolated.1.csv /data/health.interpolated.csv Timestamp 'Weight first' 'Weight first'

docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/01.DiastolicTogether.png 'Diastolic first' Together
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/01.DiastolicTogether.png 'Diastolic first' Together
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/02.DiastolicWeekday.png 'Diastolic first' Weekday
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/03.DiastolicWeekend.png 'Diastolic first' Weekend
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/04.DiastolicMonth.png 'Diastolic first' Month
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/05.DiastolicSeason.png 'Diastolic first' Season
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/06.DiastolicPlanning.png 'Diastolic last' Planning Detailed
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/07.DiastolicMedication.png 'Diastolic first' Medication
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/08.DiastolicVacation.png 'Diastolic first' Vacation
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/09.DiastolicSwitch.png 'Diastolic first' Switch
docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-grouped /data/health.interpolated.csv /data/10.DiastolicCombined.png 'Diastolic first' Combined

docker run --rm -it -v $DATA:/data altermarkive/plot-boxplot-versus /data/health.interpolated.csv /data/11.DiastolicMorningVsEvening.png 'Diastolic Morning first' 'Diastolic Evening last'

docker run --rm -it -v $DATA:/data altermarkive/plot-scatterplot /data/health.interpolated.csv /data/12.WalkingDiastolic.png 'Walking Distance total' 'Diastolic Evening last'
docker run --rm -it -v $DATA:/data altermarkive/plot-scatterplot /data/health.interpolated.csv /data/13.StepDiastolic.png 'Step Count total' 'Diastolic Evening last'
docker run --rm -it -v $DATA:/data altermarkive/plot-scatterplot /data/health.interpolated.csv /data/14.BMIDiastolic.png 'BMI first' 'Diastolic Morning last'
docker run --rm -it -v $DATA:/data altermarkive/plot-scatterplot /data/health.interpolated.csv /data/15.WeightDiastolic.png 'Weight first' 'Diastolic Morning last'
