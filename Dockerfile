#python image
FROM python:3.9-slim-buster

# working directory
WORKDIR /pkrms

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
COPY . .