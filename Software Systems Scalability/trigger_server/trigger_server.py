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
from threading import *

BUY_TRIGGER_LOCK = Lock()
SELL_TRIGGER_LOCK = Lock()
TRIGGER_TIMER = 5*60
sync_constant = None
close = False
SYNC_LOCK = Lock()
flush = False
QUOTE_SERVER_PORT = 4441
PAUSE_LOCK = Lock()
DUMPLOG_DELAY = 10

stock_cache = 'stock-cache'
#stock_cache = '192.168.1.167'  # stock-cache

log_server = 'log-server'
#log_server = '192.168.1.167'  # log-server

#quote_server = 'mock-quote-server'
quote_server = 'quoteserve.seng.uvic.ca'

user_db = 'db_user'
#user_db = '192.168.1.167'  # db_user


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

def connect_to_quote_server(port):
    global quote_server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket
    while True:
        try:
            s.connect((quote_server, 4441))  # 'quoteserve.seng.uvic.ca'
            break
        except socket.gaierror as error:
            time.sleep(0.01)

    return s

def quote_server_request(userid, stock_symbol):
    # Send the user's query
    message = stock_symbol + ', ' + userid + '\n'
    message = message.encode()
    global QUOTE_SERVER_PORT
    global QUOTE_TIMEOUT
    # uncomment when dealing with real quote server
    '''
    QUOTE_SERVER_PORT += 1
    if QUOTE_SERVER_PORT > 4451:
        QUOTE_SERVER_PORT = 4441
    '''

    qs = connect_to_quote_server(QUOTE_SERVER_PORT)
    qs.settimeout(QUOTE_TIMEOUT)
    qs.send(message)
    while True:
        # print('quote_loop')
        try:
            data = qs.recv(1024)
            break;
        except socket.timeout:
            qs = connect_to_quote_server(QUOTE_SERVER_PORT)
            qs.settimeout(QUOTE_TIMEOUT)
            qs.send(message)

    data = data.decode()

    # data = quote, sym, userid, timestamp, cryptokey
    return data.split(',')

def pull_from_global_cache(stock_cache, stock_symbol):
    global cache_socket
    message = 'pull,'+ stock_symbol
    message = message.encode()
    cache_socket.sendall(message)
    cache_socket.settimeout(0.1)
    try:
        message = cache_socket.recv(1024)
        data = message.decode('utf-8')
    except socket.timeout:
        data = 'None'
        print('pull timeout')
    '''
    raw_msglen = recvall(cache_socket, 4)
    if not raw_msglen:
        # connection is broken no point wasting time waiting around
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # print(msglen)
    # Read the message data
    message = recvall(cache_socket, msglen)
    if not message:
        # connection is broken
        return None
    '''

    #message = message.decode()
    # print('cache data: ' + data)
    if data == 'None':
        return
    else:
        all = data.split(',')[:-1]
        for i in range(0,len(all),3):
            stock_symbol = all[i]
            quote = int(all[i+1])
            try:
                expiry = int(all[i+2][:13])
            except ValueError:
                pass
                #send_to_global_cache(stock_symbol, quote, expiry)
            stock_cache[stock_symbol] = (quote, expiry)
        return


def send_to_global_cache(stock_symbol, quote, expiry):
    global cache_socket
    message = 'push,' + stock_symbol + ',' + str(quote) + ',' + str(expiry)
    message = message.encode()
    cache_socket.sendall(message)
    return


def now():
    global sync_constant
    if sync_constant is None:
        with SYNC_LOCK:
            if sync_constant is None:
                qs = connect_to_quote_server(QUOTE_SERVER_PORT)
                qs.send('ABC,123\n'.encode())
                now = int(round(time.time() * 1000))
                data = qs.recv(1024)
                data = data.decode()
                timestamp = int(data.split(',')[3])
                sync_constant = timestamp - now
    return int(round(time.time() * 1000)) + sync_constant

def QUOTE(userid, stock_symbol, t_num, stock_cache, log_queue):

    # check to see if the stock_symbol is valid
    if not re.match('^([a-z]|[A-Z]){1,3}$', stock_symbol):
        log_generator.generate_log(('ERROR', 'QUOTE'), (now(), SERVER_NAME, t_num, userid, stock_symbol,
                                                            'Stock symbol does not exist.'), log_queue)
        log_generator.generate_log(('DEBUG', 'QUOTE'), (now(), SERVER_NAME, t_num, userid, stock_symbol,
                                                            'Symbol must be 0-3 characters from the english alphabet'),
                                   log_queue)
        # print('Error: Stock symbol "{}" does not exist. '.format(stock_symbol))
        return('Error: Stock symbol "{}" does not exist. '.format(stock_symbol))

    # before making a request to the quote server first check to see if the value exists in the stock_cache

    # ****someone with more threading experience should refine this lock****
    if stock_symbol in stock_cache:
        quote, expiry = stock_cache[stock_symbol]
        if expiry > now():
            # print('Stock {} QUOTED {:.2f} to userid: {}'.format(stock_symbol, round((quote/100.0), 2), userid))
            return ('Stock {} QUOTED {:.2f} to userid: {}'.format(stock_symbol, round((quote/100.0), 2), userid))

    with cache_lock:
        pull_from_global_cache(stock_cache, stock_symbol)

    if stock_symbol in stock_cache:
        quote, expiry = stock_cache[stock_symbol]
        if expiry > now():
            #print('Stock {} QUOTED {:.2f} to userid: {}'.format(stock_symbol, round((quote / 100.0), 2), userid))
            return ('Stock {} QUOTED {:.2f} to userid: {}'.format(stock_symbol, round((quote / 100.0), 2), userid))

    with cache_lock:
        quote, sym, userid_ret, quote_timestamp, cryptokey = quote_server_request(userid, stock_symbol)
    timestamp = now()
    quote = int(round(float(quote)*100))
    if userid_ret != 'NA':
        send_to_global_cache(stock_symbol, quote, (timestamp + 60000)) #comment out when only one server
        stock_cache[stock_symbol] = (quote, timestamp + 60000)

    log_generator.generate_log(('QUOTE',), (timestamp, 'QS', t_num, quote, stock_symbol, userid,
                                                quote_timestamp, cryptokey), log_queue)
    if userid_ret == 'NA':  # userid can't be 'NA'
        # invalid entry to server
        log_generator.generate_log(('ERROR', 'QUOTE'), (now(), 'QS', t_num, userid, stock_symbol,
                                                            'Invalid server request.'), log_queue)
        log_generator.generate_log(('DEBUG', 'QUOTE'), (now(), 'QS', t_num, userid, stock_symbol,
                                                            'Invalid server request.'), log_queue)

        # print('Error: Invalid server request - "{}, {}". '.format(userid, stock_symbol))
        return('Error: Invalid server request - "{}, {}". '.format(userid, stock_symbol))
    else:
        log_generator.generate_log(('SYSTEM', 'QUOTE'), (now(), SERVER_NAME, t_num, userid, stock_symbol),
                                   log_queue)
        # return this result to the user
        return ('Stock {} QUOTED {:.2f} to userid: {}'.format(stock_symbol, round((quote/100.0), 2), userid))

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

def t_remove(userid, buy_triggers, sell_triggers, users):
    global BUY_TRIGGER_LOCK
    to_remove = []
    for i in range(len(buy_triggers)):
        # userid, stock_symbol, t_num, trigger, cent_amount
        if userid == buy_triggers[i][0]:
            to_remove.append(i)
    to_remove.reverse()
    for i in to_remove:
        with BUY_TRIGGER_LOCK:
            buy_triggers.pop(i)
    to_remove = []
    for i in range(len(sell_triggers)):
        # userid, stock_symbol, t_num, trigger, cent_amount
        if userid == sell_triggers[i][0]:
            to_remove.append(i)
    to_remove.reverse()
    for i in to_remove:
        with SELL_TRIGGER_LOCK:
            sell_triggers.pop(i)
    try:
        users.remove(userid)
    except ValueError as error:
        pass
    return


def on_new_client(client_socket, address, buy_triggers, sell_triggers, users):

    global BUY_TRIGGER_LOCK
    global SELL_TRIGGER_LOCK

    with client_socket:
        while True:
            data = client_socket.recv(1024)
            message = ''
            if not data: break
            print('Rcvd', repr(data), 'From', address)
            data = data.decode()
            data = data.split(';')[:-1] # everything but the last item which is likely an empty string
            for i in data:
                req = i.split(',')
                if req[0] == 'pull':
                    user = req[1]
                    t_remove(user, buy_triggers, sell_triggers, users)
                    message = 'done'
                    message = message.encode('utf-8')
                    client_socket.sendall(message)
                elif req[0] == 'push':
                    # push,buy,userid,stock_symbol, t_num, trigger, cent_amount
                    which = req[1]
                    userid = req[2]
                    db_user = connect_to_database_user()
                    local_user_data = user.user(userid, db_user)
                    stock_symbol = req[3]
                    t_num = int(req[4])
                    trigger = int(req[5])
                    cent_amount = int(req[6])
                    if which == 'buy':
                        with BUY_TRIGGER_LOCK:
                            buy_triggers.append([local_user_data, stock_symbol, t_num, trigger, cent_amount])
                    elif which == 'sell':
                        with SELL_TRIGGER_LOCK:
                            sell_triggers.append([local_user_data, stock_symbol, t_num, trigger, cent_amount])
                    message = 'done'
                    message = message.encode('utf-8')
                    client_socket.sendall(message)
                else:
                    print('something unexpected happening')

def write_logs(log_queue):
    global flush
    global close
    line_num = 0

    with open('./transaction_logs.txt', 'wt') as output:
        while True:
            if close:
                close = False
                break
            if flush == True:
                output.flush()
                flush = False
            if line_num >= 1000 or len(log_queue) == 0:
                if line_num > 0:
                    output.flush()
                else:
                    time.sleep(5)
                line_num = 0
            else:
                entry = log_queue.pop(0)
                output.write('\\N')
                for i in range(1,16):  #len(entry)
                    if entry[i] == None:
                        output.write(',\\N')
                    else:
                        output.write(',' + str(entry[i]))

                output.write('\t')
                line_num += 1
        print('leaving_write_logs')
        print('Length of log queue: ' + str(len(log_queue)))
    return

def send_to_log_server(s):
    # want to ensure that the log_writer thread and function is not running while this is being run
    try:
        # log_file = open('log_file.xml', 'wt')
        with open('./transaction_logs.txt', 'rt') as output:
            while True:
                logs = output.readline()
                #print(logs)
                if logs == '':
                    #log_file.close()
                    break
                else:
                    #log_file.write(logs)
                    logs = logs.encode()
                    s.sendall(logs)
        '''
        with open('./transaction_logs.txt', 'rt') as output:
            logs = output.read()
            # print(logs)
            logs = logs.encode()
            s.sendall(logs)
        '''
    except FileNotFoundError as error:
        pass
        #print('Caught\n')
        print('error')
    erase = open('./transaction_logs.txt', 'wt')
    erase.write('')
    erase.close()
    print('done_sending')


def listen_for_dump(log_queue):
    global close
    global pause_sync
    global PAUSE_LOCK
    global DUMPLOG_DELAY

    while True:
        log_server = connect_to_log_server()
        #send any outstanding log_file entries to the server
        #print('shouldnt be here yet')
        send_to_log_server(log_server)
        log_server.close()
        log_thread = Thread(target=write_logs, args=(log_queue,))
        log_thread.start()
        log_server = connect_to_log_server()
        while True:
            data = log_server.recv(1024)
            if not data: break
            data = data.decode()
            if data == 'TAKE_DUMP':
                print('@ take dump')
                with PAUSE_LOCK:
                    pause_sync = True
                time.sleep(DUMPLOG_DELAY)
                close = True
                log_thread.join()
                #time.sleep(1)
                send_to_log_server(log_server)
                break
            else:
                pass
        log_server.close()

def check_triggers(log_queue, buy_triggers, sell_triggers, stock_cache):
    last_trigger_check = -1
    while True:
        if (now()-last_trigger_check) < TRIGGER_TIMER:
            last_trigger_check = now()
            to_remove = []
            for i in buy_triggers:
                local_user_data, stock_symbol, t_num, trigger, cent_amount = i
                userid = local_user_data.get_userid()
                QUOTE(userid, stock_symbol, t_num, stock_cache, log_queue)
                quote, expiry = stock_cache[stock_symbol]
                if quote <= trigger:
                    # proceed with buy, funds are already reserved

                    num_stocks = cent_amount // quote
                    cost = num_stocks * quote

                    diff = cent_amount - cost

                    accessible_money, reserved_money = local_user_data.get_money()
                    local_user_data.set_money(accessible_money + diff, reserved_money - cent_amount)

                    accessible_stocks = local_user_data.get_accessible_stocks(stock_symbol)
                    local_user_data.set_accessible_stocks(stock_symbol, accessible_stocks + num_stocks)

                    local_user_data.clear_buy_trigger(stock_symbol)
                    stock_symbols.append(stock_symbol)
                    costs.append(cost)

                    log_generator.generate_log(('SYSTEM', 'SET_BUY_TRIGGER'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, trigger), log_queue)
                    # Account Transaction Log Entry here
                    log_generator.generate_log(('ACCOUNT',), (now(), 'DB1', t_num, 'remove', userid, cost), log_queue)
                    to_remove.append(i)
                    local_user_data.sync_user()
            to_remove = []
            for i in to_remove:
                buy_triggers.remove(i)
            for i in sell_triggers:
                stock_symbol, t_num, trigger, cent_amount = i
                QUOTE(userid, stock_symbol, t_num, stock_cache, log_queue)
                quote, expiry = stock_cache[stock_symbol]
                if quote >= trigger:
                    # proceed with sell stocks are already reserved

                    previously_reserved = cent_amount // trigger
                    actual_num_stocks = cent_amount // quote

                    value = actual_num_stocks * quote

                    diff = previously_reserved - actual_num_stocks

                    accessible_money = local_user_data.get_accessible_money()

                    local_user_data.set_accessible_money(accessible_money + value)

                    accessible_stocks, reserved_stocks = local_user_data.get_num_stocks(stock_symbol)
                    local_user_data.set_num_stocks(stock_symbol, (accessible_stocks + diff),
                                                   (reserved_stocks - previously_reserved))

                    local_user_data.clear_sell_trigger(stock_symbol)

                    log_generator.generate_log(('SYSTEM', 'SET_SELL_TRIGGER'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, trigger), log_queue)
                    # Account Transaction Log Entry here
                    log_generator.generate_log(('ACCOUNT',), (now(), 'DB1', t_num, 'add', userid, value), log_queue)
                    to_remove.append(i)
                    local_user_data.sync_user()
            to_remove = []
            for i in to_remove:
                sell_triggers.remove(i)

            time.sleep(TRIGGER_TIMER)
        else:
            time.sleep(3)



def main():
    users = []
    buy_triggers = []
    sell_triggers = []
    log_queue = []
    stock_cache = {}

    # set port to free port
    if len(sys.argv) == 1:
        port = 7444
    else:
        port = int(sys.argv[1])
    # init server
    # init server
    print("Initializing server...")
    server_socket = None
    msg = ""

    trigger_thread = Thread(target=check_triggers, args=(log_queue, buy_triggers, sell_triggers, stock_cache))
    trigger_thread.start()

    dumplog_thread = Thread(target=listen_for_dump, args=(log_queue,))
    dumplog_thread.start()

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
            client_thread = Thread(target=on_new_client, args=(client_socket, address, buy_triggers, sell_triggers,
                                                               users))
            client_thread.start()
        except Exception as e:
            # something went wrong
            print(e)

    server_socket.close()
    print("Server closed")


if __name__ == "__main__":
    main()
