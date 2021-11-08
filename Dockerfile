FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY . .

RUN pip install --upgrade --no-cache-dir pip
RUN pip install --no-cache-dir -r requirements.txt
