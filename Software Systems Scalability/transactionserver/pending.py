class pending:


    def __init__(self, kind, stock_name, expiry, num, req_amount, stock_price, t_num):
        self.kind = kind
        self.stock_name = stock_name
        self.expiry = expiry
        self.num = num
        self.req_amount = req_amount
        self.stock_price = stock_price
        self.t_num = t_num

    def get_symbol(self):
        return self.stock_name

    def get_expiry(self):
        return self.expiry

    def get_essentials(self):
        return (self.stock_name, self.t_num, self.req_amount, self.num)

    def get_all(self):
        return (self.stock_name, self.stock_price, self.num, self.expiry, self.req_amount, self.t_num)

    def get_commit_sell(self):
        return (self.stock_name, self.stock_price, self.num, self.expiry)

    def get_req_amount(self):
        return self.req_amount

    def get_symbol_and_num(self):
        return(self.stock_name, self.num)

    def refresh(self, expiry, num, quote):
        self.expiry = expiry
        self.num = num
        self.stock_price = quote
