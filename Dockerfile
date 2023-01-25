FROM python:3.11.0-slim-buster

COPY . /hollys
WORKDIR /hollys

# install nodejs
RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && apt-get install -y nodejs

# install bun
RUN apt install unzip && \
    curl -fsSL https://bun.sh/install | bash

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /hollys
RUN pip install pip --upgrade && \
    pip install -r requirements.txt && \
    pc init

CMD pc run --env prod
