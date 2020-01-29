#!/bin/bash

sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)

sudo docker-compose up -d --build db_user
sudo docker-compose up --build stock-cache
