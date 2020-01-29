# core.py

import random
import socket # for socket connections
import sys
from threading import *
import time
import mysql.connector
import log_generator
import re
import user
import pending
import stocks
import connections
import struct
import os


# TODO: consider changing data types of numbers in database from ints to varchar()
# TODO: establish a protocol for server responses

#connection_pool_lock = Lock()
cache_lock = Lock()
SERVER_NAME = socket.gethostname()
QUOTE_SERVER_PORT = 4441
cache_socket = connections.connect_to_stock_cache()
trigger_socket = connections.connect_to_trigger()
flush = False
close = False
sync_constant = None
SYNC_LOCK = Lock()
pause_sync = False
PAUSE_LOCK = Lock()
QUOTE_TIMEOUT = 0.01
SYNC_DELAY = 5
DUMPLOG_DELAY = 10
TRIGGER_TIMER = 1000
TRIGGER_LOCK = Lock()


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            # broken connection
            return None
        data += packet
    return data


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
                qs = connections.connect_to_quote_server(QUOTE_SERVER_PORT)
                qs.send('ABC,123\n'.encode())
                now = int(round(time.time() * 1000))
                data = qs.recv(1024)
                data = data.decode()
                timestamp = int(data.split(',')[3])
                sync_constant = timestamp - now
    return int(round(time.time() * 1000)) + sync_constant


def quote_server_request(userid, stock_symbol):
    # Send the user's query
    message = stock_symbol + ', ' + userid + '\n'
    message = message.encode()
    global QUOTE_SERVER_PORT
    global QUOTE_TIMEOUT
    #uncomment when dealing with real quote server
    '''
    QUOTE_SERVER_PORT += 1
    if QUOTE_SERVER_PORT > 4451:
        QUOTE_SERVER_PORT = 4441
    '''
    
    qs = connections.connect_to_quote_server(QUOTE_SERVER_PORT)
    qs.settimeout(QUOTE_TIMEOUT)
    qs.send(message)
    while True:
        #print('quote_loop')
        try:
            data = qs.recv(1024)
            break;
        except socket.timeout:
            qs = connections.connect_to_quote_server(QUOTE_SERVER_PORT)
            qs.settimeout(QUOTE_TIMEOUT)
            qs.send(message)

    data = data.decode()

    # data = quote, sym, userid, timestamp, cryptokey
    return data.split(',')


def refresh_pending(cs, local_user_data, userid, stock_cache, log_queue):

    now_time = now()
    # PENDING BUYS -----------------------------------------------------------------------------------------------------
    # check when the value was last displayed to the user
    pending_buy = local_user_data.get_pending_buy()
    if pending_buy is not None:
        expire_time = pending_buy.get_expiry()
        if now_time > expire_time:
            stock_symbol, t_num, req_amount, _ = pending_buy.get_essentials()
            # we need to check if the value has changed and redisplay it for the user
            QUOTE(userid, stock_symbol, t_num, stock_cache, log_queue)
            quote, expiry = stock_cache[stock_symbol]

            num_stock = req_amount // quote

            pending_buy.refresh(expiry, num_stock, quote)
            log_generator.generate_log(('SYSTEM', 'BUY'),
                                       (now(), SERVER_NAME, t_num, userid, stock_symbol, req_amount), log_queue)

            #TODO: Display updated data to user using the cs socket provided
            # print('pending buy updated sucessfully')

    # PENDING SELLS ----------------------------------------------------------------------------------------------------
    # check when the value was last displayed to the user
    pending_sell = local_user_data.get_pending_sell()
    if pending_sell is not None:
        expire_time = pending_sell.get_expiry()
        if now_time > expire_time:
            stock_symbol, t_num, req_amount, previously_reserved = pending_sell.get_essentials()
            # we need to check if the value has changed and redisplay it for the user
            QUOTE(userid, stock_symbol, t_num, stock_cache, log_queue)
            quote, expiry = stock_cache[stock_symbol]

            # the amount of stock reserved will change with the price
            stock = local_user_data.get_stock_info(stock_symbol)
            accessible_stocks, reserved_stocks = stock.get_num_stocks() # should exist

            num_stock = req_amount // quote

            diff = num_stock - previously_reserved

            if diff > accessible_stocks:
                # we have a problem and we will have to eliminate this sell.
                # can't sell this stock for this price
                log_generator.generate_log(('ERROR', 'SELL'),
                                           (now_time, SERVER_NAME, t_num, userid, stock_symbol, req_amount,
                                            'Value of user stock no longer values high enough for sell amount.'),
                                           log_queue)
                log_generator.generate_log(('DEBUG', 'SELL'),
                                           (now_time, SERVER_NAME, t_num, userid, stock_symbol, req_amount,
                                            'Cancelling most recent sell command.'), log_queue)

                stock.set_num_stocks((accessible_stocks + previously_reserved), (reserved_stocks - previously_reserved))

                local_user_data.remove_pending_sell()  #removes the most recent sell command issued
                # print('cancelled most recent pending sell due to reduced value in user\'s stocks')

            else:
                stock.set_num_stocks((accessible_stocks - diff), (reserved_stocks + diff))

                pending_sell.refresh(expiry, num_stock, quote)


                log_generator.generate_log(('SYSTEM', 'SELL'),
                                          (now(), SERVER_NAME, t_num, userid, stock_symbol, req_amount),
                                           log_queue)

                # TODO: Display updated data to user using the cs socket provided
                # print('pending sell updated sucessfully')
    return


def ADD(local_user_data, userid, cent_amount, t_num, log_queue):
    # check if cent_amount is positive
    if cent_amount < 0:
        log_generator.generate_log(('ERROR', 'ADD'), (now(), SERVER_NAME, t_num, userid, cent_amount,
                                                          'Add amount must be greater than 0.'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'ADD'), (now(), SERVER_NAME, t_num, userid, cent_amount,
                                                          'Add amount must be greater than 0.'),
                                   log_queue)
        # print('Add amount must be greater than 0.  ')
        return('Add amount must be greater than 0.  ')

    previous_amount = local_user_data.get_accessible_money()
    local_user_data.set_accessible_money((cent_amount + previous_amount))

    # GENERATE LOG FILES ***********************************************************************************************

    # GENERATE ACCOUNT TRANSACTION LOG ENTRY HERE
    log_generator.generate_log(('ACCOUNT',), (now(), 'DB1', t_num, 'add', userid, cent_amount), log_queue)

    # GENERATE SYSTEM EVENT AS WELL??
    log_generator.generate_log(('SYSTEM', 'ADD'), (now(), SERVER_NAME, t_num, userid, cent_amount), log_queue)

    # ******************************************************************************************************************
    # print(('ADDED {:.2f} to userid: {}'.format(round((cent_amount/100.0), 2), userid)))
    return ('ADDED {:.2f} to userid: {}'.format(round((cent_amount/100.0), 2), userid))


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


def BUY(local_user_data, userid, stock_symbol, cent_amount, t_num, stock_cache, log_queue):
    timestamp = now()
    if cent_amount < 0:
        # can't buy this stock for this price
        log_generator.generate_log(('ERROR', 'BUY'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                                          'BUY amount must be greater than 0'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'BUY'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                                          'BUY amount must be greater than 0'),
                                   log_queue)
        # print('Error: BUY amount must be greater than 0')
        return('Error: BUY amount must be greater than 0')

    # check how much the stock is
    QUOTE(userid, stock_symbol, t_num, stock_cache, log_queue)
    quote, expiry = stock_cache[stock_symbol]

    # check if the quote is greater than the cent_amount
    # this also ensures that negative numbers can't be used
    if quote > cent_amount:
        # can't buy this stock for this price
        log_generator.generate_log(('ERROR', 'BUY'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'Stock price greater than buy amount.'), log_queue)
        log_generator.generate_log(('DEBUG', 'BUY'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'Stock price greater than buy amount.'), log_queue)
        # print('Error: Stock price greater than buy amount')
        return('Error: Stock price greater than buy amount')

    num_stocks = cent_amount // quote
    accessible_money, reserved_money = local_user_data.get_money()

    if accessible_money < cent_amount:
        # insufficient funds to continue transaction
        log_generator.generate_log(('ERROR', 'BUY'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'Insufficient funds for attempted buy.'), log_queue)
        log_generator.generate_log(('DEBUG', 'BUY'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'Add funds before attempting buy.'), log_queue)
        # print('Error: Insufficient funds for attempted buy.')
        return('Error: Insufficient funds for attempted buy.')

    local_user_data.set_money((accessible_money - cent_amount), (reserved_money + cent_amount))
    local_user_data.add_pending_buy(stock_symbol, num_stocks, expiry, quote, cent_amount, t_num)

    log_generator.generate_log(('SYSTEM', 'BUY'),
                               (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                               log_queue)
    return ("BUY " + stock_symbol + " " + str(round((cent_amount/100.0), 2)) + " " + userid)


def COMMIT_BUY(local_user_data, userid, t_num, log_queue):

    # check if a pending buy exists
    pending_buy = local_user_data.get_pending_buy()
    if pending_buy is None:
        log_generator.generate_log(('ERROR', 'COMMIT_BUY'), (now(), SERVER_NAME, t_num, userid,
                                                                 'No pending buy commands to commit.'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'COMMIT_BUY'), (now(), SERVER_NAME, t_num, userid,
                                                                 'Issue a buy command first. '),
                                   log_queue)
        # print('Error: No pending buy commands to commit')
        return('Error: No pending buy commands to commit')

    stock_symbol, stock_price, num, expiry, req_amount, t_num2 = pending_buy.get_all()

    # There should be if it is all programmed correctly
    timestamp = now()

    # confirm that time stamp is still valid
    if expiry > timestamp:  # valid timestamp encountered

        accessible_money, reserved_money = local_user_data.get_money()
        buy_amount = stock_price * num
        diff = req_amount - buy_amount

        local_user_data.set_money((accessible_money + diff), (reserved_money - req_amount))

        # Account Transaction Log Entry here
        log_generator.generate_log(('ACCOUNT',), (timestamp, 'DB1', t_num, 'remove', userid, buy_amount),
                                   log_queue)

        local_user_data.remove_pending_buy()  # remove it from the pending buys list

        # check if the user already owns any of these stocks
        stock = local_user_data.get_stock_info(stock_symbol)

        if stock is not None:
            current_stock_num = stock.get_accessible_stocks()
            stock.set_accessible_stocks((num+current_stock_num))
        else:
            local_user_data.add_stock(stock_symbol, num)
        log_generator.generate_log(('SYSTEM', 'COMMIT_BUY'), (now(), SERVER_NAME, t_num, userid),
                                   log_queue)
        return('COMMIT_BUY completed successfully')

    # This is the case that the timestamp has indeed expired
    else:
        log_generator.generate_log(('ERROR', 'COMMIT_BUY'), (now(), SERVER_NAME, t_num, userid,
                                                                 'Pending buy had expired when commit was issued.'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'COMMIT_BUY'), (now(), SERVER_NAME, t_num, userid,
                                                                 'Update quote for stock before commiting buy.  '),
                                   log_queue)
        # Options: 1) don't let this happen and if it does abort <-------- I like this options
        #          2) immediately request a quote let user know request a quote and send this to the user
        # print('Error quoted stock value was expired when commit_buy was issued')
        return('Error quoted stock value was expired when commit_buy was issued')


# currently does not check if buy command was issued within 60 seconds (I don't think it matter though)
def CANCEL_BUY(local_user_data, userid, t_num, log_queue):

    # check if a pending buy exists
    pending_buy = local_user_data.get_pending_buy()
    if pending_buy is None:
        log_generator.generate_log(('ERROR', 'CANCEL_BUY'), (now(), SERVER_NAME, t_num, userid,
                                                          'No pending buy commands to cancel.'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'CANCEL_BUY'), (now(), SERVER_NAME, t_num, userid,
                                                                 'Must issue a BUY command prior to a CANCEL_BUY.  '),
                                   log_queue)
        # print('Error: No pending buy commands to cancel')
        return('Error: No pending buy commands to cancel')

    req_amount = pending_buy.get_req_amount()

    accessible_money, reserved_money = local_user_data.get_money()

    local_user_data.set_money((accessible_money + req_amount), (reserved_money - req_amount))

    local_user_data.remove_pending_buy()

    log_generator.generate_log(('SYSTEM', 'CANCEL_BUY'), (now(), SERVER_NAME, t_num, userid),
                               log_queue)

    return ('CANCEL_BUY ' + userid + 'completed successfully')


def SELL(local_user_data, userid, stock_symbol, cent_amount, t_num, stock_cache, log_queue):
    if cent_amount < 0:
        # can't sell this stock for this price
        log_generator.generate_log(('ERROR', 'SELL'), (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                                            'SELL amount must be greater than 0'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'SELL'), (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                                           'SELL amount must be greater than 0'),
                                   log_queue)
        # print('Error: SELL amount must be greater than 0')
        return('Error: SELL amount must be greater than 0')

    timestamp = now()

    # check if they own any of that stock

    stock = local_user_data.get_stock_info(stock_symbol)

    if stock is None:
        # ERROR LOG
        log_generator.generate_log(('ERROR', 'SELL'), (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                                           'No accessible stocks of this symbol to sell'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'SELL'), (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                                          'No accessible stocks of this symbol to sell'),
                                   log_queue)
        # print('Error: No accessible stocks to sell')
        return('Error: No accessible stocks to sell')

    accessible_stocks, reserved_stocks = stock.get_num_stocks()

    # check how much the stock is
    if accessible_stocks == 0:
        # ERROR LOG
        log_generator.generate_log(('ERROR', 'SELL'), (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                                           'No accessible stocks of this symbol to sell'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'SELL'), (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                                           'No accessible stocks of this symbol to sell'),
                                   log_queue)
        # print('Error: No accessible stocks to sell')
        return('Error: No accessible stocks to sell')

    QUOTE(userid, stock_symbol, t_num, stock_cache, log_queue)
    quote, expiry = stock_cache[stock_symbol]

    # check if the quote is greater than the cent_amount
    # this also ensures that negative numbers can't be used
    if quote > cent_amount:
        # can't sell this stock for this price
        log_generator.generate_log(('ERROR', 'SELL'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                           cent_amount, 'Stock price greater than sell amount.'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'SELL'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                           cent_amount, 'Sell amount must be greater than sell price.'),
                                   log_queue)
        # print('Error: Stock price greater than sell amount')
        return('Error: Stock price greater than sell amount')

    if accessible_stocks*quote < cent_amount:
        # can't sell this stock for this price
        log_generator.generate_log(('ERROR', 'SELL'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                           cent_amount, 'Value of user stock less than sell amount.'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'SELL'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                           cent_amount, 'Value of user stock less than sell amount.'),
                                   log_queue)
        # print('Error: Value of user stock less than sell amount')
        return('Error: Value of user stock less than sell amount')

    num_stocks = cent_amount // quote

    stock.set_num_stocks((accessible_stocks-num_stocks), (reserved_stocks+num_stocks))

    local_user_data.add_pending_sell(stock_symbol, num_stocks, expiry, quote, cent_amount, t_num)

    log_generator.generate_log(('SYSTEM', 'SELL'), (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                               log_queue)
    # print('sell command completed successfully')
    return("SELL " + str(round((cent_amount/100.0),2)) + " " + userid)


def COMMIT_SELL(local_user_data, userid, t_num, log_queue):
    # commit most recent sell tx
    # check if a pending sells has any entries
    pending_sell = local_user_data.get_pending_sell()
    if pending_sell is None:
        log_generator.generate_log(('ERROR', 'COMMIT_SELL'), (now(), SERVER_NAME, t_num, userid,
                                                                  'No pending sell commands to commit.'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'COMMIT_SELL'), (now(), SERVER_NAME, t_num, userid,
                                                                  'No pending sell commands to commit.'),
                                   log_queue)
        # print('Error: No pending sell commands to commit')
        return('Error: No pending sell commands to commit')

    stock_symbol, stock_price, num, expiry = pending_sell.get_commit_sell()

    timestamp = now()

    # confirm that time stamp is still valid
    if expiry > timestamp:  # valid timestamp encountered
        sell_amount = stock_price*num

        accessible_money = local_user_data.get_accessible_money()

        stock = local_user_data.get_stock_info(stock_symbol)
        current_stock_num = stock.get_num_reserved_stocks()

        stock.set_num_reserved_stocks((current_stock_num - num))

        local_user_data.remove_pending_sell()

        local_user_data.set_accessible_money((accessible_money + sell_amount))

        # Account Transaction Log Entry here
        log_generator.generate_log(('ACCOUNT',), (timestamp, 'DB1', t_num, 'add', userid, sell_amount),
                                   log_queue)

        log_generator.generate_log(('SYSTEM', 'COMMIT_SELL'), (now(), SERVER_NAME, t_num, userid),
                                   log_queue)
        return('Successful sell')

    # This is the case that the timestamp has indeed expired
    else:
        log_generator.generate_log(('ERROR', 'COMMIT_SELL'), (now(), SERVER_NAME, t_num, userid,
                                                                 'Pending sell had expired when commit was issued.'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'COMMIT_SELL'), (now(), SERVER_NAME, t_num, userid,
                                                                 'Update quote for stock before commiting sell.  '),
                                   log_queue)
        # Options: 1) don't let this happen and if it does abort <-------- I like this options
        #          2) immediately request a quote let user know request a quote and send this to the user
        # print('Error quoted stock value was expired when commit_buy was issued')
        return('Error quoted stock value was expired when commit_buy was issued')


# currently does not check whether sell command was issued within 60 seconds
def CANCEL_SELL(local_user_data, userid, t_num, log_queue):
    # cancel sell tx
    # check if a there are any pending sells
    pending_sell = local_user_data.get_pending_sell()
    if pending_sell is None:
        log_generator.generate_log(('ERROR', 'CANCEL_SELL'), (now(), SERVER_NAME, t_num, userid,
                                                          'No pending sell commands to cancel.'),
                                   log_queue)
        log_generator.generate_log(('DEBUG', 'CANCEL_SELL'), (now(), SERVER_NAME, t_num, userid,
                                                                 'No pending sell commands to cancel.'),
                                   log_queue)
        # print('Error: No pending sell commands to cancel')
        return('Error: No pending sell commands to cancel')

    stock_symbol, num = pending_sell.get_symbol_and_num()

    local_user_data.remove_pending_sell()

    stock = local_user_data.get_stock_info(stock_symbol)
    accessible_stocks, reserved_stocks = stock.get_num_stocks()

    stock.set_num_stocks((accessible_stocks + num), (reserved_stocks - num))

    log_generator.generate_log(('SYSTEM', 'CANCEL_SELL'), (now(), SERVER_NAME, t_num, userid),
                               log_queue)
    return ("CANCEL_SELL " + userid)


# sets buy amount to what was previously there plus the amount specified
# deducts the specified amount from the user account
def SET_BUY_AMOUNT(local_user_data, userid, stock_symbol, cent_amount, t_num, log_queue):
    timestamp = now()
    if cent_amount <= 0:
        # can't buy this stock for this price
        log_generator.generate_log(('ERROR', 'SET_BUY_AMOUNT'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET BUY amount must be greater than 0'), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_BUY_AMOUNT'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET BUY amount must be greater than 0'), log_queue)
        # print('Error: SET BUY amount must be greater than 0')
        return('Error: SET BUY amount must be greater than 0')

    accessible_money, reserved_money = local_user_data.get_money()

    if accessible_money < cent_amount:
        # insufficient funds to continue transaction
        log_generator.generate_log(('ERROR', 'SET_BUY_AMOUNT'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'Insufficient funds for attempted set buy amount.'), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_BUY_AMOUNT'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'Add funds or cancel pending buys before attempting to set this buy amount.  '),
                                   log_queue)

        # print('Error: Insufficient funds for attempted set buy amount.')
        return('Error: Insufficient funds for attempted set buy amount.')

    # check if user has prior buy trigger already set

    stock = local_user_data.get_stock_info(stock_symbol)

    if stock is not None:
        # don't care about buy trigger yet
        prev_buy_trigger, prev_buy_amount = stock.get_buy_trigger_and_amount()

        if prev_buy_amount is not None:
            # we have a previous buy trigger
            new_buy_amount = cent_amount + prev_buy_amount
        else:
            new_buy_amount = cent_amount

        stock.set_buy_amount(new_buy_amount)

    else:
        prev_buy_trigger = None
        # perform an insert for the entry in the table
        local_user_data.add_stock(stock_symbol, 0, 0, buy_amount=cent_amount)


    local_user_data.set_money((accessible_money - cent_amount), (reserved_money + cent_amount))

    if prev_buy_trigger is None:
        pass
        # print('TODO: Prompt user to set buy trigger for given stock.  ')
    else:
        pass
    log_generator.generate_log(('SYSTEM', 'SET_BUY_AMOUNT'), (now(), SERVER_NAME, t_num, userid, stock_symbol,
                                                                cent_amount), log_queue)
    return("SET_BUY_AMOUNT " + stock_symbol + " " + str(round((cent_amount/100.00),2)) + " " + userid)


# the buy amount and the trigger details are dealt with once the trigger point is hit
# if the user specifies more money than they need to it will all be held.
# Assuming for the time being that this replaces any other trigger
def SET_BUY_TRIGGER(local_user_data, userid, stock_symbol, cent_amount, t_num, stock_cache, log_queue, buy_triggers):
    # check that the trigger is greater than 0
    timestamp = now()
    if cent_amount <= 0:
        # can't buy this stock for this price
        log_generator.generate_log(('ERROR', 'SET_BUY_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET BUY TRIGGER must be greater than 0'), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_BUY_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET BUY TRIGGER must be greater than 0'), log_queue)
        # print('Error: SET BUY TRIGGER must be greater than 0')
        return ('Error: SET BUY TRIGGER must be greater than 0')

    stock = local_user_data.get_stock_info(stock_symbol)

    # check if previous set buy amount was issued
    if stock is None:
        log_generator.generate_log(('ERROR', 'SET_BUY_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'No previous SET BUY AMOUNT issued.  '), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_BUY_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET BUY AMOUNT must be issued before trigger.  '), log_queue)
        # print('Error: No previous SET_BUY_AMOUNT command issued. ')
        return('Error: No previous SET_BUY_AMOUNT command issued. ')
    else:
        buy_amount = stock.get_buy_amount()
        if buy_amount is None:
            log_generator.generate_log(('ERROR', 'SET_BUY_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'No previous SET BUY AMOUNT issued.  '), log_queue)
            log_generator.generate_log(('DEBUG', 'SET_BUY_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'SET BUY AMOUNT must be issued before trigger.  '), log_queue)
            # print('Error: No previous SET_BUY_AMOUNT command issued. ')
            return('Error: No previous SET_BUY_AMOUNT command issued. ')

        if buy_amount < cent_amount:
            # insufficient funds to continue transaction
            log_generator.generate_log(('ERROR', 'SET_BUY_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'SET_BUY_TRIGGER must be less than SET_BUY_AMOUNT.'),
                                       log_queue)
            log_generator.generate_log(('DEBUG', 'SET_BUY_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'SET BUY TRIGGER must be less than SET_BUY_AMOUNT. '),
                                       log_queue)
            # print('Error: SET_BUY_TRIGGER must be less than SET_BUY_AMOUNT.')
            return ('Error: SET_BUY_TRIGGER must be less than SET_BUY_AMOUNT.')

    stock.set_buy_trigger_and_bt_tnum(cent_amount, t_num)

    log_generator.generate_log(('SYSTEM', 'SET_BUY_TRIGGER'), (now(), SERVER_NAME, t_num, userid, stock_symbol,
                                                                 cent_amount), log_queue)

    # TODO: figure out how to implement check triggers
    for i in range(len(buy_triggers)):
        if stock_symbol == buy_triggers[i][0]:
            # entry exists
            buy_triggers[i] = [stock_symbol, t_num, cent_amount, buy_amount]
            break
    buy_triggers.append([stock_symbol, t_num, cent_amount, buy_amount]) #stock_symbol, t_num, trigger, cent_amount

    return("SET_BUY_TRIGGER " + stock_symbol + " " + str(round((cent_amount/100.0),2)) + " " + userid)


def CANCEL_SET_BUY(local_user_data, userid, stock_symbol, t_num, log_queue, buy_triggers):
    timestamp = now()

    stock = local_user_data.get_stock_info(stock_symbol)

    for i in buy_triggers:
        if i[0] == stock_symbol:
            buy_triggers.remove(i)
            break

    if stock is None:
        log_generator.generate_log(('ERROR', 'CANCEL_SET_BUY'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                    'No previous SET_BUY_AMOUNT to cancel.  '), log_queue)
        log_generator.generate_log(('DEBUG', 'CANCEL_SET_BUY'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                    'No previous SET_BUY_AMOUNT to cancel.  '), log_queue)
        # print('Error: No previous SET_BUY_AMOUNT to cancel.  ')
        return('Error: No previous SET_BUY_AMOUNT to cancel.  ')
    else:
        buy_amount = stock.get_buy_amount()
        if buy_amount is None:
            log_generator.generate_log(('ERROR', 'CANCEL_SET_BUY'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                        'No previous SET_BUY_AMOUNT to cancel.  '), log_queue)
            log_generator.generate_log(('DEBUG', 'CANCEL_SET_BUY'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                        'No previous SET_BUY_AMOUNT to cancel.  '), log_queue)
            # print('Error: No previous SET_BUY_AMOUNT to cancel.  ')
            return ('Error: No previous SET_BUY_AMOUNT to cancel.  ')
        else:
            stock.clear_buy_trigger()
            for i in range(len(buy_triggers)):
                if stock_symbol == buy_triggers[i][1]:
                    buy_triggers = buy_triggers[:i]+buy_triggers[(i+1):]
                    break

            # free up funds
            accessible_money, reserved_money = local_user_data.get_money()
            local_user_data.set_money((accessible_money + buy_amount), (reserved_money - buy_amount))

            log_generator.generate_log(('SYSTEM', 'CANCEL_SET_BUY'),
                                       (now(), SERVER_NAME, t_num, userid, stock_symbol),
                                       log_queue)
    return("CANCEL_SET_BUY " + stock_symbol + " " + str(round((buy_amount/100.0),2)) + " " + userid)


def SET_SELL_AMOUNT(local_user_data, userid, stock_symbol, cent_amount, t_num, log_queue):

    timestamp = now()

    if cent_amount <= 0:
        # can't sell this stock for this price
        log_generator.generate_log(('ERROR', 'SET_SELL_AMOUNT'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET SELL amount must be greater than 0'), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_SELL_AMOUNT'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET SELL amount must be greater than 0'), log_queue)
        # print('Error: SET SELL amount must be greater than 0')
        return('Error: SET SELL amount must be greater than 0')

    # check if they own any of that stock
    stock = local_user_data.get_stock_info(stock_symbol)

    if stock is None:
        # ERROR LOG
        log_generator.generate_log(('ERROR', 'SET_SELL_AMOUNT'),
                                   (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'No accessible stocks of this symbol to sell. '), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_SELL_AMOUNT'),
                                   (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'No accessible stocks of this symbol to sell. '), log_queue)
        # print('Error: No accessible stocks to sell.  ')
        return('Error: No accessible stocks to sell.  ')
    elif stock.get_accessible_stocks() == 0:
        # ERROR LOG
        log_generator.generate_log(('ERROR', 'SET_SELL_AMOUNT'),
                                   (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'No accessible stocks of this symbol to sell. '), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_SELL_AMOUNT'),
                                   (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'No accessible stocks of this symbol to sell. '), log_queue)
        # print('Error: No accessible stocks to sell.  ')
        return('Error: No accessible stocks to sell.  ')
    else:
        accessible_stocks, reserved_stocks, prev_sell_amount, sell_trigger = stock.get_sell_amount_data()

        if sell_trigger is not None:
            # previous stock has already been put aside only need to worry about cent_amount
            # we have to check if the user has enough stock to proceed with the transaction
            num_stocks = cent_amount // sell_trigger
            if num_stocks > accessible_stocks:
                # ERROR LOG
                log_generator.generate_log(('ERROR', 'SET_SELL_AMOUNT'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                            'Not enough accessible stocks of this symbol to set sell amount. '),
                                           log_queue)
                log_generator.generate_log(('DEBUG', 'SET_SELL_AMOUNT'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                            'Not enough accessible stocks of this symbol to set sell amount. '),
                                           log_queue)
                # print('Error: Not enough accessible stocks to set sell amount.  ')
                return ('Error: Not enough accessible stocks to set sell amount.  ')
            else:
                sell_amount = (num_stocks * sell_trigger) + prev_sell_amount

                stock.set_sell_amount_data((accessible_stocks - num_stocks), (reserved_stocks + num_stocks),
                                            sell_amount)
                log_generator.generate_log(('SYSTEM', 'SET_SELL_AMOUNT'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol,
                                            cent_amount), log_queue)
                return ("SET_SELL_AMOUNT " + stock_symbol + " " + str(round((cent_amount/100.00),2)) + " " + userid)

        else:
            # then we have no problem proceeding
            # check if previous sell_amount has been set
            if prev_sell_amount is not None:
                sell_amount = prev_sell_amount + cent_amount
            else:
                sell_amount = cent_amount

            stock.set_sell_amount(sell_amount)
            log_generator.generate_log(('SYSTEM', 'SET_SELL_AMOUNT'),
                                       (now(), SERVER_NAME, t_num, userid, stock_symbol,
                                        cent_amount), log_queue)
            # print('TODO: Prompt user to enter sell trigger')
            return ("SET_SELL_AMOUNT " + stock_symbol + " " + str(round((cent_amount / 100.00), 2)) + " " + userid)


def SET_SELL_TRIGGER(local_user_data, userid, stock_symbol, cent_amount, t_num, stock_cache, log_queue, sell_triggers):

    # check that the trigger is greater than 0
    timestamp = now()
    if cent_amount <= 0:
        # can't buy this stock for this price
        log_generator.generate_log(('ERROR', 'SET_SELL_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET SELL TRIGGER must be greater than 0'), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_SELL_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET SELL TRIGGER must be greater than 0'), log_queue)
        # print('Error: SET SELL TRIGGER must be greater than 0')
        return ('Error: SET SELL TRIGGER must be greater than 0')

    stock = local_user_data.get_stock_info(stock_symbol)

    if stock is None:
        log_generator.generate_log(('ERROR', 'SET_SELL_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'No previous SET SELL AMOUNT issued.  '), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_SELL_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'Set sell amount before issuing sell trigger. '), log_queue)
        # print('Error: No previous SET_SELL_AMOUNT command issued. ')
        return('Error: No previous SET_SELL_AMOUNT command issued. ')
    else:
        sell_trigger, sell_amount = stock.get_sell_trigger_and_amount()
        if sell_amount is None:
            log_generator.generate_log(('ERROR', 'SET_SELL_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'No previous SET SELL AMOUNT issued.  '), log_queue)
            log_generator.generate_log(('DEBUG', 'SET_SELL_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'Set sell amount before issuing sell trigger. '), log_queue)
            # print('Error: No previous SET_SELL_AMOUNT command issued. ')
            return('Error: No previous SET_SELL_AMOUNT command issued. ')

    if sell_amount < cent_amount:
        # sell amount set too low to continue transaction
        log_generator.generate_log(('ERROR', 'SET_SELL_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET_SELL_TRIGGER must be less than SET_SELL_AMOUNT.'), log_queue)
        log_generator.generate_log(('DEBUG', 'SET_SELL_TRIGGER'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                    'SET_SELL_TRIGGER must be less than SET_SELL_AMOUNT.'), log_queue)

        # print('Error: SET_SELL_TRIGGER must be less than SET_SELL_AMOUNT.')
        return ('Error: SET_SELL_TRIGGER must be less than SET_SELL_AMOUNT.')

    accessible_stocks, reserved_stocks = stock.get_num_stocks()

    # check stock amount
    if sell_trigger is None:
        # no previous trigger set
        # which means there should currently be no stock in reserve for this trigger
        if (cent_amount * accessible_stocks) > sell_amount:
            num_stocks = sell_amount // cent_amount
            sell_amount = num_stocks * cent_amount

            stock.set_sell_trigger_data((accessible_stocks-num_stocks), (reserved_stocks+num_stocks), cent_amount,
                                        sell_amount, t_num)
            log_generator.generate_log(('SYSTEM', 'SET_SELL_TRIGGER'),
                                       (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                       log_queue)

            for i in range(len(sell_triggers)):
                if stock_symbol == sell_triggers[i][0]:
                    # entry exists
                    sell_triggers[i] = [stock_symbol, t_num, cent_amount, sell_amount]
                    break
            sell_triggers.append(
                    [stock_symbol, t_num, cent_amount, sell_amount])  # stock_symbol, t_num, trigger, cent_amount

            # print('Potential change of set sell amount for user')
            # TODO: figure out how to implement triggers
            # check_triggers(db, userid, stock_symbol, t_num, stock_cache, cent_amount, sell_amount, 'sell')
            return("SET_SELL_TRIGGER " + stock_symbol + " " + str(round((cent_amount/100.0),2)) + " " + userid)
        else:
            log_generator.generate_log(('ERROR', 'SET_SELL_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'Not enough accessible stocks for this SET_SELL_TRIGGER '
                                        'with previous SET_SELL_AMOUNT.'), log_queue)
            log_generator.generate_log(('DEBUG', 'SET_SELL_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'Not enough accessible stocks for this SET_SELL_TRIGGER '
                                        'with previous SET_SELL_AMOUNT.'), log_queue)

            # print('Error: Not enough accessible stocks for this SET_SELL_TRIGGER with previous SET_SELL_AMOUNT.')
            return ('Error: Not enough accessible stocks for this SET_SELL_TRIGGER with previous SET_SELL_AMOUNT.')
    else:
        # has previously been set so we need pull the stock from the reserve and then reserve it again
        # need to unallocate and then reallocate the stock
        prev_reserved_stocks = sell_amount // sell_trigger

        if (cent_amount * (accessible_stocks+prev_reserved_stocks)) > sell_amount:
            num_stocks = sell_amount // cent_amount
            sell_amount = num_stocks * cent_amount
            diff = num_stocks - prev_reserved_stocks

            stock.set_sell_trigger_data((accessible_stocks - diff), (reserved_stocks + diff), cent_amount,
                                        sell_amount, t_num)
            log_generator.generate_log(('SYSTEM', 'SET_SELL_TRIGGER'),
                                       (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                       log_queue)
            # print('Potential change of set sell amount for user')
            # TODO: figure out how to implement triggers
            #check_triggers(db, userid, stock_symbol, t_num, stock_cache, cent_amount, sell_amount, 'sell')
            return ("SET_SELL_TRIGGER " + stock_symbol + " " + str(round((cent_amount / 100.0), 2)) + " " + userid)
            # we can proceed with the command
        else:
            log_generator.generate_log(('ERROR', 'SET_SELL_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'Not enough accessible stocks for this SET_SELL_TRIGGER '
                                        'with previous SET_SELL_AMOUNT.'), log_queue)
            log_generator.generate_log(('DEBUG', 'SET_SELL_TRIGGER'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol, cent_amount,
                                        'Not enough accessible stocks for this SET_SELL_TRIGGER '
                                        'with previous SET_SELL_AMOUNT.'), log_queue)

            # print('Error: Not enough accessible stocks for this SET_SELL_TRIGGER with previous SET_SELL_AMOUNT.')
            return ('Error: Not enough accessible stocks for this SET_SELL_TRIGGER with previous SET_SELL_AMOUNT.')


def CANCEL_SET_SELL(local_user_data, userid, stock_symbol, t_num, log_queue, sell_triggers):

    timestamp = now()

    stock = local_user_data.get_stock_info(stock_symbol)
    for i in sell_triggers:
        if i[0] == stock_symbol:
            sell_triggers.remove(i)
            break

    if stock is None:
        log_generator.generate_log(('ERROR', 'CANCEL_SET_SELL'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                    'No previous SET_SELL_AMOUNT to cancel.  '), log_queue)
        log_generator.generate_log(('DEBUG', 'CANCEL_SET_SELL'),
                                   (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                    'No previous SET_SELL_AMOUNT to cancel.  '), log_queue)
        # print('Error: No previous SET_SELL_AMOUNT to cancel.  ')
        return('Error: No previous SET_SELL_AMOUNT to cancel.  ')
    else:
        sell_trigger, sell_amount = stock.get_sell_trigger_and_amount()

        if sell_amount is None:
            log_generator.generate_log(('ERROR', 'CANCEL_SET_SELL'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                        'No previous SET_SELL_AMOUNT to cancel.  '), log_queue)
            log_generator.generate_log(('DEBUG', 'CANCEL_SET_SELL'),
                                       (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                        'No previous SET_SELL_AMOUNT to cancel.  '), log_queue)
            # print('Error: No previous SET_SELL_AMOUNT to cancel.  ')
            return ('Error: No previous SET_SELL_AMOUNT to cancel.  ')
        else:
            stock.clear_sell_trigger()

            if sell_trigger is None:
                # then there wasn't any stocks reserved yet and we're done
                log_generator.generate_log(('SYSTEM', 'CANCEL_SET_SELL'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol),
                                           log_queue)
                # print("CANCEL_SET_SELL " + stock_symbol + " " + str(round((sell_amount / 100.0), 2)) + " " + userid)
                return("CANCEL_SET_SELL " + stock_symbol + " " + str(round((sell_amount / 100.0), 2)) + " " + userid)
            else:
                # free up stocks
                prev_reserved_stocks = sell_amount // sell_trigger
                accessible_stocks, reserved_stocks = stock.get_num_stocks()
                stock.set_num_stocks((accessible_stocks + prev_reserved_stocks), (reserved_stocks -
                                                                                  prev_reserved_stocks))
                log_generator.generate_log(('SYSTEM', 'CANCEL_SET_SELL'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol),
                                           log_queue)
                # print("CANCEL_SET_SELL " + stock_symbol + " " + str(round((sell_amount / 100.0), 2)) + " " + userid)
                return("CANCEL_SET_SELL " + stock_symbol + " " + str(round((sell_amount/100.0),2)) + " " + userid)


def DUMPLOG(log_server, filename, userid, t_num, log_queue, client_socket):
    log_generator.generate_log(('SYSTEM', 'DUMPLOG'), (now(), SERVER_NAME, t_num, userid, filename),
                               log_queue)
    global flush
    flush = True
    if userid is None:
        userid = 'None'
    message = 'DUMPLOG,' + userid
    message = message.encode()
    log_server.sendall(message)
    while True:
        data = log_server.recv(1024)
        if not data: break
        client_socket.sendall(data)
    print('log_server_killed_connection')

    
    # xml_builder.generateXML(db_log, client_socket, filename, userid)

# TODO: Finish implementing
def DISPLAY_SUMMARY(local_user_data, userid, t_num, log_queue):
    userid, accessible_money, reserved_money, pending_buys, pending_sells, user_stocks = local_user_data.get_all()
    summary = 'Userid:\t{}\nAccessible Money:\t{}\nReserved Money:\t{}\n\n\tPending Buys:\n'.format(userid, accessible_money,
                                                                                 reserved_money)

    for i in pending_buys:
        stock_name, _, _, _, req_amount, _ = i.get_all()
        summary += '\t\tStock:\t{} - {}'.format(stock_name, req_amount)

    summary += 'n\n\tPending Sells:\n'

    for i in pending_sells:
        stock_name, _, _, _, req_amount, _ = i.get_all()
        summary += '\t\tStock:\t{} - {}'.format(stock_name, req_amount)

    summary += 'n\n\tUser Stocks:\n'

    for i in user_stocks:
        stock_name, accessible, reserved, buy_trigger, buy_amount, sell_trigger, sell_amount, _, _ = user_stocks[i].get_all()
        summary += '\t\tStock:\t{}\n\t\tAccessible:\t{}\n\t\tReserved:\t{}\n\t\tBuy Trigger:\t{}\n\t\t' \
                   'Buy Amount:\t{}\n\t\tSell Trigger:\t{}\n\t\tSell Amount:\t{}\n'\
            .format(stock_name, accessible, reserved, buy_trigger, buy_amount, sell_trigger, sell_amount)

    return(summary)


def get_commands(client_socket, commands, clientIP):
    with client_socket:
        prev = ''
        data = client_socket.recv(1024)
        data = data.decode()
        clientIP.append(data.split('\n')[0])
        print(clientIP[0])
        length = len(clientIP[0])
        prev = data[(length+1):]
        ## print('START' + prev + 'END')
        ## print(prev)
        while True:
            #print('get_commands_loop')
            data = client_socket.recv(1024)
            if not data: break
            data = data.decode()
            data = prev + data
            ## print('START' + data + 'END')
            data = data.split('\n')
            prev = data[-1]
            ## print('S_PREV' + prev + 'E_PREV')
            commands += data[:-1]
        last_commands = prev.split('/n')
        #last_commands = prev
        for i in last_commands:
            if i == '':
                pass
            else:
                commands.append(i)
    print('received all commands')
    return


def check_triggers(buy_triggers, sell_triggers, userid, local_user_data, stock_cache, log_queue):
    stock_symbols = []
    costs = []
    message = ''
    now_time = now()
    to_remove = []
    if buy_triggers != []:
        print(buy_triggers)
    if sell_triggers != []:
        print(sell_triggers)
    for i in buy_triggers:
        stock_symbol, t_num, trigger, cent_amount = i
        QUOTE(userid,stock_symbol,t_num,stock_cache,log_queue)
        quote, expiry = stock_cache[stock_symbol]
        if quote <= trigger:
            # proceed with buy, funds are already reserved

            num_stocks = cent_amount // quote
            cost = num_stocks * quote

            diff = cent_amount - cost

            accessible_money, reserved_money = local_user_data.get_money()
            local_user_data.set_money(accessible_money+diff, reserved_money-cent_amount)

            accessible_stocks = local_user_data.get_accessible_stocks(stock_symbol)
            local_user_data.set_accessible_stocks(stock_symbol, accessible_stocks+num_stocks)

            local_user_data.clear_buy_trigger(stock_symbol)
            stock_symbols.append(stock_symbol)
            costs.append(cost)

            log_generator.generate_log(('SYSTEM', 'SET_BUY_TRIGGER'),
                                       (now_time, SERVER_NAME, t_num, userid, stock_symbol, trigger), log_queue)
            # Account Transaction Log Entry here
            log_generator.generate_log(('ACCOUNT',), (now_time, 'DB1', t_num, 'remove', userid, cost), log_queue)

            message += "BUY TRIGGER ACTIVATED" + stock_symbol + " " + str(round((cost / 100.0), 2)) + " " + userid + "\n"
            to_remove.append(i)
            #count += 1

    for i in to_remove:
        buy_triggers.remove(i)
    to_remove = []

    for i in sell_triggers:
        stock_symbol, t_num, trigger, cent_amount = i
        #[['CCC', 1, 8000, 8000]]
        QUOTE(userid, stock_symbol, t_num, stock_cache, log_queue)
        quote, expiry = stock_cache[stock_symbol]
        if quote >= trigger:
            # proceed with sell stocks are already reserved

            previously_reserved = cent_amount // trigger
            actual_num_stocks =   cent_amount // quote
            print('amount: ' + str(cent_amount))
            print('quote: ' + str(quote))

            value = actual_num_stocks * quote

            diff = previously_reserved - actual_num_stocks

            accessible_money = local_user_data.get_accessible_money()

            local_user_data.set_accessible_money(accessible_money + value)

            print('valueee: ' + str(value))
            print('diff: ' + str(diff))

            accessible_stocks, reserved_stocks = local_user_data.get_num_stocks(stock_symbol)

            print('access stocks: ' + str(accessible_stocks))
            print('reserved stocks: ' + str(reserved_stocks))
            local_user_data.set_num_stocks(stock_symbol, (accessible_stocks + diff),
                                           (reserved_stocks - previously_reserved))

            local_user_data.clear_sell_trigger(stock_symbol)

            log_generator.generate_log(('SYSTEM', 'SET_SELL_TRIGGER'),
                                       (now_time, SERVER_NAME, t_num, userid, stock_symbol, trigger), log_queue)
            # Account Transaction Log Entry here
            log_generator.generate_log(('ACCOUNT',), (now_time, 'DB1', t_num, 'add', userid, value), log_queue)

            message += "SELL TRIGGER ACTIVATED" + stock_symbol + " " + str(round((value / 100.0), 2)) + " " + userid + "\n"
            to_remove.append(i)

    for i in to_remove:
        sell_triggers.remove(i)
    return ''


def listen_to_trigger_server(trigger_messages):
    global TRIGGER_LOCK
    global trigger_socket
    while True:
        if len(trigger_messages) == 0:
            time.sleep(1)
        else:
            message = trigger_messages[0]
            message = message.encode('utf-8')
            trigger_socket.sendall(message)
            response = trigger_socket.recv(1024)
            if response is None:
                trigger_socket = connections.connect_to_trigger()
            else:
                with TRIGGER_LOCK:
                    trigger_messages = trigger_messages[1:]

def fetch_triggers(userid, local_user_data, trigger_messages):

    while userid in trigger_messages:
        time.sleep(1)

    buy_triggers = []
    sell_triggers = []

    stocks = local_user_data.get_stocks()

    for i in stocks:
        stock_symbol, t_num, trigger, cent_amount = stocks[i].get_buy_trigger_info()
        s_stock_symbol, s_t_num, s_trigger, s_cent_amount = stocks[i].get_sell_trigger_info()
        if trigger is not None:
            buy_triggers.append([stock_symbol, t_num, trigger, cent_amount])
        if s_trigger is not None:
            sell_triggers.append([s_stock_symbol, s_t_num, s_trigger, s_cent_amount])

    return (buy_triggers, sell_triggers)


def on_new_client(recv_socket, client_address, stock_cache, connected_users, buy_triggers, sell_triggers, thread,
                  log_queue, userids, trigger_messages):

    first_time = True  # we should use this to grab all the information for that user
    local_user_data = None
    t_count = 0
    commands = []
    clientIP = []
    global flush
    global close
    global TRIGGER_TIMER

    # can't do this for too many connections
    # connect to databases and maintain these connection as long as feasible
    # db_user = connections.connect_to_database_user()
    # connect to trigger server
    #ts = connections.connect_to_trigger()
    #servers = [db_user, db_log, qs, client_socket]
    commands_thread = Thread(target=get_commands, args=(recv_socket, commands, clientIP))
    commands_thread.start()
    sleep_timer = 1
    while True:
        print('client_connection_loop')
        try:
            client_socket = connections.connect_to_client(clientIP[0])
            break
        except (IndexError, ConnectionRefusedError) as error:
            time.sleep(sleep_timer)
            sleep_timer = sleep_timer*2
            if sleep_timer > 16:
                sleep_timer = 1

    sleep_timer = 1
    with client_socket:
        while len(commands) == 0:
            #print('0_length_command_loop')
            time.sleep(0.1)
            sleep_timer = sleep_timer*2
            if sleep_timer > 4:
                sleep_timer = 0.1
        #print(len(commands))
        #print(commands[0]+' : '+str(thread))
        last_trigger_check = -1
        while commands_thread.isAlive() or (t_count < len(commands)):
            while True:
                if (first_time == False) and (local_user_data is not None) and ((now() - last_trigger_check) >= TRIGGER_TIMER):
                    last_trigger_check = now()
                    userid = local_user_data.get_userid()
                    message = check_triggers(buy_triggers, sell_triggers, userid, local_user_data, stock_cache,
                                             log_queue)
                    if message != '':
                        message = message.encode('utf-8')
                        client_socket.send(message)
                if commands_thread.isAlive() or (t_count < len(commands)):
                    try:
                        data = commands[t_count]
                        print(data)
                        break
                    except IndexError:
                        time.sleep(1)
                else:
                    break

            if not commands_thread.isAlive() and (t_count >= len(commands)):
                break
            # print(data)
            #if not data: break
            ## print('Received', repr(data), "From", client_address)
            #data = data.decode("UTF-8") # decode from byte to str

            # further process each line coming in to separate elements
            temp = data.split(' ')
            t_num = int(temp[0][1:-1])
            command = temp[1]
            arguments = temp[2:]

            if len(arguments) > 1:
                userid = arguments[0]
            else:
                userid = 'None'

            if first_time and command != 'DUMPLOG' and userid != 'None': # will want to refine this
                # Assumes first command is not a DUMPLOG <filename>
                # Also assumes that the command is valid
                sleep_timer = 1
                while True:
                    #print('db_connection_loop2')
                    try:
                        db_user = connections.connect_to_database_user()
                        local_user_data = user.user(userid, db_user)
                        message = 'pull,' + userid + ';'
                        with TRIGGER_LOCK:
                            trigger_messages.append(message)
                        buy_triggers, sell_triggers = fetch_triggers(userid, local_user_data, trigger_messages)
                        connected_users.append(local_user_data)
                        userids.append(local_user_data.get_userid())
                        db_user.close()
                        break
                    except mysql.connector.errors.DatabaseError as error:
                        time.sleep(sleep_timer)
                        sleep_timer = sleep_timer*2
                        if sleep_timer > 16:
                            sleep_timer = 1
                first_time = False
                if (first_time == False) and ((now() - last_trigger_check) >= TRIGGER_TIMER):
                    last_trigger_check = now()
                    userid = local_user_data.get_userid()
                    message = check_triggers(buy_triggers, sell_triggers, userid, local_user_data, stock_cache,
                                             log_queue)
                    if message != '':
                        message = message.encode('utf-8')
                        client_socket.send(message)

            # only need to update the most recent one as it is the only one that can be dealt with
            # may want to reduce the number of servers sent to this function
            if len(arguments) > 1:
                refresh_pending(client_socket, local_user_data, userid, stock_cache, log_queue)

            returnData = 'Invalid Command'

            #parse command and go to function
            if command== "ADD":
                # print("ADD..")
                userid = arguments[0]

                try:
                    cent_amount = int(round(float(arguments[1]) * 100))

                    # GENERATE USERCOMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'ADD'), (now(), SERVER_NAME, t_num, userid, cent_amount),
                                               log_queue)

                    # UPDATE DATABASE
                    returnData = ADD(local_user_data, userid, cent_amount, t_num, log_queue)

                except ValueError as error:
                    cent_amount = arguments[1]
                    timestamp = now()
                    log_generator.generate_log(('USER', 'ADD'), (timestamp, SERVER_NAME, t_num, userid, cent_amount),
                                               log_queue)
                    log_generator.generate_log(('ERROR', 'ADD'), (timestamp, SERVER_NAME, t_num, userid, cent_amount,
                                                                  'Add amount must be a number value.'),
                                                                  log_queue)
                    log_generator.generate_log(('DEBUG', 'ADD'), (timestamp, SERVER_NAME, t_num, userid, cent_amount,
                                                                  'Add amount must be a number value.'),
                                                                  log_queue)
                    # write log

            elif command== "QUOTE":
                # print("QUOTE..")
                userid = arguments[0]
                stock_symbol = arguments[1]

                # GENERATE USERCOMMAND LOG ENTRY HERE
                log_generator.generate_log(('USER', 'QUOTE'), (now(), SERVER_NAME, t_num, userid, stock_symbol),
                                           log_queue)

                # GET STOCK PRICE
                returnData = QUOTE(userid, stock_symbol, t_num, stock_cache, log_queue)

            elif command== "BUY":
                # print("BUY..")
                userid = arguments[0]
                stock_symbol = arguments[1]
                try:
                    cent_amount = int(round(float(arguments[2]) * 100))

                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'BUY'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                           log_queue)

                    returnData = BUY(local_user_data, userid, stock_symbol, cent_amount, t_num, stock_cache,
                                 log_queue)
                except ValueError as error:
                    cent_amount = arguments[2]
                    timestamp = now()
                    log_generator.generate_log(('USER', 'BUY'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                           log_queue)
                    log_generator.generate_log(('ERROR', 'BUY'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount,'Buy amount must be a number value.'),
                                                                  log_queue)
                    log_generator.generate_log(('DEBUG', 'BUY'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Buy amount must be a number value.'),
                                                                  log_queue)
                    # Error log

            elif command == 'COMMIT_BUY':
                # print('COMMIT_BUY..')
                userid = arguments[0]

                # GENERATE USER COMMAND LOG ENTRY HERE
                log_generator.generate_log(('USER', 'COMMIT_BUY'), (now(), SERVER_NAME, t_num, userid),
                                           log_queue)

                returnData = COMMIT_BUY(local_user_data, userid, t_num, log_queue)

            elif command == 'CANCEL_BUY':
                # print('CANCEL_BUY..')
                # 'CANCEL_BUY': (1, 'user'),  # userid
                userid = arguments[0]

                # GENERATE USER COMMAND LOG ENTRY HERE
                log_generator.generate_log(('USER', 'CANCEL_BUY'), (now(), SERVER_NAME, t_num, userid), log_queue)

                returnData = CANCEL_BUY(local_user_data, userid, t_num, log_queue)

            elif command == 'SELL':
                # print('SELL..')
                userid = arguments[0]
                stock_symbol = arguments[1]
                try:
                    cent_amount = int(round(float(arguments[2]) * 100))

                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'SELL'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount), log_queue)

                    returnData = SELL(local_user_data, userid, stock_symbol, cent_amount, t_num, stock_cache,
                                  log_queue)
                except ValueError as error:
                    timestamp = now()
                    cent_amount = arguments[2]
                    log_generator.generate_log(('USER', 'SELL'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount), log_queue)
                    log_generator.generate_log(('ERROR', 'SELL'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Sell amount must be a number value.'),
                                               log_queue)
                    log_generator.generate_log(('DEBUG', 'SELL'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Sell amount must be a number value.'),
                                               log_queue)
                    # error log

            elif command == 'COMMIT_SELL':
                # print('COMMIT_SELL..')
                userid = arguments[0]

                # GENERATE USER COMMAND LOG ENTRY HERE
                log_generator.generate_log(('USER', 'COMMIT_SELL'), (now(), SERVER_NAME, t_num, userid), log_queue)

                returnData = COMMIT_SELL(local_user_data, userid, t_num, log_queue)

            elif command== "CANCEL_SELL":
                # print("CANCEL_SELL..")
                # 'CANCEL_SELL': (1, 'user'),  # userid
                userid = arguments[0]

                # GENERATE USER COMMAND LOG ENTRY HERE
                log_generator.generate_log(('USER', 'CANCEL_SELL'), (now(), SERVER_NAME, t_num, userid), log_queue)

                returnData = CANCEL_SELL(local_user_data, userid, t_num, log_queue)

            elif command == 'SET_BUY_AMOUNT':
                # print("SET_BUY_AMOUNT..")
                userid = arguments[0]
                stock_symbol = arguments[1]

                try:
                    cent_amount = int(round(float(arguments[2]) * 100))

                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'SET_BUY_AMOUNT'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                           log_queue)

                    returnData = SET_BUY_AMOUNT(local_user_data, userid, stock_symbol, cent_amount, t_num, log_queue)
                except ValueError as error:
                    timestamp = now()
                    cent_amount = arguments[2]
                    log_generator.generate_log(('USER', 'SET_BUY_AMOUNT'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                           log_queue)
                    log_generator.generate_log(('ERROR', 'SET_BUY_AMOUNT'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Set buy amount must be a number value.'),
                                               log_queue)
                    log_generator.generate_log(('DEBUG', 'SET_BUY_AMOUNT'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Set buy amount must be a number value.'),
                                               log_queue)
                    # write error log

            elif command== "SET_BUY_TRIGGER":
                # print("SET_BUY_TRIGGER..")
                userid = arguments[0]
                stock_symbol = arguments[1]
                try:
                    cent_amount = int(round(float(arguments[2]) * 100))
                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'SET_BUY_TRIGGER'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                               log_queue)

                    returnData = SET_BUY_TRIGGER(local_user_data, userid, stock_symbol, cent_amount, t_num, stock_cache,
                                                 log_queue, buy_triggers)
                except ValueError as error:
                    timestamp = now()
                    cent_amount = arguments[2]
                    log_generator.generate_log(('USER', 'SET_BUY_TRIGGER'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                               log_queue)
                    log_generator.generate_log(('ERROR', 'SET_BUY_TRIGGER'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Buy trigger must be a number value.'),
                                               log_queue)
                    log_generator.generate_log(('DEBUG', 'SET_BUY_TRIGGER'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Buy trigger must be a number value.'),
                                               log_queue)
                    # write error and debug log

            elif command== "CANCEL_SET_BUY":
                # print("CANCEL_SET_BUY..")
                userid = arguments[0]
                stock_symbol = arguments[1]

                # GENERATE USER COMMAND LOG ENTRY HERE
                log_generator.generate_log(('USER', 'CANCEL_SET_BUY'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol),
                                           log_queue)

                returnData = CANCEL_SET_BUY(local_user_data, userid, stock_symbol, t_num, log_queue, buy_triggers)

            elif command== "SET_SELL_AMOUNT":
                # print("SET_BUY_AMOUNT..")
                userid = arguments[0]
                stock_symbol = arguments[1]
                try:
                    cent_amount = int(round(float(arguments[2]) * 100))

                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'SET_SELL_AMOUNT'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                               log_queue)

                    returnData = SET_SELL_AMOUNT(local_user_data, userid, stock_symbol, cent_amount, t_num, log_queue)
                except ValueError as error:
                    timestamp = now()
                    cent_amount = arguments[2]
                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'SET_SELL_AMOUNT'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                               log_queue)
                    log_generator.generate_log(('ERROR', 'SET_SELL_AMOUNT'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Set sell amount must be a number value.'),
                                               log_queue)
                    log_generator.generate_log(('DEBUG', 'SET_SELL_AMOUNT'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Set sell amount must be a number value.'),
                                               log_queue)
                    #generate error log and debug log

            elif command== "SET_SELL_TRIGGER":
                # print("SET_SELL_TRIGGER..")
                userid = arguments[0]
                stock_symbol = arguments[1]
                try:
                    cent_amount = int(round(float(arguments[2]) * 100))

                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'SET_SELL_TRIGGER'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                               log_queue)

                    returnData = SET_SELL_TRIGGER(local_user_data, userid, stock_symbol, cent_amount, t_num, stock_cache,
                                              log_queue, sell_triggers)
                except ValueError as error:
                    timestamp = now()
                    cent_amount = arguments[2]
                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'SET_SELL_TRIGGER'),
                                               (now(), SERVER_NAME, t_num, userid, stock_symbol, cent_amount),
                                               log_queue)
                    log_generator.generate_log(('ERROR', 'SET_SELL_TRIGGER'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Set sell trigger must be a number value.'),
                                               log_queue)
                    log_generator.generate_log(('DEBUG', 'SET_SELL_TRIGGER'), (timestamp, SERVER_NAME, t_num, userid, stock_symbol,
                                                                  cent_amount, 'Set sell trigger must be a number value.'),
                                               log_queue)
                    #generate error log and debug log

            elif command== "CANCEL_SET_SELL":
                # print("CANCEL_SET_SELL..")
                userid = arguments[0]
                stock_symbol = arguments[1]

                # GENERATE USER COMMAND LOG ENTRY HERE
                log_generator.generate_log(('USER', 'CANCEL_SET_SELL'),
                                           (now(), SERVER_NAME, t_num, userid, stock_symbol),
                                           log_queue)

                returnData = CANCEL_SET_SELL(local_user_data, userid, stock_symbol, t_num, log_queue, sell_triggers)

            elif command== "DISPLAY_SUMMARY":
                # print("DISPLAY_SUMMARY..")
                userid = arguments[0]

                # GENERATE USER COMMAND LOG ENTRY HERE
                log_generator.generate_log(('USER', 'DISPLAY_SUMMARY'),
                                           (now(), SERVER_NAME, t_num, userid), log_queue)

                returnData = DISPLAY_SUMMARY(local_user_data, userid, t_num, log_queue)

            elif command == 'DUMPLOG':
                if len(arguments) == 2:
                    userid = arguments[0]
                    filename = arguments[1].rstrip()
                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'DUMPLOG'), (now(), SERVER_NAME, t_num, userid, filename),
                                               log_queue)
                else:
                    userid = None
                    filename = arguments[0].rstrip()
                    # GENERATE USER COMMAND LOG ENTRY HERE
                    log_generator.generate_log(('USER', 'DUMPLOG'), (now(), SERVER_NAME, t_num, userid, filename),
                                               log_queue)

                log_server = connections.connect_to_log_server()

                DUMPLOG(log_server, filename, userid, t_num, log_queue, client_socket)
                returnData = '\n'
                
            elif command == "PING":
                returnData = 'ping\n'
                
            else:
                # print("Invalid Command")
                # print(command)
                returnData = 'InvalidCommand'

            returnData = returnData.encode("utf-8") #encode into bytes data
            client_socket.send(returnData)
            t_count += 1

    client_socket.close()
    flush = True
    if local_user_data is not None:
        userid = local_user_data.get_userid()
        userids.remove(userid)
        for i in buy_triggers:
            message = 'push,buy,' + userid
            for j in i:
                message += (',' + str(j))
            message += ';'
            with TRIGGER_LOCK:
                trigger_messages.append(message)
        for i in sell_triggers:
            message = 'push,sell,' + userid
            for j in i:
                message += (',' + str(j))
            message += ';'
            trigger_messages.append(message)
    print('done'+str(thread))


def send_to_log_server(s):
    # want to ensure that the log_writer thread and function is not running while this is being run
    try:
        #log_file = open('log_file.xml', 'wt')
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


def listen_for_dump(log_queue):
    global close
    global pause_sync
    global PAUSE_LOCK
    global DUMPLOG_DELAY

    while True:
        log_server = connections.connect_to_log_server()
        #send any outstanding log_file entries to the server
        #print('shouldnt be here yet')
        send_to_log_server(log_server)
        log_server.close()
        log_thread = Thread(target=write_logs, args=(log_queue,))
        log_thread.start()
        log_server = connections.connect_to_log_server()
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


def sync_users(connected_users, userids):

    db_user = connections.connect_to_database_user()
    remove_indexes = []
    global pause_sync
    global PAUSE_LOCK
    global SYNC_DELAY
    global DUMPLOG_DELAY

    # could split this into seperate threads
    while True:
        time.sleep(SYNC_DELAY)
        for i in range(len(connected_users)):
            if pause_sync == True:
                time.sleep(DUMPLOG_DELAY)
                with PAUSE_LOCK:
                    pause_sync = False
            user = connected_users[i]
            user.sync_user(db_user)
            if user.get_userid() not in userids:
                remove_indexes.append(i)

        remove_indexes.reverse()
        for i in remove_indexes:
            del connected_users[i]

        remove_indexes = []


def main():
    count = 0
    #dictionary to hold stock values to avoid needlessly making requests to quote server
    stock_cache = {}
    buy_triggers = []  # userid, stock_symbol, t_num, trigger, cent_amount
    sell_triggers = []  # userid, stock_symbol, t_num, trigger, cent_amount
    connected_users = []  # may want to change this to a set
    userids = []
    threads = []
    log_queue = []
    trigger_messages = []

    dumplog_thread = Thread(target=listen_for_dump, args=(log_queue,))
    dumplog_thread.start()

    trigger_thread = Thread(target=listen_to_trigger_server, args=(trigger_messages,))
    trigger_thread.start()

    server_socket = connections.bind_to_socket(8080)
    server_socket.listen(10)

    user_sync_thread = Thread(target=sync_users, args=(connected_users, userids))
    user_sync_thread.start()

    while True:
        count += 1
        try:
            client_socket, address = server_socket.accept()
            # print("Connection from", address)
            client_thread = Thread(target=on_new_client, args=(client_socket, address, stock_cache, connected_users,
                                                               buy_triggers, sell_triggers, count, log_queue,
                                                               userids, trigger_messages))
            threads.append(client_thread)
            client_thread.start()
        except Exception as e:
            pass
            # something went wrong
            print(e)

    server_socket.close()
    print("Server closed")

if __name__ == "__main__":
    main()
