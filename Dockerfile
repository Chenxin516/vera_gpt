FROM python:3.10.6-bullseye

WORKDIR /vera-gpt
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN pip3 install -e .
