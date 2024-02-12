FROM python:3.11-alpine

COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt && rm requirements.txt

WORKDIR /backend
COPY . /backend
