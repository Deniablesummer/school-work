"""
" mock quote server
"
" Used for testing of the transactions server 
" Usage: 'mockQuoteServer.py <port>'
"""

import socket
import sys
import hashlib
import time
import random
from threading import Thread

def on_new_client(client_socket, address):
	with client_socket:
		while True:
			data = client_socket.recv(1024)
			if not data: break
			print('Rcvd', repr(data), 'From', address)
			data = data.decode("UTF-8")
			request = data.split(',')
			print(request)
			stock = request[0]
			usr = request[1].strip('\n')
			crypto = "fgjdswkldsfasd9fasdfsd"

			timestamp = int(round(time.time() * 1000))
			quote = random.randrange(100) + 1

			print(quote, ",", stock, ",", usr, ",", timestamp, ",", crypto)
			response = (str(quote) + "," + stock + "," + usr + "," + str(timestamp) + "," + str(crypto))
			response = response.encode("UTF-8")
			client_socket.sendall(response)

def main():
	#set port to free port
	if len(sys.argv) == 1:
		port = 4441
	else:
		port = int(sys.argv[1])
	# init server
	 #init server
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
	#wait for, and handle connections
	server_socket.listen(5)
	while True:
		try:
			client_socket, address = server_socket.accept()
			print("Connection from", address)
			# with client_socket:
			client_thread = Thread(target=on_new_client, args=(client_socket, address))
			client_thread.start()
			print("Connection from", address)
		except Exception as e:
			# something went wrong
			print(e)

	server_socket.close()
	print("Server closed")
	
if __name__ == "__main__":
	main()
