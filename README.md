# Converting Health Data Exports to CSV

To convert Apple Health data export to CSV run the following command:

    docker run --rm -it -v $PWD:/data altermarkive/apple-health-to-csv /data/export.zip /data/apple.csv