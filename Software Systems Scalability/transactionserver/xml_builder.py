import mysql.connector
import socket
import time

def generateXML(db, client_socket, filename, userid=None):
    # eventually will want to send the file over the socket once everything is connected, but for now will
    # just write it to file on local machine
    # NOTE: we will need to come up with a protocol for transfering these files because they will likely
    # be longer than the 1024 bytes currently expected.

    time.sleep(30.0)

    mycursor = db.cursor(buffered=True)

    if userid is None:
        mycursor.execute('SELECT * FROM log_entries')
    else:
        sql = 'SELECT * FROM log_entries WHERE userid = %s'
        mycursor.execute(sql, (userid, ))

    #print(all_entries)

    message = '<?xml version="1.0"?>\n<log>\n\n'
    message = message.encode()
    client_socket.sendall(message)
    while True:
        print('loop')
        i = mycursor.fetchone()
        if i is None: break
        message = '\t<' + i[1] + '>\n'
        message += '\t\t<timestamp>' + str(i[2]) + '</timestamp>\n'
        message += '\t\t<server>' + i[3] + '</server>\n'
        message += '\t\t<transactionNum>' + str(i[4]) + '</transactionNum>\n'
        if i[5] is not None:
            message += '\t\t<command>' + str(i[5]) + '</command>\n'
        if i[7] is not None:
            message += '\t\t<action>' + str(i[7]) + '</action>\n'
        if i[8] is not None:
            message += '\t\t<username>' + str(i[8]) + '</username>\n'
        if i[9] is not None:
            message += '\t\t<stockSymbol>' + str(i[9]) + '</stockSymbol>\n'
        if i[6] is not None:
            try:
                message += '\t\t<price>' + '{:.2f}'.format(round((float(i[6]) / 100.0), 2)) + '</price>\n'
            except (TypeError, ValueError) as error:
                message += '\t\t<price>' + str(i[6]) + '</price>\n'
        if i[10] is not None:
            try:
                message += '\t\t<funds>' + '{:.2f}'.format(round((float(i[10]) / 100.0), 2)) + '</funds>\n'
            except (TypeError, ValueError) as error:
                message += '\t\t<funds>' + str(i[10]) + '</funds>\n'
        if i[11] is not None:
            message += '\t\t<quoteServerTime>' + str(i[11]) + '</quoteServerTime>\n'
        if i[12] is not None:
            message += '\t\t<cryptokey>' + str(i[12]) + '</cryptokey>\n'
        if i[13] is not None:
            message += '\t\t<filename>' + str(i[13]) + '</filename>\n'
        if i[14] is not None:
            message += '\t\t<errorMessage>' + str(i[14]) + '</errorMessage>\n'
        if i[15] is not None:
            message += '\t\t<debugMessage>' + str(i[15]) + '</debugMessage>\n'
        message += '\t</' + i[1] + '>\n'
        message = message.encode()
        client_socket.sendall(message)
    message = '\n</log>\n'
    message = message.encode()
    client_socket.sendall(message)

    '''
    output = open(filename, 'wt')
    output.write('<?xml version="1.0"?>\n<log>\n\n')
    for i in all_entries:
        output.write('\t<' + i[1] + '>\n')
        output.write('\t\t<timestamp>' + str(i[2]) + '</timestamp>\n')
        output.write('\t\t<server>' + i[3] + '</server>\n')
        output.write('\t\t<transactionNum>' + str(i[4]) + '</transactionNum>\n')
        if i[5] is not None:
            output.write('\t\t<command>' + str(i[5]) + '</command>\n')
        if i[7] is not None:
            output.write('\t\t<action>' + str(i[7]) + '</action>\n')
        if i[8] is not None:
            output.write('\t\t<username>' + str(i[8]) + '</username>\n')
        if i[9] is not None:
            output.write('\t\t<stockSymbol>' + str(i[9]) + '</stockSymbol>\n')
        if i[6] is not None:
            output.write('\t\t<price>' + '{:.2f}'.format(round((i[6]/100.0),2)) + '</price>\n')
        if i[10] is not None:
            output.write('\t\t<funds>' + '{:.2f}'.format(round((i[10]/100.0),2)) + '</funds>\n')
        if i[11] is not None:
            output.write('\t\t<quoteServerTime>' + str(i[11]) + '</quoteServerTime>\n')
        if i[12] is not None:
            output.write('\t\t<cryptokey>' + str(i[12]) + '</cryptokey>\n')
        if i[13] is not None:
            output.write('\t\t<filename>' + str(i[13]) + '</filename>\n')
        if i[14] is not None:
            output.write('\t\t<errorMessage>' + str(i[14]) + '</errorMessage>\n')
        if i[15] is not None:
            output.write('\t\t<debugMessage>' + str(i[15]) + '</debugMessage>\n')
        output.write('\t</' + i[1] + '>\n')
    output.write('\n</log>\n')
    output.close()
    '''



