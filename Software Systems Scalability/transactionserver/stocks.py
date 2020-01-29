class stocks:
    def __init__(self, stock_name, accessible, reserved, buy_trigger, buy_amount, sell_trigger, sell_amount, bt_t_num,
                 st_t_num):
        self.stock_name = stock_name
        self.accessible = accessible
        self.reserved = reserved
        self.buy_trigger = buy_trigger
        self.buy_amount = buy_amount
        self.sell_trigger = sell_trigger
        self.sell_amount = sell_amount
        self.bt_t_num = bt_t_num
        self.st_t_num = st_t_num

    def get_num_stocks(self):
        return (self.accessible, self.reserved)

    def get_num_reserved_stocks(self):
        return (self.reserved)

    def set_num_stocks(self, accessible, reserved):
        self.accessible = accessible
        self.reserved = reserved

    def set_num_reserved_stocks(self, reserved):
        self.reserved = reserved

    def get_buy_trigger(self):
        return self.buy_trigger

    def get_buy_amount(self):
        return self.buy_amount

    def set_buy_trigger_and_bt_tnum(self, buy_trigger, t_num):
        self.buy_trigger = buy_trigger
        self.bt_t_num = t_num

    def get_buy_trigger_and_amount(self):
        return (self.buy_trigger, self.buy_amount)

    def set_buy_amount(self, buy_amount):
        self.buy_amount = buy_amount

    def clear_buy_trigger(self):
        self.buy_amount = None
        self.buy_trigger = None
        self.bt_t_num = None

    def get_accessible_stocks(self):
        return self.accessible

    def set_accessible_stocks(self, amount):
        self.accessible = amount

    def get_sell_amount_data(self):
        return (self.accessible, self.reserved, self.sell_amount, self.sell_trigger)

    def set_sell_amount_data(self, accessible, reserved, sell_amount):
        self.accessible = accessible
        self.reserved = reserved
        self.sell_amount = sell_amount

    def set_sell_amount(self, sell_amount):
        self.sell_amount = sell_amount

    def get_sell_trigger_and_amount(self):
        return (self.sell_trigger, self.sell_amount)

    def set_sell_trigger_data(self, accessible, reserved, trigger, amount, t_num):
        self.accessible = accessible
        self.reserved = reserved
        self.sell_trigger = trigger
        self.sell_amount = amount
        self.st_t_num = t_num

    def clear_sell_trigger(self):
        self.sell_amount = None
        self.sell_trigger = None
        self.st_t_num = None

    def get_buy_trigger_info(self):
        #stock_symbol, t_num, trigger, cent_amount
        return (self.stock_name, self.bt_t_num, self.buy_trigger, self.buy_amount)

    def get_sell_trigger_info(self):
        #stock_symbol, t_num, trigger, cent_amount
        return (self.stock_name, self.st_t_num, self.sell_trigger, self.sell_amount)

    def get_all(self):
        return (self.stock_name, self.accessible, self.reserved, self.buy_trigger, self.buy_amount, self.sell_trigger,
                self.sell_amount, self.bt_t_num, self.st_t_num)
