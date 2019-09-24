#!/bin/sh

export MSYS_NO_PATHCONV=1
export DATA=$(cygpath -w $PWD)

docker run --rm --name apple -it -v $DATA:/data altermarkive/apple-health-to-csv /data/export.zip /data/apple.csv
docker run --rm --name apple -it -v $DATA:/data altermarkive/fitbit-to-csv /data/MyFitbitData.zip /data/fitbit.csv
