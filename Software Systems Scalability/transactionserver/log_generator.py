def generate_log(kind, arguments, log_queue):

#-----------------------------------------------------------------------------------------------------------------------
    if kind[0] == 'USER':
        # now we need to check the command
        if kind[1] == 'ADD':
            timestamp, server, transaction_num, userid, funds = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'ADD', None, None, userid,
                              None, funds, None, None, None, None, None])

        elif kind[1] == 'QUOTE':
            timestamp, server, transaction_num, userid, stock_symbol = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'QUOTE', None, None, userid,
                              stock_symbol, None, None, None, None, None, None])

        elif kind[1] == 'BUY':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'BUY', None, None, userid,
                              stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'COMMIT_BUY':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'COMMIT_BUY', None, None, userid,
                              None, None, None, None, None, None, None])

        elif kind[1] == 'CANCEL_BUY':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'CANCEL_BUY', None, None, userid,
                              None, None, None, None, None, None, None])

        elif kind[1] == 'SELL':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'SELL', None, None, userid,
                              stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'COMMIT_SELL':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'COMMIT_SELL', None, None,
                              userid, None, None, None, None, None, None, None])

        elif kind[1] == 'CANCEL_SELL':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'CANCEL_SELL', None, None,
                              userid, None, None, None, None, None, None, None])

        elif kind[1] == 'SET_BUY_AMOUNT':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'SET_BUY_AMOUNT', None, None,
                              userid, stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'SET_BUY_TRIGGER':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'SET_BUY_TRIGGER', None, None,
                              userid, stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'CANCEL_SET_BUY':
            timestamp, server, transaction_num, userid, stock_symbol = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'CANCEL_SET_BUY', None, None,
                              userid, stock_symbol, None, None, None, None, None, None])

        elif kind[1] == 'SET_SELL_AMOUNT':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'SET_SELL_AMOUNT', None, None,
                              userid, stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'SET_SELL_TRIGGER':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'SET_SELL_TRIGGER', None, None,
                              userid, stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'CANCEL_SET_SELL':
            timestamp, server, transaction_num, userid, stock_symbol = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'CANCEL_SET_SELL', None, None,
                              userid, stock_symbol, None, None, None, None, None, None])

        elif kind[1] == 'DISPLAY_SUMMARY':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'DISPLAY_SUMMARY', None, None,
                              userid, None, None, None, None, None, None, None])

        elif kind[1] == 'DUMPLOG':
            timestamp, server, transaction_num, userid, filename = arguments
            log_queue.append([None, 'userCommand', timestamp, server, transaction_num, 'DUMPLOG', None, None,
                              userid, None, None, None, None, filename, None, None])
        else:
            print('****************************** WARNING:  NO USER LOG ENTRY CREATED! ******************************')

#-----------------------------------------------------------------------------------------------------------------------
# DONE ***** (I THINK)

    elif kind[0] == 'ACCOUNT':
        timestamp, server, transaction_num, action, userid, funds = arguments
        log_queue.append([None, 'accountTransaction', timestamp, server, transaction_num, None, None, action, userid,
                          None, funds, None, None, None, None, None])
# DONE *****
#-----------------------------------------------------------------------------------------------------------------------
# DONE ***** (I THINK)

    elif kind[0] == 'QUOTE':
        timestamp, server, transaction_num, price, stock_symbol, userid, quote_server_time, crypto_key = arguments
        log_queue.append([None, 'quoteServer', timestamp, server, transaction_num, None, price, None, userid,
                          stock_symbol, None, quote_server_time, crypto_key, None, None, None])

# DONE *****
# ----------------------------------------------------------------------------------------------------------------------
    elif kind[0] == 'ERROR':
        # now we need to check the command
        if kind[1] == 'ADD':
            timestamp, server, transaction_num, userid, funds, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'ADD', None, None, userid,
                              None, funds, None, None, None, error_message, None])

        elif kind[1] == 'QUOTE':
            timestamp, server, transaction_num, userid, stock_symbol, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'QUOTE', None, None, userid,
                              stock_symbol, None, None, None, None, error_message, None])

        elif kind[1] == 'BUY':
            timestamp, server, transaction_num, userid, stock_symbol, funds, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'BUY', None, None, userid,
                              stock_symbol, funds, None, None, None, error_message, None])

        elif kind[1] == 'COMMIT_BUY':
            timestamp, server, transaction_num, userid, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'COMMIT_BUY', None, None, userid,
                              None, None, None, None, None, error_message, None])

        elif kind[1] == 'CANCEL_BUY':
            timestamp, server, transaction_num, userid, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'CANCEL_BUY', None, None, userid,
                              None, None, None, None, None, error_message, None])

        elif kind[1] == 'SELL':
            timestamp, server, transaction_num, userid, stock_symbol, funds, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'SELL', None, None, userid,
                              stock_symbol, funds, None, None, None, error_message, None])

        elif kind[1] == 'COMMIT_SELL':
            timestamp, server, transaction_num, userid, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'COMMIT_SELL', None, None,
                              userid, None, None, None, None, None, error_message, None])

        elif kind[1] == 'CANCEL_SELL':
            timestamp, server, transaction_num, userid, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'CANCEL_SELL', None, None,
                              userid, None, None, None, None, None, error_message, None])

        elif kind[1] == 'SET_BUY_AMOUNT':
            timestamp, server, transaction_num, userid, stock_symbol, funds, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'SET_BUY_AMOUNT', None, None,
                              userid, stock_symbol, funds, None, None, None, error_message, None])

        elif kind[1] == 'SET_BUY_TRIGGER':
            timestamp, server, transaction_num, userid, stock_symbol, funds, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'SET_BUY_TRIGGER', None, None,
                              userid, stock_symbol, funds, None, None, None, error_message, None])

        elif kind[1] == 'CANCEL_SET_BUY':
            timestamp, server, transaction_num, userid, stock_symbol, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'CANCEL_SET_BUY', None, None,
                              userid, stock_symbol, None, None, None, None, error_message, None])

        elif kind[1] == 'SET_SELL_AMOUNT':
            timestamp, server, transaction_num, userid, stock_symbol, funds, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'SET_SELL_AMOUNT', None, None,
                              userid, stock_symbol, funds, None, None, None, error_message, None])

        elif kind[1] == 'SET_SELL_TRIGGER':
            timestamp, server, transaction_num, userid, stock_symbol, funds, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'SET_SELL_TRIGGER', None, None,
                              userid, stock_symbol, funds, None, None, None, error_message, None])

        elif kind[1] == 'CANCEL_SET_SELL':
            timestamp, server, transaction_num, userid, stock_symbol, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'CANCEL_SET_SELL', None, None,
                              userid, stock_symbol, None, None, None, None, error_message, None])

        elif kind[1] == 'DISPLAY_SUMMARY':
            timestamp, server, transaction_num, userid, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'DISPLAY_SUMMARY', None, None,
                              userid, None, None, None, None, None, error_message, None])

        elif kind[1] == 'DUMPLOG':
            timestamp, server, transaction_num, userid, filename, error_message = arguments
            log_queue.append([None, 'errorEvent', timestamp, server, transaction_num, 'DUMPLOG', None, None,
                              userid, None, None, None, None, filename, error_message, None])

        else:
            print('****************************** WARNING:  NO ERROR LOG ENTRY CREATED! ******************************')

    elif kind[0] == 'SYSTEM':
        # now we need to check the command
        if kind[1] == 'ADD':
            timestamp, server, transaction_num, userid, funds = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'ADD', None, None, userid,
                              None, funds, None, None, None, None, None])

        elif kind[1] == 'QUOTE':
            timestamp, server, transaction_num, userid, stock_symbol = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'QUOTE', None, None, userid,
                              stock_symbol, None, None, None, None, None, None])

        elif kind[1] == 'BUY':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'BUY', None, None, userid,
                              stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'COMMIT_BUY':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'COMMIT_BUY', None, None, userid,
                              None, None, None, None, None, None, None])

        elif kind[1] == 'CANCEL_BUY':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'CANCEL_BUY', None, None, userid,
                              None, None, None, None, None, None, None])

        elif kind[1] == 'SELL':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'SELL', None, None, userid,
                              stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'COMMIT_SELL':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'COMMIT_SELL', None, None,
                              userid, None, None, None, None, None, None, None])

        elif kind[1] == 'CANCEL_SELL':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'CANCEL_SELL', None, None,
                              userid, None, None, None, None, None, None, None])

        elif kind[1] == 'SET_BUY_AMOUNT':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'SET_BUY_AMOUNT', None, None,
                              userid, stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'SET_BUY_TRIGGER':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'SET_BUY_TRIGGER', None, None,
                              userid, stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'CANCEL_SET_BUY':
            timestamp, server, transaction_num, userid, stock_symbol = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'CANCEL_SET_BUY', None, None,
                              userid, stock_symbol, None, None, None, None, None, None])

        elif kind[1] == 'SET_SELL_AMOUNT':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'SET_SELL_AMOUNT', None, None,
                              userid, stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'SET_SELL_TRIGGER':
            timestamp, server, transaction_num, userid, stock_symbol, funds = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'SET_SELL_TRIGGER', None, None,
                              userid, stock_symbol, funds, None, None, None, None, None])

        elif kind[1] == 'CANCEL_SET_SELL':
            timestamp, server, transaction_num, userid, stock_symbol = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'CANCEL_SET_SELL', None, None,
                              userid, stock_symbol, None, None, None, None, None, None])

        elif kind[1] == 'DISPLAY_SUMMARY':
            timestamp, server, transaction_num, userid = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'DISPLAY_SUMMARY', None, None,
                              userid, None, None, None, None, None, None, None])

        elif kind[1] == 'DUMPLOG':
            timestamp, server, transaction_num, userid, filename = arguments
            log_queue.append([None, 'systemEvent', timestamp, server, transaction_num, 'DUMPLOG', None, None,
                              userid, None, None, None, None, filename, None, None])

        else:
            print('****************************** WARNING: NO SYSTEM LOG ENTRY CREATED! ******************************')

    elif kind[0] == 'DEBUG':
        # now we need to check the command
        if kind[1] == 'ADD':
            timestamp, server, transaction_num, userid, funds, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'ADD', None, None, userid,
                              None, funds, None, None, None, None, debug_message])

        elif kind[1] == 'QUOTE':
            timestamp, server, transaction_num, userid, stock_symbol, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'QUOTE', None, None, userid,
                              stock_symbol, None, None, None, None, None, debug_message])

        elif kind[1] == 'BUY':
            timestamp, server, transaction_num, userid, stock_symbol, funds, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'BUY', None, None, userid,
                              stock_symbol, funds, None, None, None, None, debug_message])

        elif kind[1] == 'COMMIT_BUY':
            timestamp, server, transaction_num, userid, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'COMMIT_BUY', None, None, userid,
                              None, None, None, None, None, None, debug_message])

        elif kind[1] == 'CANCEL_BUY':
            timestamp, server, transaction_num, userid, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'CANCEL_BUY', None, None, userid,
                              None, None, None, None, None, None, debug_message])

        elif kind[1] == 'SELL':
            timestamp, server, transaction_num, userid, stock_symbol, funds, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'SELL', None, None, userid,
                              stock_symbol, funds, None, None, None, None, debug_message])

        elif kind[1] == 'COMMIT_SELL':
            timestamp, server, transaction_num, userid, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'COMMIT_SELL', None, None,
                              userid, None, None, None, None, None, None, debug_message])

        elif kind[1] == 'CANCEL_SELL':
            timestamp, server, transaction_num, userid, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'CANCEL_SELL', None, None,
                              userid, None, None, None, None, None, None, debug_message])

        elif kind[1] == 'SET_BUY_AMOUNT':
            timestamp, server, transaction_num, userid, stock_symbol, funds, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'SET_BUY_AMOUNT', None, None,
                              userid, stock_symbol, funds, None, None, None, None, debug_message])

        elif kind[1] == 'SET_BUY_TRIGGER':
            timestamp, server, transaction_num, userid, stock_symbol, funds, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'SET_BUY_TRIGGER', None, None,
                              userid, stock_symbol, funds, None, None, None, None, debug_message])

        elif kind[1] == 'CANCEL_SET_BUY':
            timestamp, server, transaction_num, userid, stock_symbol, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'CANCEL_SET_BUY', None, None,
                              userid, stock_symbol, None, None, None, None, None, debug_message])

        elif kind[1] == 'SET_SELL_AMOUNT':
            timestamp, server, transaction_num, userid, stock_symbol, funds, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'SET_SELL_AMOUNT', None, None,
                              userid, stock_symbol, funds, None, None, None, None, debug_message])

        elif kind[1] == 'SET_SELL_TRIGGER':
            timestamp, server, transaction_num, userid, stock_symbol, funds, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'SET_SELL_TRIGGER', None, None,
                              userid, stock_symbol, funds, None, None, None, None, debug_message])

        elif kind[1] == 'CANCEL_SET_SELL':
            timestamp, server, transaction_num, userid, stock_symbol, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'CANCEL_SET_SELL', None, None,
                              userid, stock_symbol, None, None, None, None, None, debug_message])

        elif kind[1] == 'DISPLAY_SUMMARY':
            timestamp, server, transaction_num, userid, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'DISPLAY_SUMMARY', None, None,
                              userid, None, None, None, None, None, None, debug_message])

        elif kind[1] == 'DUMPLOG':
            timestamp, server, transaction_num, userid, filename, debug_message = arguments
            log_queue.append([None, 'debugEvent', timestamp, server, transaction_num, 'DUMPLOG', None, None,
                              userid, None, None, None, None, filename, None, debug_message])

        else:
            print('****************************** WARNING:  NO DEBUG LOG ENTRY CREATED! ******************************')
    else:
        print('****************************** WARNING:  UNKNOWN LOG ENTRY TYPE! ******************************')

'''        
def write_log(db_log, sql, val):

    assert(len(sql) == len(val))
    mycursor = db_log.cursor(buffered=True)
    for i in range(len(sql)):
        mycursor.execute(sql[i], val[i])
    db_log.commit()
    sql = []
    val = []
    return
'''