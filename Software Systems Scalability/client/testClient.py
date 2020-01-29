#client for testing core.py
import socket
import time
import threading

PORT = 9080
BIND_LOCK = threading.Lock()
PRINT_LOCK = threading.Lock()

def create_server_socket():
    global BIND_LOCK
    # init server
    # print("Initializing server...")
    server_socket = None
    global PORT
    port = PORT  # default port
    PORT += 1
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception as msg:
        # print(msg)
        server_socket = None

    hostName = socket.gethostname()
    # print(hostName)
    hostIP = socket.gethostbyname(hostName)

    with BIND_LOCK:
        try:
            server_socket.bind((hostIP, port))
        except Exception as msg:
            server_socket.close()
            # print(msg)
            server_socket = None

    # TODO: Graceful exit
    if server_socket is None:
        # print("Could not open socket")
        exit(-1)
    # print("Host: " + hostName + " is running on: " + hostIP + ":" + str(port))
    # print("Press Ctrl-Break to force close...")
    # wait for, and handle connections
    return (server_socket, port)

def receive_responses(receiving_socket, dumplog, filename):
    receiving_socket.listen(5)
    try:
        server_socket, address = receiving_socket.accept()
        #server_socket.settimeout(10) # may want to change this
        # print("Connection from", address)
    except Exception as e:
        pass
        # something went wrong
        # print(e)
    if dumplog == True:
        output = open(filename, 'wt')

    while True:
        #print('receive_response_loop')
        data = server_socket.recv(1024)
        if not data: break
        if dumplog == True:
            data = data.decode()
            if data[-12:] == 'ENDOFDUMPLOG':
                output.write(data[:-12])
                break
            else:
                output.write(data)
        else:
            pass
    if dumplog == True:
        output.close()
        #data = data.decode()
        #print(data)
    server_socket.close()
    return

def new_client(commands, count):
    #print('thread ' + str(count) + 'in')
    threads = []
    dumplog = False
    filename = None
    command = commands[0]
    command = command.split(' ')
    if command[1] == 'DUMPLOG':
        dumplog = True
        if len(command) == 3:
            filename = command[2]
        elif len(command) == 4:
            filename = command[3]
        else:
            filename = 'None'

    # TODO: implement a thread for receiving
    #print("Initializing testing client...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8090  # user specified port?
    hostIP = socket.gethostbyname(socket.gethostname())
    # connect
    client_socket.connect(('haproxy', port))  # '192.168.99.101'
    recv_socket, port = create_server_socket()

    receiving_thread = threading.Thread(target=receive_responses, args=(recv_socket,dumplog,filename))
    threads.append(receiving_thread)
    receiving_thread.start()

    hostIP = socket.gethostbyname(socket.gethostname())
    hostIP = hostIP + ':' + str(port) +'\n'
    #hostIP = '192.168.1.212' + ':' + str(port) + '\n'
    client_socket.sendall(hostIP.encode())

    for i in commands:
        i = i + '\n'
        client_socket.sendall(i.encode())
        #print("SENT: {}".format(i))
        '''
        data = client_socket.recv(1024)
        print('RECV: {}'.format(data.decode()))
        '''
    client_socket.close()

    for i in threads:
        i.join()
    '''
    with PRINT_LOCK:
        print(str(count))
    '''

    return

def main():
    count = 0
    clients = {}
    threads = []
    filename = './10_user_workload.txt'  #'./final_workload_2019'
    commands_file = open(filename, 'rt')
    all_data = commands_file.read()
    all_data = all_data.split('\n')[:-1]
    final_command = all_data[-1]
    final_command = final_command.replace(',', ' ')
    
    for i in all_data[:-1]: # removes the dumplog command so it ensure it will execute after all others
        userid = i.split(',')[1]
        userid = userid.rstrip()
        i = i.replace(',', ' ')
        if userid in clients:
            commands = clients[userid]
            commands.append(i)
            clients[userid] = commands
        else:
            clients[userid] = [i]

    '''
    all_data = commands_file.readline()
    
    while all_data != '':
        print(all_data)
        all_data = commands_file.readline()
    
    while all_data != '':
        #print(all_data)
        try:
            all_data = all_data.decode()
            #print(all_data)
            all_data = all_data.rstrip()
            all_data = all_data.replace(',', ' ')
            temp = all_data.split(' ')
            command = temp[1]
            if command == 'DUMPLOG':
                clients['None'] = all_data
            else:
                userid = temp[2]
                userid = userid.rstrip()
                if userid in clients:
                    commands = clients[userid]
                    commands.append(all_data)
                    clients[userid] = commands
                else:
                    clients[userid] = [all_data]
            all_data = commands_file.readline()
            print(all_data)
        except UnicodeDecodeError as error:
            print('bad_line')
            all_data = commands_file.readline()
            print(all_data)
    '''
    if filename != './_user_workload.txt':
        print(len(clients))
        for i in clients:
            count += 1
            #time.sleep(0.1)
            client_thread = threading.Thread(target=new_client, args=(clients[i],count))
            threads.append(client_thread)
            client_thread.start()
        count = 1
        for i in threads:
            i.join()
            print('joined: ' + str(count))
            count += 1
        print(final_command)
        final_command = final_command.rstrip()
        clients['None'] = [final_command]
        new_client(clients['None'],count)

        for i in range(100):
            print('get_file_now')
        time.sleep(10000)
        
        '''
        print("Initializing testing client...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 8090  # user specified port?
        hostIP = socket.gethostbyname(socket.gethostname())

        # connect
        # send data
        output = open('testLOG', 'wt')
        client_socket.connect(('haproxy', port))
        client_socket.sendall(final_command.encode())
        print("SENT: {}".format(final_command))
        time.sleep(30.0)
        while True:
            data = client_socket.recv(1024)
            #print(data)
            if not data:
                break
            else:
                data = data.decode()
                output.write(data)

        client_socket.close()
    else:
        print("Initializing testing client...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 8090  # user specified port?
        hostIP = socket.gethostbyname(socket.gethostname())

        #connect
        # send data
        output = open('testLOG', 'wt')
        client_socket.connect(('haproxy', port))
        for i in range(len(all_data)):
            if i == (len(all_data) - 1):
                command = all_data[i]
                command = command.replace(',', ' ')
                client_socket.sendall(command.encode())
                print("SENT: {}".format(command))
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    else:
                        data = data.decode()
                        output.write(data)
                output.close()

                client_socket.close()
            else:
                command = all_data[i]
                command = command.replace(',', ' ')
                client_socket.sendall(command.encode())
                print("SENT: {}".format(command))
                data = client_socket.recv(1024)
                print('RECV: {}'.format(data.decode()))
        client_socket.close()
        '''

    '''
    client_socket.sendall(b'ADD USER 200')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    # send data
    client_socket.sendall(b'QUOTE USER2 AMD')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    
    # send data
    client_socket.sendall(b'BUY USER AMD 200')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    # send data
    client_socket.sendall(b'SELL USER2 AMD 200')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    
    # send data
    client_socket.sendall(b'CANCEL_BUY USER')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    # send data
    client_socket.sendall(b'CANCEL_SELL USER2')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    
    # send data
    client_socket.sendall(b'DISPLAY_SUMMARY USER2')
    print("SENT")
    data = client_socket.recv(1024)
    print('Received', repr(data))
    
    # send data
    client_socket.sendall(b'SET_BUY_AMOUNT USER AMD 200')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    # send data
    client_socket.sendall(b'SET_SELL_AMOUNT USER2 AMD 200')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    
    # send data
    client_socket.sendall(b'CANCEL_SET_BUY USER AMD 200')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    # send data
    client_socket.sendall(b'CANCEL_SET_SELL USER2 AMD 200')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    
    # send data
    client_socket.sendall(b'SET_BUY_TRIGGER USER AMD 200')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    # send data
    client_socket.sendall(b'SET_SELL_TRIGGER USER2 AMD 200')
    print("SENT")
    data = client_socket.recv(1024)	
    print('Received', repr(data))
    '''

if __name__ == "__main__":
    main()
