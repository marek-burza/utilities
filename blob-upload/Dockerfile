FROM python:3.7

RUN pip3 install azure-storage-blob==12.3.0

ADD program.py /app/
WORKDIR /app

ENTRYPOINT ["python3", "/app/program.py"]
