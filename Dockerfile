FROM python:3.11-slim

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY .env .
COPY scriptdb .
COPY insertNation.py .
EXPOSE 8127