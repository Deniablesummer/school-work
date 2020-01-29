import mysql.connector
import socket
import time

#user_db = '192.168.1.167'  # db_user
#stock_cache = '192.168.1.167'  # stock-cache
#log_server = '192.168.1.167'  # log-server
#quote_server = 'mock-quote-server'

user_db = 'db_user'
stock_cache = 'stock-cache'
log_server = 'log-server'
quote_server = 'quoteserve.seng.uvic.ca'


def connect_to_database_user():
    global user_db

    db_user = mysql.connector.connect(
                        host=user_db,  # this will have to become a fixed and global location eventually
                        user='seng468',
                        passwd='seng468',
                        database='day_trading_inc',
                        #port=33060
                        #local_infile = 1
                     )
    return db_user


def connect_to_stock_cache():
    global stock_cache
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket
    s.connect((stock_cache, 8075))
    return s

def connect_to_log_server():
    global log_server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket
    s.connect((log_server, 8030))
    return s

def connect_to_quote_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket
    while True:
        try:
            s.connect((quote_server, 4441))  # 'quoteserve.seng.uvic.ca'
            break
        except socket.gaierror as error:
            time.sleep(0.01)

    return s

def bind_to_socket(port):
    # init server
    print("Initializing server...")
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception as msg:
        print(msg)
        server_socket = None

    # get port from args
    # if no port specified, default to 8080
    # if arg not int, default to 8080
    '''
    try:
        port = int(sys.argv[1])
    except:
        port = 8080
    '''
    hostName = socket.gethostname()
    print(hostName)
    hostIP = socket.gethostbyname(hostName)
    try:
        server_socket.bind((hostIP, port))
    except Exception as msg:
        server_socket.close()
        print(msg)
        server_socket = None

    # TODO: Graceful exit
    if server_socket is None:
        print("Could not open socket")
        exit(-1)
    print("Host: " + hostName + " is running on: " + hostIP + ":" + str(port))
    print("Press Ctrl-Break to force close...")
    # wait for, and handle connections
    return server_socket


def connect_to_client(address):
    data = address.split(':')
    address = data[0]
    port = int(data[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket
    #print(address)
    s.connect((address, port))
    return s

def connect_to_trigger():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket
    s.connect(('trigger-server', 7444))
    return s
