The apache web server should run on port 8081 on the host ip (192.168.1.X) if you go to that address the web client will be served. It runs on port 80 of the apache docker container

The webserver.py is the bridge between the clients and the load balancer -> transaction servers. Its port is 8085
