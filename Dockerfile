FROM ubuntu:jammy

#
# Install python3
#
RUN apt-get update

RUN apt-get install -y --no-install-recommends \
    ca-certificates \
    python3 \
    python3-pip \
    python3-lxml \
    git \
    ssh

#
# Install HPS DataCite and it's dependencies
#
ADD . /hps-b2handle

RUN pip3 install -r /hps-b2handle/requirements.txt

WORKDIR /hps-b2handle/src

VOLUME /hps-b2handle/certs/privkey.pem
VOLUME /hps-b2handle/certs/cert.pem

ENV HANDLE_PROXY_HOST=0.0.0.0
ENV HANDLE_PROXY_PORT=8080

ENTRYPOINT ["python3", "./app.py"]
