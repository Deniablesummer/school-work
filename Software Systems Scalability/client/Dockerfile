#This file builds our transaction server image

#Use this as base image for now (smallest in size). See docker hub docs for more info
#https://hub.docker.com/_/python
FROM python:3.7.2-alpine3.9
WORKDIR /usr/local/bin

#Add testClient.py into image
COPY testClient.py .

#Required to run testClient.py
#Edit here to change workload file
COPY 10_user_workload.txt .

#EXPOSE 9080-10580

#Run server
CMD python -u testClient.py
