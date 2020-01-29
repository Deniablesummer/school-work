import socket
import threading
import websockets
import asyncio


# used for sending returned data from the receiver server (transaction server connection) to original client
returned_data = []

# Connect to haproxy server
haproxyPort = 8090
haproxySocket = None

recvAddress = None


# Server loop, receives data from client connections, and sends it to haproxy server load balancer.
'''
def client_connection(haproxySocket, client_server_socket):

    global returned_data

    server_address = client_server_socket.getsockname()
  
    while True:
        print('[client_connection]: waiting for a connection on '+server_address[0]+':'+str(server_address[1]) +' (transaction server -> webserver connection)')
        connection, client_address = client_server_socket.accept()
	
        try:
            print("[client_connection]: connection received")
            while True:
                
                data = connection.recv(1024)
                if data:
                    print("[client_connection]:" + data.decode())
                    returnMsg = "[client_connection]: client server received from you: " + data.decode()
                    connection.sendall(returnMsg.encode('utf-8'))
                    
                    data_string = data.decode()
                    data_string = data_string.rstrip()
                    print(data_string)
                 
                    # send to haproxy commands
                    haproxySocket.sendall(data_string.encode('utf-8') + '\n'.encode())
                    
                    while True: 
                        if returned_data:
                            connection.sendall(returned_data)
                            returned_data = None
                            break

                else:
                    print("[client_connection]: no more data from client")
                    break
        finally:
            print("client closed")
            connection.close() 	  
'''

async def client_connection(websocket, path):

    global returned_data
    global haproxySocket


    while True:

        print("[client_connection]: awaiting data")

        try:
            data = await websocket.recv()
            print("[client_connection]: data arrived")
        except:
            print("client connection closed")
            break

        response = data.rstrip()
        print("sending data: ",response)

        #await websocket.send("got it, thanks")

        haproxySocket.sendall(response.encode('utf-8') + '\n'.encode())
        somethingHappened = False

        while True:
            if len(returned_data) > 0:
                somethingHappened = True
                print("returning ", returned_data)
                await websocket.send(returned_data[0].decode())
                del returned_data[0]
            elif len(returned_data) == 0 and somethingHappened == True:
                break
    return



def ping_haproxy():
    global haproxySocket

    if(haproxySocket):
        haproxySocket.sendall("[1] PING\n".encode())

def receiver(recv_server_socket):

    global returned_data
    global haproxySocket
    global recvAddress
    

    while True:

        server_address = recv_server_socket.getsockname()
        recvAddress = server_address[0] + ":" + str(server_address[1])

        #connect to haproxy
        haproxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        haproxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        haproxySocket.connect(('haproxy', haproxyPort)) 
        haproxySocket.sendall(recvAddress.encode() + "\n".encode())

        print('[receiver]: waiting for a connection on '+recvAddress+' (transaction server -> webserver connection)')
        connection, client_address = recv_server_socket.accept()

        try:
            print("[receiver]: connection received, connected to ", client_address)
            while True:
             
                data = connection.recv(1000000)
                print("recieved data ", data)
                if data:
                    
                    if data.decode() != 'ping\n':
                        returned_data.append(data)
                    
                else:
                    print("[receiver]: no more data from client")
                    break
        finally:
            print("receiver closed connection")
            connection.close()
            haproxySocket.close()
            

def main():

    '''
    t = threading.Timer(10.0, ping_haproxy)
    t.start()
    '''

    # server config
    
    hostport = 9081 # host port (of the docker container) to map webserver to.
        
    hostIp = socket.gethostbyname(socket.gethostname())
    server_address = (hostIp, hostport) # specify the server address, set at localhost and PORT.
    
    '''
    client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_server_socket.bind(server_address)
    client_server_socket.listen(5)
    '''
    start_client_connection = websockets.serve(client_connection, server_address[0], hostport )
    print("[client_connection]: websocket server started, listening at: %s:%d" % (server_address[0],hostport))



    # server config
    #send recv server details to haproxy
    recvPort = 9082
    hostIP = socket.gethostbyname(socket.gethostname())
    server_address = (hostIP, recvPort) # specify the server address, set at localhost and PORT.
        
    recv_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_server_socket.bind(server_address)
    recv_server_socket.listen(5)


    receiving_thread = threading.Thread(target=receiver, args=(recv_server_socket,))
    receiving_thread.start()

    '''
    client_thread = threading.Thread(target=client_connection, args=(haproxySocket, client_server_socket,))
    client_thread.start()
    '''

    asyncio.get_event_loop().run_until_complete(start_client_connection)
    asyncio.get_event_loop().run_forever()


 


if __name__ == '__main__':
    main()
