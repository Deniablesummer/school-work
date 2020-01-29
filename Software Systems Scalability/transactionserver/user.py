import mysql.connector
import pending
import stocks

class user:
    def __init__(self, userid, db):

        # user table info
        self.userid = userid
        self.pending_buys = []
        self.pending_sells = []
        self.stocks = {}

        mycursor = db.cursor(buffered=True)

        # --- user data ------------------------------------------------------------------------------------------------
        sql = 'SELECT accessible_money, reserved_money FROM users WHERE userid = %s'
        val = (self.userid,)
        mycursor.execute(sql, val)
        data = mycursor.fetchone()  # assume this is in the form of an int

        if data is None:
            self.accessible_money = 0
            self.reserved_money = 0
            sql = 'INSERT INTO users (userid, accessible_money, reserved_money) VALUES (%s, %s, %s)'
            val = (self.userid, self.accessible_money, self.reserved_money)
            mycursor.execute(sql, val)
            db.commit()
        else:
            # from userid we pull the rest of the information
            self.accessible_money = data[0]
            self.reserved_money = data[1]

        # --- pending_buys ---------------------------------------------------------------------------------------------
        sql = 'SELECT stock_name, expiry, num, req_amount, stock_price, t_num FROM pending_buys WHERE userid = %s' \
              ' ORDER BY id'  # these are in increasing order
        val = (userid,)
        mycursor.execute(sql, val)
        data = mycursor.fetchall()

        if data is None:
            pass
        else:
            for i in data:
                self.pending_buys.append(pending.pending('buy', i[0], i[1], i[2], i[3], i[4], i[5]))  # most recent at the
                                                                                              # end of the list

        # --- pending_sells --------------------------------------------------------------------------------------------

        sql = 'SELECT stock_name, expiry, num, req_amount, stock_price, t_num FROM pending_sells WHERE userid = %s' \
              ' ORDER BY id'    # these are in increasing order
        val = (userid,)
        mycursor.execute(sql, val)
        data = mycursor.fetchall()

        if data is None:
            pass
        else:
            for i in data:
                self.pending_sells.append(pending.pending('sell', i[0], i[1], i[2], i[3], i[4], i[5]))  # most recent at the
                                                                                                # end of the list

        # --- stock_info -----------------------------------------------------------------------------------------------

        sql = 'SELECT stock_name, accessible_stocks, reserved_stocks, buy_trigger, buy_amount, sell_trigger, sell_amount, bt_t_num,' \
              ' st_t_num FROM user_stocks WHERE userid = %s'
        val = (userid,)
        mycursor.execute(sql, val)
        data = mycursor.fetchall()

        if data is None:
            pass
        else:
            for i in data:
                self.stocks[i[0]] = stocks.stocks(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])

    def get_pending_buy(self):
        if len(self.pending_buys) > 0:
            return self.pending_buys[-1]
        else:
            return None

    def get_stocks(self):
        return self.stocks

    def get_accessible_stocks(self, stock_symbol):
        try:
            return self.stocks[stock_symbol].get_accessible_stocks()
        except KeyError as error:
            return 0

    def set_accessible_stocks(self, stock_symbol, amount):
        try:
            self.stocks[stock_symbol].set_accessible_stocks(amount)
        except KeyError as error:
            self.stocks[stock_symbol] = stocks.stocks(stock_symbol, accessible, 0, 0, 0)
        return

    def get_userid(self):
        return self.userid

    def get_all(self):
        return (self.userid, self.accessible_money, self.reserved_money,
                self.pending_buys, self.pending_sells, self.stocks)

    def get_pending_sell(self):
        if len(self.pending_sells) > 0:
            return self.pending_sells[-1]
        else:
            return None

    def get_stock_info(self, stock_symbol):
        try:
            return self.stocks[stock_symbol]
        except KeyError as error:
# self.stock_name, self.accessible, self.reserved, self.buy_trigger, self.buy_amount, self.sell_trigger, self.sell_amount, self.bt_t_num, self.st_t_num
            return None

    def remove_pending_sell(self):
        if len(self.pending_sells) > 0:
            self.pending_sells.pop()
        else:
            print('No pending sell to remove from list')
            return

    def remove_pending_buy(self):
        if len(self.pending_buys) > 0:
            self.pending_buys.pop()
        else:
            print('No pending buy to remove from list')
            return

    def get_num_stocks(self, stock_symbol):
        return self.stocks[stock_symbol].get_num_stocks()

    def set_num_stocks(self, stock_symbol, accessible, reserved):
        self.stocks[stock_symbol].set_num_stocks(accessible, reserved)
        return

    def clear_sell_trigger(self, stock_symbol):
        self.stocks[stock_symbol].clear_sell_trigger()


    def get_money(self):
        return (self.accessible_money, self.reserved_money)

    def get_accessible_money(self):
        return self.accessible_money

    def clear_buy_trigger(self, stock_symbol):
        self.stocks[stock_symbol].clear_buy_trigger()

    def set_accessible_money(self, amount):
        self.accessible_money = amount

    def set_money(self, accessible, reserved):
        self.accessible_money = accessible
        self.reserved_money = reserved

    def add_pending_buy(self,stock_symbol, num_stocks, expiry, quote, cent_amount, t_num):
        self.pending_buys.append(pending.pending('buy', stock_symbol, expiry, num_stocks, cent_amount, quote, t_num))

    def add_stock(self, stock_name, accessible, reserved=0, buy_trigger=None, buy_amount=None, sell_trigger=None,
                  sell_amount=None, bt_t_num=None, st_t_num=None):
        self.stocks[stock_name] = stocks.stocks(stock_name, accessible, reserved, buy_trigger, buy_amount, sell_trigger,
                                         sell_amount, bt_t_num, st_t_num)

    def add_pending_sell(self, stock_symbol, num_stocks, expiry, quote, cent_amount, t_num):
        self.pending_sells.append(pending.pending('sell', stock_symbol, expiry, num_stocks, cent_amount, quote, t_num))

    #TODO: make this smarter instead of deleting all and updating should
    def sync_user(self, db):
        mycursor = db.cursor(buffered=True)
        userid = self.userid
        current_entries = []

        # --- sync user table ------------------------------------------------------------------------------------------
        sql = 'UPDATE users SET accessible_money = %s, reserved_money = %s WHERE userid = %s'
        val = (self.accessible_money, self.reserved_money, self.userid)
        mycursor.execute(sql,val)

        # currently erase and rewrite values, faster to do update, but needs to be thought out
        # --- pending buys and sells------------------------------------------------------------------------------------
        sql = 'SELECT stock_name, stock_price, num, expiry, req_amount, t_num FROM pending_buys WHERE userid = %s'
        val = (userid,)
        mycursor.execute(sql, val)
        existing_entries = mycursor.fetchall()

        for i in self.pending_buys:
            current_entries.append(i.get_all())

        for i in current_entries:
            code = [1, 1, 1, 1, 1]
            stock_name_new, stock_price_new, num_new, expiry_new, req_amount_new, t_num_new = i
            current_entry = None
            broke = False
            for j in range(len(existing_entries)):
                if stock_name_new == existing_entries[j][0]:
                    current_entry = existing_entries.pop(j)
                    broke = True
                    break
                else:
                    pass
            if broke:
                stock_name_old, stock_price_old, num_old, expiry_old, req_amount_old, t_num_old = current_entry
                if stock_price_old == stock_price_new:
                    code[0] = 0
                if num_old == num_new:
                    code[1] = 0
                if expiry_old == expiry_new:
                    code[2] = 0
                if req_amount_old == req_amount_new:
                    code[3] = 0
                if t_num_old == t_num_new:
                    code[4] = 0

                if (code[0] == 0) and (code[1] == 0) and (code[2] == 0) and (code[3] == 0) and (code[4] == 0):
                    # no update needed
                    pass
                else:
                    sql = 'UPDATE pending_buys SET '
                    val = []
                    if code[0] == 1:
                        sql += 'stock_price = %s, '
                        val.append(stock_price_new)

                    if code[1] == 1:
                        sql += 'num = %s, '
                        val.append(num_new)

                    if code[2] == 1:
                        sql += 'expiry = %s, '
                        val.append(expiry_new)

                    if code[3] == 1:
                        sql += 'req_amount = %s, '
                        val.append(req_amount_new)

                    if code[4] == 1:
                        sql += 't_num = %s, '
                        val.append(t_num_new)

                    sql = sql.rstrip(', ')

                    sql += ' WHERE userid = %s AND stock_name = %s'
                    val.append(userid)
                    val.append(stock_name_new)
                    mycursor.execute(sql, val)


            else:
                sql = 'INSERT INTO pending_buys (userid, stock_name, expiry, num, req_amount, stock_price, t_num) ' \
                      'VALUES (%s, %s, %s, %s, %s, %s, %s)'
                val = (userid, stock_name_new, expiry_new, num_new, req_amount_new, stock_price_new, t_num_new)
                mycursor.execute(sql, val)

        for i in existing_entries:
            sql = 'DELETE FROM pending_buys WHERE userid = %s and stock_name = %s'
            val = (userid, i[0])
            mycursor.execute(sql, val)
        db.commit()

        current_entries = []

        sql = 'SELECT stock_name, stock_price, num, expiry, req_amount, t_num FROM pending_sells WHERE userid = %s'
        val = (userid,)
        mycursor.execute(sql, val)
        existing_entries = mycursor.fetchall()

        for i in self.pending_sells:
            current_entries.append(i.get_all())

        for i in current_entries:
            code = [1, 1, 1, 1, 1]
            stock_name_new, stock_price_new, num_new, expiry_new, req_amount_new, t_num_new = i
            current_entry = None
            broke = False
            for j in range(len(existing_entries)):
                if stock_name_new == existing_entries[j][0]:
                    current_entry = existing_entries.pop(j)
                    broke = True
                    break
                else:
                    pass
            if broke:
                stock_name_old, stock_price_old, num_old, expiry_old, req_amount_old, t_num_old = current_entry
                if stock_price_old == stock_price_new:
                    code[0] = 0
                if num_old == num_new:
                    code[1] = 0
                if expiry_old == expiry_new:
                    code[2] = 0
                if req_amount_old == req_amount_new:
                    code[3] = 0
                if t_num_old == t_num_new:
                    code[4] = 0

                if (code[0] == 0) and (code[1] == 0) and (code[2] == 0) and (code[3] == 0) and (code[4] == 0):
                    # no update needed
                    pass
                else:
                    sql = 'UPDATE pending_sells SET '
                    val = []
                    if code[0] == 1:
                        sql += 'stock_price = %s, '
                        val.append(stock_price_new)

                    if code[1] == 1:
                        sql += 'num = %s, '
                        val.append(num_new)

                    if code[2] == 1:
                        sql += 'expiry = %s, '
                        val.append(expiry_new)

                    if code[3] == 1:
                        sql += 'req_amount = %s, '
                        val.append(req_amount_new)

                    if code[4] == 1:
                        sql += 't_num = %s, '
                        val.append(t_num_new)

                    sql = sql.rstrip(', ')

                    sql += ' WHERE userid = %s AND stock_name = %s'
                    val.append(userid)
                    val.append(stock_name_new)
                    mycursor.execute(sql, val)


            else:
                sql = 'INSERT INTO pending_sells (userid, stock_name, expiry, num, req_amount, stock_price, t_num) ' \
                      'VALUES (%s, %s, %s, %s, %s, %s, %s)'
                val = (userid, stock_name_new, expiry_new, num_new, req_amount_new, stock_price_new, t_num_new)
                mycursor.execute(sql, val)

        for i in existing_entries:
            sql = 'DELETE FROM pending_sells WHERE userid = %s and stock_name = %s'
            val = (userid, i[0])
            mycursor.execute(sql, val)
        db.commit()


        current_entries = []

        sql = 'SELECT stock_name, accessible_stocks, reserved_stocks, buy_trigger, buy_amount, sell_trigger, ' \
              'sell_amount, bt_t_num, st_t_num FROM user_stocks WHERE userid = %s'
        val = (userid,)
        mycursor.execute(sql, val)
        existing_entries = mycursor.fetchall()

        stocks = self.stocks

        for i in stocks:
            # stock_name, accessible, reserved, buy_trigger, buy_amount, sell_trigger, sell_amount, bt_t_num, st_t_num
            current_entries.append(stocks[i].get_all())

        for i in current_entries:
            code = [1, 1, 1, 1, 1, 1, 1, 1, 1]
            stock_name_new, accessible_new, reserved_new, buy_trigger_new, buy_amount_new, sell_trigger_new, \
            sell_amount_new, bt_t_num_new, st_t_num_new = i
            current_entry = None
            broke = False
            for j in range(len(existing_entries)):
                if stock_name_new == existing_entries[j][0]:
                    current_entry = existing_entries.pop(j)
                    broke = True
                    break
                else:
                    pass
            if broke:
                stock_name_old, accessible_stocks_old, reserved_stocks_old, buy_trigger_old, buy_amount_old, \
                sell_trigger_old, sell_amount_old, bt_t_num_old, st_t_num_old = current_entry

                if accessible_stocks_old == accessible_new:
                    code[0] = 0
                if reserved_stocks_old == reserved_new:
                    code[1] = 0
                if buy_trigger_old == buy_trigger_new:
                    code[2] = 0
                if buy_amount_old == buy_amount_new:
                    code[3] = 0
                if sell_trigger_old == sell_trigger_new:
                    code[4] = 0
                if sell_amount_old == sell_amount_new:
                    code[5] = 0
                if bt_t_num_old == bt_t_num_new:
                    code[6] = 0
                if st_t_num_old == st_t_num_new:
                    code[7] = 0

                if (code[0] == 0) and (code[1] == 0) and (code[2] == 0) and (code[3] == 0) and (code[4] == 0) and \
                        (code[5] == 0) and (code[6] == 0) and (code[7] == 0):
                    # no update needed
                    pass
                else:
                    sql = 'UPDATE user_stocks SET '
                    val = []

                    if code[0] == 1:
                        sql += 'accessible_stocks = %s, '
                        val.append(accessible_new)

                    if code[1] == 1:
                        sql += 'reserved_stocks = %s, '
                        val.append(reserved_new)

                    if code[2] == 1:
                        sql += 'buy_trigger = %s, '
                        val.append(buy_trigger_new)

                    if code[3] == 1:
                        sql += 'buy_amount = %s, '
                        val.append(buy_amount_new)

                    if code[4] == 1:
                        sql += 'sell_trigger = %s, '
                        val.append(sell_trigger_new)

                    if code[5] == 1:
                        sql += 'sell_amount = %s, '
                        val.append(sell_amount_new)

                    if code[6] == 1:
                        sql += 'bt_t_num = %s, '
                        val.append(bt_t_num_new)

                    if code[7] == 1:
                        sql += 'st_t_num = %s, '
                        val.append(st_t_num_new)

                    sql = sql.rstrip(', ')

                    sql += ' WHERE userid = %s AND stock_name = %s'
                    val.append(userid)
                    val.append(stock_name_new)
                    mycursor.execute(sql, val)


            else:
                sql = 'INSERT INTO user_stocks (userid, stock_name, accessible_stocks, reserved_stocks, buy_trigger, ' \
                      'buy_amount, sell_trigger, sell_amount, bt_t_num, st_t_num)  VALUES (%s, %s, %s, %s, %s, %s, %s, ' \
                      '%s, %s, %s)'
                val = (userid, stock_name_new, accessible_new, reserved_new, buy_trigger_new, buy_amount_new,
                       sell_trigger_new, sell_amount_new, bt_t_num_new, st_t_num_new)
                mycursor.execute(sql, val)

        for i in existing_entries:
            sql = 'DELETE FROM user_stocks WHERE userid = %s and stock_name = %s'
            val = (userid, i[0])
            mycursor.execute(sql, val)
        db.commit()

        return








