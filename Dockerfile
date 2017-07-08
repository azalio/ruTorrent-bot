FROM python:3
MAINTAINER Mikhail Petrov <azalio@azalio.net>

ENV REFRESHED_AT 2017-07-08-21:17

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./main.py" ]
