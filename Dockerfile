#python image
FROM python:3.9-slim-buster

# working directory
WORKDIR /pkrms

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY . .