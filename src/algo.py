from threading import Timer
import time
import threading
import winsound
from enum import Enum
import datetime
import sys
class Position(Enum):
    Non = 1
    Long = 2
    Short = 3

class Algo:

    #
    # コンストラクタ
    #
    def __init__(self, trade, chart):
        self.trade = trade
        self.chart = chart
        self.__position = Position.Non
        self.__pos_price = 0
        return

    #
    # アルゴ開始
    # mode: 'sim' シミュレーションモード開始
    #       その他 本番開始
    #
    def start(self, mode):
        if mode == 'SIM':
            self.__sim_start()
        else:
            self.__trade_start()

    #
    # シミュレーションモード開始
    #
    def __sim_start(self):
        print('BackTest Start:')
        self.chart.print_candle_chart(60*60, 1000)
        #cur_datetime = datetime.datetime(2020,1,1,0,0,0)
        #cur_datetime = datetime.datetime(2020,1,11,5,0,0)
        #while True:
        #    self.__tick(int(cur_datetime.timestamp()))
        #    cur_datetime += datetime.timedelta(hours=1)

    #
    # 本番開始
    #
    def __trade_start(self):
        current_time = int(time.time())
        print('Trade Start:', current_time)

    #
    # 一定時間で処理する関数
    #
    def __tick(self, current_time):
        print('--------------------------------------')
        print(datetime.datetime.fromtimestamp(current_time))
        print('Cuurent Position = ', self.__position)
        print('Position Price = ', self.__pos_price)
        if self.__position == Position.Non:
            self.__check_position_signal(current_time)
        else:
            self.__check_settle_signal(current_time)

    #
    # @brief 1時間足の移動平均を取得する関数
    # @param current_time 基準時間
    # @return 基準時間前の9MA、75MA、200MA
    #
    def __get_ma_9_75_200(self, current_time):
        ma_9 = self.chart.get_9ma_1h(current_time)
        ma_75 = self.chart.get_75ma_1h(current_time)
        ma_200 = self.chart.get_200ma_1h(current_time)
        print('9MA = ', ma_9)
        print('75MA = ', ma_75)
        print('200MA = ', ma_200)
        return ma_9, ma_75, ma_200

    def __check_position_signal(self, current_time):
        print('check_position_signal')
        ma_9, ma_75, ma_200 = self.__get_ma_9_75_200(current_time)
        if self.__check_buy_signal(ma_9, ma_75, ma_200):
            self.__buy()
            self.__pos_price = self.chart.get_close_price(current_time, 60 * 60)
            self.__position = Position.Long
        elif self.__check_sell_signal(ma_9, ma_75, ma_200):
            self.__sell()
            self.__pos_price = self.chart.get_close_price(current_time, 60 * 60)
            self.__position = Position.Short
        self.__pre_ma_9 = ma_9

    def __check_buy_signal(self, ma_9, ma_75, ma_200):
        if ma_200 < ma_9 and \
           ma_200 < ma_75 and \
           ma_75 < ma_9 and \
           self.__pre_ma_9 < ma_75 and \
           self.__position == Position.Non:
           return True
        else:
           return False

    def __check_sell_signal(self, ma_9, ma_75, ma_200):
        if ma_200 > ma_9 and \
           ma_200 > ma_75 and \
           ma_75 > ma_9 and \
           self.__pre_ma_9 > ma_75 and \
           self.__position == Position.Non:
           return True
        else:
            return False

    def __check_settle_signal(self, current_time):
        current_close_price = self.chart.get_close_price(current_time, 60 * 60)
        if current_close_price > self.__pos_price + 3000:
            return True
        elif current_close_price < self.__pos_price - 3000:
            return True
        else:
            return False

    def __buy(self):
        print('buy')
        winsound.Beep(400,1)

    def __sell(self):
        print('sell')
        winsound.Beep(400,1)
        self.__position = Position.Short

    def __settle(self):
        if (self.__position == Position.Long):
            self.__sell
        
        self.__position = Position.Non
        self.__pos_price = 0
        print('settle')

