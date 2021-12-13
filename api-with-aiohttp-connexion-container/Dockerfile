# Build environment
FROM python:3.8.6-alpine3.12 as Build

RUN apk add --no-cache build-base linux-headers
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt


# Target container image
FROM python:3.8.6-alpine3.12

COPY --from=Build /usr/local/bin/chardetect /usr/local/bin/chardetect
COPY --from=Build /usr/local/bin/connexion /usr/local/bin/connexion
COPY --from=Build /usr/local/bin/flask /usr/local/bin/flask
COPY --from=Build /usr/local/bin/jsonschema /usr/local/bin/jsonschema
COPY --from=Build /usr/local/bin/openapi-spec-validator /usr/local/bin/openapi-spec-validator
COPY --from=Build /usr/local/bin/openapi-spec-validator /usr/local/bin/openapi-spec-validator
COPY --from=Build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

COPY app /app
WORKDIR /app

ENTRYPOINT ["python3", "/app/app.py"]
