# syntax=docker/dockerfile:1
FROM python:3.11-rc-alpine
COPY ./src /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install typer
RUN pip install rich
RUN pip install pysqlite3
CMD ["/bin/sh"]