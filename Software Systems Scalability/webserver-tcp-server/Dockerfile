# This file builds our webserver tcp server

# Use this as base image for now (smallest in size). See docker hub docs for more info
# https://hub.docker.com/_/python
FROM python:3.7.2-alpine3.9
WORKDIR /usr/local/bin

# copy webserver.py onto the container.
COPY webserver.py .

# copy websockets python module onto the container
COPY websockets ./websockets

# start webserver.py
CMD python3 -u webserver.py

EXPOSE 9081 9082

