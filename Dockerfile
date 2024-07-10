FROM python:3
# https://hub.docker.com/_/python

WORKDIR /opt/bot

COPY . .

RUN apt update \
    && apt install -y libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r src/requirements.txt

ENV PYTHONPATH=.
ENV MAJOR_VERSION=1
ENV MINOR_VERSION=1
ENV PATCH_VERSION=0
ENV LOCALE_DIR=locales

ENTRYPOINT [ "python3", "src/main.py" ]

# cp /opt/bot/.env.local.example /opt/bot/.env
