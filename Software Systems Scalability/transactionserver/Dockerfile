#This file builds our transaction server image

#Use this as base image for now (smallest in size). See docker hub docs for more info
#https://hub.docker.com/_/python
FROM python:3.7.2-alpine3.9
WORKDIR /usr/local/bin

#Add core.py into image
COPY core.py .
#Required to run core.py
COPY log_generator.py .
COPY xml_builder.py .
COPY connections.py .
COPY pending.py .
COPY stocks.py .
COPY user.py .
COPY mysql ./mysql

#Dependencies
#RUN pip3 install mysql-connector-python
#Run server
CMD python -u ./core.py
