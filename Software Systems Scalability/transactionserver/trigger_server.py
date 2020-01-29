import connections
import log_generator
import socket
import time
import re

SERVER_NAME = socket.gethostname()
TRIGGER_INTERVAL = 600000

def now():
    return int(round(time.time() * 1000))

def quote_server_request(userid, stock_symbol, s):
    # Send the user's query
    message = stock_symbol + ', ' + userid + '\n'
    try:
        s.send(message.encode())
    except TimeoutError:
        s = connect_to_quote_server()

    # Read and print up to 1k of data.

    # returns: 'quote,sym,userid,timestamp,cryptokey'
    data = s.recv(1024)
    data = data.decode()

    #data = '123.45,' + stock_symbol + ',' + userid + ',' + str(now()) + ',' + 'IRrR7UeTO35kSWUgG0QJKmB35sL27FKM7AVhP5qpjCgmWQeXFJs35g=='
    return data.split(',')

def QUOTE(db, userid, stock_symbol, t_num, stock_cache):

    # check to see if the stock_symbol is valid
    if not re.match('^([a-z]|[A-Z]){1,3}$', stock_symbol):
        log_generator.generate_log(db, ('ERROR', 'QUOTE'), (now(), SERVER_NAME, t_num, userid, stock_symbol,
                                                            'Stock symbol does not exist.'))
        log_generator.generate_log(db, ('DEBUG', 'QUOTE'), (now(), SERVER_NAME, t_num, userid, stock_symbol,
                                                            'Symbol must be 0-3 characters from the english alphabet'))
        print('Error: Stock symbol "{}" does not exist. '.format(stock_symbol))
        return('Error: Stock symbol "{}" does not exist. '.format(stock_symbol))

    # before making a request to the quote server first check to see if the value exists in the stock_cache

    # ****someone with more threading experience should refine this lock****
    with cache_lock:
        if stock_symbol in stock_cache:
            quote, expiry = stock_cache[stock_symbol]
            if expiry > now():
                print('Stock {} QUOTED {:.2f} to userid: {}'.format(stock_symbol, round((quote/100.0), 2), userid))
                return ('Stock {} QUOTED {:.2f} to userid: {}'.format(stock_symbol, round((quote/100.0), 2), userid))

        timestamp = now()
        quote, sym, userid_ret, quote_timestamp, cryptokey = quote_server_request(userid, stock_symbol)
        quote = int(round(float(quote)*100))
        # cryptokey = cryptokey.strip('\n')  #may not want to do this
        # print(now())
        # print(quote_timestamp)

        log_generator.generate_log(db, ('QUOTE',), (timestamp, 'QS', t_num, quote, stock_symbol, userid,
                                                    quote_timestamp, cryptokey))

        if userid_ret == 'NA':  # userid can't be 'NA'
            # invalid entry to server
            log_generator.generate_log(db, ('ERROR', 'QUOTE'), (now(), 'QS', t_num, userid, stock_symbol,
                                                                'Invalid server request.'))
            log_generator.generate_log(db, ('DEBUG', 'QUOTE'), (now(), 'QS', t_num, userid, stock_symbol,
                                                                'Invalid server request.'))

            print('Error: Invalid server request - "{}, {}". '.format(userid, stock_symbol))
            return('Error: Invalid server request - "{}, {}". '.format(userid, stock_symbol))
        else:
            quote_timestamp = int(quote_timestamp)  # verify the format of response from quote server

            stock_cache[stock_symbol] = (quote, quote_timestamp + 60000)

            log_generator.generate_log(db, ('SYSTEM', 'QUOTE'), (now(), SERVER_NAME, t_num, userid, stock_symbol))

            # return this result to the user
            return ('Stock {} QUOTED {:.2f} to userid: {}'.format(stock_symbol, round((quote/100.0), 2), userid))

def check_triggers(db, userid, stock_symbol, t_num, stock_cache, trigger, cent_amount, which):
    QUOTE(db, userid, stock_symbol, t_num, stock_cache)
    quote, expiry = stock_cache[stock_symbol]
    if which == 'buy':
        if quote <= trigger:
            # proceed with buy, funds are already reserved
            mycursor = db.cursor(buffered=True)

            num_stocks = cent_amount // quote
            cost = num_stocks * quote

            diff = cent_amount - cost

            sql = 'SELECT accessible_money, reserved_money FROM users WHERE userid = %s'
            val = (userid,)
            mycursor.execute(sql, val)
            accessible_money, reserved_money = mycursor.fetchone()

            sql = 'UPDATE users SET accessible_money = %s, reserved_money = %s WHERE userid = %s'
            val = ((accessible_money + diff), (reserved_money - cent_amount), userid)
            mycursor.execute(sql, val)

            sql = 'SELECT accessible_stocks FROM user_stocks WHERE userid = %s AND stock_name = %s'
            val = (userid, stock_symbol)
            mycursor.execute(sql, val)
            accessible_stocks = mycursor.fetchone()[0]

            sql = 'UPDATE user_stocks SET accessible_stocks = %s, buy_amount = %s, buy_trigger = %s' \
                  ' WHERE userid = %s AND stock_name = %s'
            val = ((accessible_stocks+num_stocks), None, None, userid, stock_symbol)
            mycursor.execute(sql, val)

            db.commit()

            log_generator.generate_log(db, ('SYSTEM', 'SET_BUY_TRIGGER'),
                                       (now(), SERVER_NAME, t_num, userid, stock_symbol, trigger))
            # Account Transaction Log Entry here
            log_generator.generate_log(db, ('ACCOUNT',), (now(), 'DB1', t_num, 'remove', userid, cost))

            return ("BUY TRIGGER ACTIVATED" + stock_symbol + " " + str(round((cost / 100.0), 2)) + " " + userid)
        return
    elif which == 'sell':
        if quote >= trigger:
            # proceed with sell stocks are already reserved
            mycursor = db.cursor(buffered=True)

            previously_reserved = cent_amount // trigger
            actual_num_stocks = cent_amount // quote

            value = actual_num_stocks * quote

            diff = previously_reserved - actual_num_stocks

            sql = 'SELECT accessible_money FROM users WHERE userid = %s'
            val = (userid,)
            mycursor.execute(sql, val)
            accessible_money = mycursor.fetchone()[0]

            sql = 'UPDATE users SET accessible_money = %s WHERE userid = %s'
            val = ((accessible_money + value), userid)
            mycursor.execute(sql, val)

            sql = 'SELECT accessible_stocks, reserved_stocks FROM user_stocks WHERE userid = %s AND stock_name = %s'
            val = (userid, stock_symbol)
            mycursor.execute(sql, val)
            accessible_stocks, reserved_stocks = mycursor.fetchone()

            sql = 'UPDATE user_stocks SET accessible_stocks = %s, reserved_stocks = %s, sell_amount = %s, ' \
                  'sell_trigger = %s WHERE userid = %s AND stock_name = %s'
            val = ((accessible_stocks + diff), (reserved_stocks - previously_reserved), None,
                   None, userid, stock_symbol)
            mycursor.execute(sql, val)

            db.commit()

            log_generator.generate_log(db, ('SYSTEM', 'SET_SELL_TRIGGER'),
                                       (now(), SERVER_NAME, t_num, userid, stock_symbol, trigger))
            # Account Transaction Log Entry here
            log_generator.generate_log(db, ('ACCOUNT',), (now(), 'DB1', t_num, 'add', userid, value))

            return ("SELL TRIGGER ACTIVATED" + stock_symbol + " " + str(round((value / 100.0), 2)) + " " + userid)
        return


def main():
    db = connections.connect_to_database()
    mycursor = db.cursor(buffered=True)

    sql = 'SELECT userid, stock_name, bt_t_num, buy_trigger, buy_amount FROM user_stocks WHERE buy_trigger IS NOT NULL'
    mycursor.execute(sql, )
    buy_triggers = mycursor.fetchall()

    sql = 'SELECT userid, stock_name, st_t_num, sell_trigger, sell_amount FROM user_stocks WHERE sell_trigger IS NOT NULL'
    mycursor.execute(sql, )
    sell_triggers = mycursor.fetchall()

    if buy_triggers is not None:
        for i in buy_triggers:
            userid = i[0]
            stock_symbol = i[1]
            t_num = i[2]
            trigger = i[3]
            cent_amount = i[4]
            check_triggers(db, userid, stock_symbol, t_num, stock_cache, trigger, cent_amount, 'buy')
    buy_trigger_time = now() + TRIGGER_INTERVAL  # check every 10 minute
    if sell_triggers is not None:
        for i in sell_triggers:
            userid = i[0]
            stock_symbol = i[1]
            t_num = i[2]
            trigger = i[3]
            cent_amount = i[4]
            check_triggers(db, userid, stock_symbol, t_num, stock_cache, trigger, cent_amount, 'sell')
    sell_trigger_time = now() + TRIGGER_INTERVAL  # check every 10 minute


    while True:
        if now() > buy_trigger_time:
            sql = 'SELECT userid, stock_name, bt_t_num, buy_trigger, buy_amount FROM user_stocks WHERE buy_trigger IS NOT NULL'
            mycursor.execute(sql, )
            buy_triggers = mycursor.fetchall()
            if buy_triggers is not None:
                for i in buy_triggers:
                    userid = i[0]
                    stock_symbol = i[1]
                    t_num = i[2]
                    trigger = i[3]
                    cent_amount = i[4]
                    check_triggers(db, userid, stock_symbol, t_num, stock_cache, trigger, cent_amount, 'buy')
            buy_trigger_time = now() + TRIGGER_INTERVAL  # check every 10 minute

        if now() > sell_trigger_time:
            sql = 'SELECT userid, stock_name, st_t_num, sell_trigger, sell_amount FROM user_stocks WHERE sell_trigger IS NOT NULL'
            mycursor.execute(sql, )
            sell_triggers = mycursor.fetchall()
            if sell_triggers is not None:
                for i in sell_triggers:
                    userid = i[0]
                    stock_symbol = i[1]
                    t_num = i[2]
                    trigger = i[3]
                    cent_amount = i[4]
                    check_triggers(db, userid, stock_symbol, t_num, stock_cache, trigger, cent_amount, 'sell')
            sell_trigger_time = now() + TRIGGER_INTERVAL  # check every 10 minute