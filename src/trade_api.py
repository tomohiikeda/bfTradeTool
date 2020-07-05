import bitflyer_api_wrapper as bfapi

class TradeApi:

    def __init__(self):
        self.bf = bfapi.BitflyerAPIWrapper()

    def buy_market(self, size):
        self.__order('MARKET', 'BUY', 0, size)

    def buy_limit(self, price, size):
        self.__order('LIMIT', 'BUY', price, size)

    def buy_limit_with_stop(self, price, size, stop_price):
        self.bf.send_parentorders_ifd_stop('BUY', price, size, stop_price)

    def sell_market(self, size):
        self.__order('MARKET', 'SELL', 0, size)

    def sell_limit(self, price, size):
        self.__order('LIMIT', 'SELL', price, size)

    def sell_limit_with_stop(self, price, size, stop_price):
        self.bf.send_parentorders_ifd_stop('SELL', price, size, stop_price)

    def __order(self, order_type, side, price, size):
        ltp = self.get_ltp()
        if order_type == 'LIMIT':
            if side == 'BUY' and price > ltp:
                print('price > ltp')
                return
            elif side == 'SELL' and price < ltp:
                print('price < ltp')
                return
        self.bf.send_childorders(order_type, side, price, size)

    def stop_order(self, side, price, size):
        ltp = self.get_ltp()
        if side == 'BUY' and price < ltp:
            print('price < ltp')
            return
        elif side == 'SELL' and price > ltp:
            print('price > ltp')
            return
        self.bf.send_parentorders_simple_stop(side, price, size)

    def cancel_all_orders(self):
        self.bf.cancel_all_child_orders()

    def get_ltp(self):
        return self.bf.get_ticker()['ltp']

    def get_cur_side(self):
        cur_positions = self.bf.get_positions()
        if len(cur_positions) == 0 :
            return '-'
        elif cur_positions[0]['side'] == 'BUY' :
            return 'L'
        else:
            return 'S'

    def get_positions_size(self):
        cur_positions = self.bf.get_positions()
        sum = 0
        for pos in cur_positions:
            sum = sum + float(pos['size'])
        return sum

    def get_total_swap_point(self):
        cur_positions = self.bf.get_positions()
        sum = 0
        for pos in cur_positions:
            sum = sum + float(pos['swap_point_accumulate'])
        return sum

    def get_average_contract_price(self):
        cur_positions = self.bf.get_positions()
        total = self.get_positions_size()
        average = 0
        for pos in cur_positions:
            price = float(pos['price'])
            size = float(pos['size'])
            average = average + (price * size / total)
        return average
