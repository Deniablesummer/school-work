#!/bin/bash

#sudo docker-compose up --build -d trigger-server
sudo docker-compose up --build --scale transaction-server=5 transaction-server
