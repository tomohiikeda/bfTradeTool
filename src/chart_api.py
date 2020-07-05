import cryptowatch_api_wrapper
import time
import pprint

class ChartApi:

    def __init__(self):
        self.cw = cryptowatch_api_wrapper.CryptoWatchAPIWrapper('bitflyer', 'btcfxjpy')

    def get_price(self):
        print(self.cw.get_price())

    def get_200ma_1h(self):
        return self.get_moving_average(60 * 60 * 1, 200)

    def get_200ma_2h(self):
        return self.get_moving_average(60 * 60 * 2, 200)

    def get_200ma_4h(self):
        return self.get_moving_average(60 * 60 * 4, 200)

    def get_moving_average(self, periods, size):
        before = int(time.time())
        resp = self.cw.get_ohlc(periods, before - periods * size, before)['result'][str(periods)]
        sum = 0
        for ohlc in resp:
            sum += ohlc[4]
        return sum / len(resp)