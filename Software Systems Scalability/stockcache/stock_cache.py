"""
" stock_cache
"
" Used for testing of the transactions server
" Usage: 'stock_cache.py '
"""

import socket
import sys
import hashlib
import time
import random
from threading import Thread
import struct

'''
'pull,VEHpush,VEH,39765,1553918828557pull,MKXpush,MKX,121,1553918828569pull,URApull,DJHpush,URA,307,1553918828582push,DJH,27132,1553918828594push,KTQ,101,1553918828596pull,RVR'
'''

def on_new_client(client_socket, address, stock_cache):
    with client_socket:
        while True:
            data = client_socket.recv(1024)
            message = ''
            if not data: break
            print('Rcvd', repr(data), 'From', address)
            data = data.decode()
            stocks = []
            if data[:4] == 'pull':
                p_data = data.split('pull')[1:]
                for i in p_data:
                    stocks.append(i[1:4])
                try:
                    for j in stocks:
                        quote, expiry = stock_cache[j]
                        message += j + ',' + quote + ',' + expiry + ','
                except KeyError as error:
                    pass
                if message == '':
                    message = 'None'
                print('SENT: ' + message)
                message = message.encode()
                client_socket.sendall(message)

                p_data = data.split('push')[1:]
                if len(p_data) == 0:
                    pass
                else:
                    for j in p_data:
                        entry = j.split(',')
                        stock_symbol = entry[1]
                        quote = entry[2]
                        expiry = entry[3][:13]
                        stock_cache[stock_symbol] = (quote, expiry)
            elif data[:4] == 'push':
                p_data = data.split('push')[1:]
                for j in p_data:
                    entry = j.split(',')
                    stock_symbol = entry[1]
                    quote = entry[2]
                    expiry = entry[3][:13]
                    stock_cache[stock_symbol] = (quote, expiry)

                p_data = data.split('pull')[1:]
                if len(p_data) == 0:
                    pass
                else:
                    for i in p_data:
                        stocks.append(i[1:4])
                    try:
                        for j in stocks:
                            quote, expiry = stock_cache[j]
                            message += j + ',' + quote + ',' + expiry + ','
                    except KeyError as error:
                        pass
                    if message == '':
                        message = 'None'
                    print('SENT: ' + message)
                    message = message.encode()
                    client_socket.sendall(message)





def main():
    stock_cache = dict()
    # set port to free port
    if len(sys.argv) == 1:
        port = 8075
    else:
        port = int(sys.argv[1])
    # init server
    # init server
    print("Initializing server...")
    server_socket = None
    msg = ""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception as msg:
        print(msg)
        server_socket = None

    hostName = socket.gethostname()
    print(hostName)
    # user specified port?
    hostIP = socket.gethostbyname(socket.gethostname())
    try:
        server_socket.bind(('', port))
    except Exception as msg:
        server_socket.close()
        print(msg)
        server_socket = None

    # TODO: Graceful exit

    if server_socket is None:
        print("Could not open socket")
        exit(-1)

    print("Host: " + hostName + " is running on: " + hostIP + ":" + str(port))
    print("Ctr-Break to force close")
    # wait for, and handle connections
    server_socket.listen(5)
    while True:
        try:
            client_socket, address = server_socket.accept()
            print("Connection from", address)
            # with client_socket:
            client_thread = Thread(target=on_new_client, args=(client_socket, address, stock_cache))
            client_thread.start()
        except Exception as e:
            # something went wrong
            print(e)

    server_socket.close()
    print("Server closed")


if __name__ == "__main__":
    main()
