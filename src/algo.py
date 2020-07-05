from threading import Timer
import time
import threading
import winsound

class Algo:

    def __init__(self, trade, chart):
        self.trade = trade
        self.chart = chart
        return
    
    def start(self):
        t = threading.Timer(1, self.__loop)
        t.start()

    def __loop(self):
        while True:
            winsound.Beep(880, 500)
            print(self.trade.get_ltp())
            print(self.chart.get_200ma_1h())
            print(self.chart.get_200ma_2h())
            print(self.chart.get_200ma_4h())
            time.sleep(60)

    def __check_buy_signal(self):
        return False

    def __check_sell_signal(self):
        return False