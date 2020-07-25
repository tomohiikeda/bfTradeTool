import cryptowatch_api_wrapper
import time
import pandas as pd
import mplfinance as mpf

class ChartApi:

    def __init__(self):
        self.cw = cryptowatch_api_wrapper.CryptoWatchAPIWrapper('bitflyer', 'btcfxjpy')

    def get_current_price(self):
        return self.cw.get_current_price()

    def get_close_price(self, time, periods):
        return self.cw.get_close_price(time, periods)

    def get_200ma_1h(self, current_time):
        return self.get_moving_average(current_time, 60 * 60 * 1, 200)

    def get_75ma_1h(self, current_time):
        return self.get_moving_average(current_time, 60 * 60 * 1, 75)

    def get_9ma_1h(self, current_time):
        return self.get_moving_average(current_time, 60 * 60 * 1, 9)

    def get_200ma_2h(self, current_time):
        return self.get_moving_average(current_time, 60 * 60 * 2, 200)

    def get_75ma_2h(self, current_time):
        return self.get_moving_average(current_time, 60 * 60 * 2, 75)

    def get_9ma_2h(self, current_time):
        return self.get_moving_average(current_time, 60 * 60 * 2, 9)

    def get_200ma_4h(self, current_time):
        return self.get_moving_average(current_time, 60 * 60 * 4, 200)

    def get_75ma_4h(self, current_time):
        return self.get_moving_average(current_time, 60 * 60 * 4, 75)

    def get_9ma_4h(self, current_time):
        return self.get_moving_average(current_time, 60 * 60 * 4, 9)

    def get_moving_average(self, current_time, periods, size):
        before = current_time
        resp = self.cw.get_ohlc(periods, before - periods * size, before)['result'][str(periods)]
        sum = 0
        for ohlc in resp:
            sum += ohlc[4]
        return sum / len(resp)

    #
    # 過去の期間内の最高値と最安値を取得する
    # periods: 足の種類
    # size: 足いくつ分までか
    #
    def get_highest_lowest_price(self, periods, size):
        before = int(time.time())
        resp = self.cw.get_ohlc(periods, before - periods * size, before)['result'][str(periods)]
        highest = 0
        lowest = 99999999
        for ohlc in resp:
            if ohlc[2] > highest:
                highest = ohlc[2]
            if ohlc[3] < lowest:
                lowest = ohlc[3]
        return highest, lowest

    def print_candle_chart(self, periods, size):
        before = int(time.time())
        data = self.cw.get_ohlc(periods, before - periods * size, before)['result'][str(periods)]
        col = ['time', 'Open', 'High', 'Low', 'Close', 'Volume', 'trade_value']
        df = pd.DataFrame(data, columns=col)
        df = df.set_index('time')
        df.index = pd.to_datetime(df.index, unit='s')
        mpf.plot(df, type='candle', volume=True, mav=(9,75,200))
