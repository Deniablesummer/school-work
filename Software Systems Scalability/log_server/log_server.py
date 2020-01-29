#when a request is sent it pulls the data from all the servers

from threading import *
import socket
import time
import sys

count = 0
count_lock = Lock()
num = 0
thread_lock = Lock()
file_lock = Lock()


def on_new_client(client_socket, address, threads):

    global count
    global count_lock
    global file_lock
    ts = []

    with client_socket:
        print('In {}:{}'.format(address[0], address[1]))
        while True:
            data = client_socket.recv(1024)
            if not data:
                #threads = [thread for thread in threads if thread[2] != client_socket]
                break
            #print('Rcvd', repr(data), 'From', address)
            data = data.decode()
            if data[:7] == 'DUMPLOG':
                print('Number of threads:' + str(len(threads)))
                user = data.split(',')[1]
                #save the entire message so we know what type of dumplog it is
                message = 'TAKE_DUMP'
                print('SENT: ' + message)
                message = message.encode()
                for i in threads:
                    if i[2] == client_socket:
                        pass
                    else:
                        try:
                            i[2].sendall(message)
                            ts.append(i[0])
                        except OSError:
                            pass
                with thread_lock:
                    for i in range(len(threads)):
                        threads.pop()
                for i in ts:
                    try:
                        i.join()
                    except RuntimeError:
                        pass
                print('onto_the_next')
                combine_log_files(client_socket, user, threads)
                break

            else:
                with count_lock:
                    count += 1
                    filename = str(count)
                print("{}:{} opening file: {}".format(address[0], address[1], count))
                with open(filename, 'wt') as output:
                    output.write(data)
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        data = data.decode()
                        #print(data)
                        output.write(data)
                break

    print('out {}:{}'.format(address[0], address[1]))
    '''
    print('out')
    print(count)
    print(len(ts))
    if count == len(ts):
    '''


def combine_log_files(client_socket, user, threads):
    global count
    global count_lock
    file_count = count
    # eventually will want to send the file over the socket once everything is connected, but for now will
    # just write it to file on local machine
    # NOTE: we will need to come up with a protocol for transfering these files because they will likely
    # be longer than the 1024 bytes currently expected.
    print('dumplog')
    generateXML(client_socket, user, file_count)
    with count_lock:
        count = 0
    with open('complete_log', 'a') as log_file:
        for j in range(1, file_count + 1):
            with open(str(j), 'rt') as input:
                logs = input.read()
                log_file.write(logs)

def send_entry(i, client_socket):
    message = '\t<' + i[1] + '>\n'
    message += '\t\t<timestamp>' + str(i[2]) + '</timestamp>\n'
    message += '\t\t<server>' + i[3] + '</server>\n'
    message += '\t\t<transactionNum>' + str(i[4]) + '</transactionNum>\n'
    if i[5] != '\\N':
        message += '\t\t<command>' + str(i[5]) + '</command>\n'
    if i[7] != '\\N':
        message += '\t\t<action>' + str(i[7]) + '</action>\n'
    if i[8] != '\\N':
        message += '\t\t<username>' + str(i[8]) + '</username>\n'
    if i[9] != '\\N':
        message += '\t\t<stockSymbol>' + str(i[9]) + '</stockSymbol>\n'
    if i[6] != '\\N':
        try:
            message += '\t\t<price>' + '{:.2f}'.format(round((float(i[6]) / 100.0), 2)) + '</price>\n'
        except (TypeError, ValueError) as error:
            message += '\t\t<price>' + str(i[6]) + '</price>\n'
    if i[10] != '\\N':
        try:
            message += '\t\t<funds>' + '{:.2f}'.format(round((float(i[10]) / 100.0), 2)) + '</funds>\n'
        except (TypeError, ValueError) as error:
            message += '\t\t<funds>' + str(i[10]) + '</funds>\n'
    if i[11] != '\\N':
        message += '\t\t<quoteServerTime>' + str(i[11]) + '</quoteServerTime>\n'
    if i[12] != '\\N':
        message += '\t\t<cryptokey>' + str(i[12]) + '\n</cryptokey>\n'
    if i[13] != '\\N':
        message += '\t\t<filename>' + str(i[13]) + '</filename>\n'
    if i[14] != '\\N':
        message += '\t\t<errorMessage>' + str(i[14]) + '</errorMessage>\n'
    if i[15] != '\\N':
        message += '\t\t<debugMessage>' + str(i[15]) + '</debugMessage>\n'
    message += '\t</' + i[1] + '>\n'
    message = message.encode()
    client_socket.sendall(message)


def generateXML(client_socket, user, file_count):
    # eventually will want to send the file over the socket once everything is connected, but for now will
    # just write it to file on local machine
    # NOTE: we will need to come up with a protocol for transfering these files because they will likely
    # be longer than the 1024 bytes currently expected.
    all_entries = None
    print(file_count)
    message = '<?xml version="1.0"?>\n<log>\n\n'
    message = message.encode()
    client_socket.sendall(message)
    # comment out if you don't want to almagamate--------------------------------------------------------------------
    try:
        with open('complete_log', 'rt') as input:
            all_entries = input.read()
        all_entries = all_entries.split('\t')
        if user == 'None':
            for k in all_entries[:-1]:
                try:
                    i = k.split(',')
                    send_entry(i, client_socket)
                except IndexError:
                    print(all_entries.index(k))
        else:
            for k in all_entries[:-1]:
                i = k.split(',')
                if i[8] != user:
                    pass
                else:
                    send_entry(i, client_socket)
    except FileNotFoundError:
        pass
    #----------------------------------------------------------------------------------------------------------------


    for j in range(1, file_count + 1):
        print('file: ' + str(j))
        with open(str(j), 'rt') as input:
            all_entries = input.read()
        all_entries = all_entries.split('\t')
        if user == 'None':
            for k in all_entries[:-1]:
                try:
                    i = k.split(',')
                    send_entry(i, client_socket)
                except IndexError:
                    print(all_entries.index(k))
        else:
            for k in all_entries[:-1]:
                i = k.split(',')
                if i[8] != user:
                    pass
                else:
                    send_entry(i, client_socket)

    message = '\n</log>\n'
    message = message.encode()
    client_socket.sendall(message)
    message = 'ENDOFDUMPLOG'
    message = message.encode()
    client_socket.sendall(message)


def main():

    num = 0
    threads = []

    # set port to free port
    if len(sys.argv) == 1:
        port = 8030
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
            num += 1
            # with client_socket:
            client_thread = Thread(target=on_new_client, args=(client_socket, address, threads))
            with thread_lock:
                threads.append([client_thread, False, client_socket])
            client_thread.start()
        except Exception as e:
            # something went wrong
            print(e)

    server_socket.close()
    print("Server closed")

if __name__ == '__main__':
    main()

