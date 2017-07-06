# docker build -t develop .
# docker run --name develop --rm -it -v $PWD:/project -p 8081:8081 develop

FROM ubuntu:16.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y apt-utils

RUN apt-get install -y build-essential git curl

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -

RUN apt-get install -y nodejs

RUN npm install -g bower
RUN npm install -g polymer-cli

WORKDIR /project

CMD ["/bin/bash"]
