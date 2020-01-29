#!/bin/bash

exec sudo COMPOSE_HTTP_TIMEOUT=200 docker-compose up --build client
