FROM debian:jessie

#
# Install python3
#
RUN apt-get update

RUN apt-get install -y --no-install-recommends \
    ca-certificates \
    libsqlite3-0 \
    libssl1.0.0 \
    python3 \
    python3-pip \
    python3-lxml \
    git \
    ssh

#
# Install HPS DataCite and it's dependencies
#

RUN pip3 install lxml connexion requests certifi

ADD . /hps-b2handle

WORKDIR /hps-b2handle/src

CMD ["python3", "app.py"]

