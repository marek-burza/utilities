#!/bin/sh

set -e

export MSYS_NO_PATHCONV=1
export DATA=$(cygpath -w $PWD)

docker run --rm -it -v $DATA:/data altermarkive/apple-health-to-csv /data/export.zip /data/apple.csv
docker run --rm -it -v $DATA:/data altermarkive/csv-select /data/apple.csv /data/apple.selected.csv HKQuantityTypeIdentifierBloodPressureDiastolicendDate HKQuantityTypeIdentifierBloodPressureDiastolicvalue HKQuantityTypeIdentifierBloodPressureSystolicendDate HKQuantityTypeIdentifierBloodPressureSystolicvalue HKQuantityTypeIdentifierHeartRateendDate HKQuantityTypeIdentifierHeartRatesourceName HKQuantityTypeIdentifierHeartRatevalue HKQuantityTypeIdentifierDistanceWalkingRunningendDate HKQuantityTypeIdentifierDistanceWalkingRunningvalue HKQuantityTypeIdentifierStepCountendDate HKQuantityTypeIdentifierStepCountvalue
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.selected.csv /data/apple.stamped.1.csv HKQuantityTypeIdentifierBloodPressureDiastolicendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.stamped.1.csv /data/apple.stamped.2.csv HKQuantityTypeIdentifierBloodPressureSystolicendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.stamped.2.csv /data/apple.stamped.3.csv HKQuantityTypeIdentifierHeartRateendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.stamped.3.csv /data/apple.stamped.4.csv HKQuantityTypeIdentifierDistanceWalkingRunningendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/apple.stamped.4.csv /data/apple.stamped.csv HKQuantityTypeIdentifierStepCountendDate Timestamp '%Y-%m-%d %H:%M:%S %z'
docker run --rm -it -v $DATA:/data altermarkive/csv-rename /data/apple.stamped.csv /data/apple.renamed.csv HKQuantityTypeIdentifierBloodPressureDiastolicvalue HKQuantityTypeIdentifierBloodPressureSystolicvalue HKQuantityTypeIdentifierHeartRatesourceName HKQuantityTypeIdentifierHeartRatevalue HKQuantityTypeIdentifierDistanceWalkingRunningvalue HKQuantityTypeIdentifierStepCountvalue Diastolic Systolic 'Heart Monitor' 'Heart Rate' 'Walking Distance' 'Step Count'
docker run --rm -it -v $DATA:/data altermarkive/csv-select /data/apple.renamed.csv /data/apple.ready.csv Timestamp Diastolic Systolic 'Heart Monitor' 'Heart Rate' 'Walking Distance' 'Step Count'

docker run --rm -it -v $DATA:/data altermarkive/fitbit-to-csv /data/MyFitbitData.zip /data/fitbit.csv
docker run --rm -it -v $DATA:/data altermarkive/csv-select /data/fitbit.csv /data/fitbit.selected.csv Weight.bmi Weight.date Weight.fat Weight.time Weight.weight
docker run --rm -it -v $DATA:/data altermarkive/csv-join /data/fitbit.selected.csv /data/fitbit.local.csv ' ' Weight.date Weight.time Local
docker run --rm -it -v $DATA:/data altermarkive/csv-timestamp-from-local /data/fitbit.local.csv /data/fitbit.stamped.csv Local Timestamp '%m/%d/%y %H:%M:%S'
docker run --rm -it -v $DATA:/data altermarkive/csv-rename /data/fitbit.stamped.csv /data/fitbit.renamed.csv Weight.bmi Weight.fat Weight.weight BMI Fat Weight
docker run --rm -it -v $DATA:/data altermarkive/csv-select /data/fitbit.renamed.csv /data/fitbit.ready.csv Timestamp BMI Fat Weight

docker run --rm -it -v $DATA:/data altermarkive/csv-concatenate /data/apple.ready.csv /data/fitbit.ready.csv /data/flat.csv
