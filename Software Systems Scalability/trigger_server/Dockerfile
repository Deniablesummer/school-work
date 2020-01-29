#Use this as base image for now (smallest in size). See docker hub docs for more info
#https://hub.docker.com/_/python
FROM python:3.7.2-alpine3.9
WORKDIR /usr/local/bin
COPY trigger_server.py .
CMD python ./trigger_server.py
