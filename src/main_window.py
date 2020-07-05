import sys
from PyQt5 import QtCore, QtWidgets, uic
import os
import trade_api
import chart_api
import algo
import pyperclip

class MainWindow:

    def __init__(self):
        self.trade = trade_api.TradeApi()
        self.chart = chart_api.ChartApi()
        self.algo = algo.Algo(self.trade, self.chart)

    def init(self):
        ui_path = os.path.dirname(os.path.abspath(__file__))
        Form, Window = uic.loadUiType(os.path.join(ui_path, "main_window.ui"))
        app = QtWidgets.QApplication([])
        window = Window()
        self.form = Form()
        self.form.setupUi(window)
        window.show()

        # UI初期設定
        self.__update_current_position()
        self.__update_ltp()
        self.form.plainTextEdit_size.setPlainText('0.5')
        self.form.plainTextEdit_price.setPlainText('0')
        self.form.plainTextEdit_offset.setPlainText('1000')
        self.form.plainTextEdit_stop_offset.setPlainText('2000')

        # 1sec間隔のTimer
        timer_0 = QtCore.QTimer()
        timer_0.setInterval(1000)
        timer_0.timeout.connect(self.__update_ltp)
        timer_0.start()

        # 60sec間隔のTimer
        timer_1 = QtCore.QTimer()
        timer_1.setInterval(60000)
        timer_1.timeout.connect(self.__update_current_position)
        timer_1.start()

        # ハンドラ登録
        self.form.pushButton_Buy.clicked.connect(self.__on_clicked_buy)
        self.form.pushButton_Sell.clicked.connect(self.__on_clicked_sell)
        
        self.form.radioButton_market.clicked.connect(self.__on_clicked_order_type)
        self.form.radioButton_limit.clicked.connect(self.__on_clicked_order_type)
        self.form.radioButton_limit_stop.clicked.connect(self.__on_clicked_order_type)
        self.form.radioButton_ltpoffset.clicked.connect(self.__on_clicked_order_type)
        self.form.radioButton_ltpoffset_stop.clicked.connect(self.__on_clicked_order_type)
        self.form.radioButton_stop.clicked.connect(self.__on_clicked_order_type)

        self.form.pushButton_update.clicked.connect(self.__update_current_position)
        self.form.pushButton_runbot.clicked.connect(self.algo.start)
        self.form.pushButton_cancel.clicked.connect(self.trade.cancel_all_orders)

        self.form.pushButton_copy_ltp_plus_2000.clicked.connect(self.__on_clicked_copy_lpt_plus_2000)
        self.form.pushButton_copy_ltp_plus_1000.clicked.connect(self.__on_clicked_copy_lpt_plus_1000)
        self.form.pushButton_copy_cur_ltp.clicked.connect(self.__on_clicked_copy_lpt)
        self.form.pushButton_copy_ltp_minus_1000.clicked.connect(self.__on_clicked_copy_lpt_minus_1000)
        self.form.pushButton_copy_ltp_minus_2000.clicked.connect(self.__on_clicked_copy_lpt_minus_2000)
        self.form.pushButton_copy_even.clicked.connect(self.__on_clicked_copy_even)

        sys.exit(app.exec_())

    def __update_ltp(self):
        ltp = self.trade.get_ltp()
        break_even_price = float(self.form.label_break_even_price.text().replace(',', ''))
        size = float(self.form.label_cur_position_size.text().replace(',', ''))
        cur_side = self.form.label_cur_side.text()
        if cur_side == '-':
            unrealized_gain = 0
        elif cur_side == 'L':
            unrealized_gain = (ltp - break_even_price) * size
        else:
            unrealized_gain = (break_even_price - ltp) * size
        self.form.label_ltp.setText('{:,.0f}'.format(ltp))
        self.form.label_unrealized_gain.setText('{:,.0f}'.format(unrealized_gain))
        return

    def __update_current_position(self):
        position_size = self.trade.get_positions_size()
        total_swap = self.trade.get_total_swap_point()
        average_price = self.trade.get_average_contract_price()
        break_even_price = average_price - total_swap
        self.form.label_cur_side.setText(self.trade.get_cur_side())
        self.form.label_cur_position_size.setText('{:.2f}'.format(position_size))
        self.form.label_cur_total_swap.setText('{:,.0f}'.format(total_swap))
        self.form.label_average_contract_price.setText('{:,.0f}'.format(average_price))
        self.form.label_break_even_price.setText('{:,.0f}'.format(break_even_price))
        return

    def __on_clicked_buy(self):
        size = float(self.form.plainTextEdit_size.toPlainText())
        price = float(self.form.plainTextEdit_price.toPlainText())
        offset = float(self.form.plainTextEdit_offset.toPlainText())
        ltp = float(self.form.label_ltp.text().replace(',', ''))
        stop_offset = float(self.form.plainTextEdit_stop_offset.toPlainText())
        if self.form.radioButton_market.isChecked():
            self.trade.buy_market(size)
        elif self.form.radioButton_limit.isChecked():
            self.trade.buy_limit(price, size)
        elif self.form.radioButton_limit_stop.isChecked():
            self.trade.buy_limit_with_stop(price, size, price - stop_offset)
        elif self.form.radioButton_ltpoffset.isChecked():
            self.trade.buy_limit(ltp - offset, size)
        elif self.form.radioButton_ltpoffset_stop.isChecked():
            self.trade.buy_limit_with_stop(ltp - offset, size, ltp - offset - stop_offset)
        elif self.form.radioButton_stop.isChecked():
            self.trade.stop_order('BUY', price, size)

    def __on_clicked_sell(self):
        size = float(self.form.plainTextEdit_size.toPlainText())
        price = float(self.form.plainTextEdit_price.toPlainText())
        offset = float(self.form.plainTextEdit_offset.toPlainText())
        ltp = float(self.form.label_ltp.text().replace(',', ''))
        stop_offset = float(self.form.plainTextEdit_stop_offset.toPlainText())
        if self.form.radioButton_market.isChecked():
            self.trade.sell_market(size)
        elif self.form.radioButton_limit.isChecked():
            self.trade.sell_limit(price, size)
        elif self.form.radioButton_limit_stop.isChecked():
            self.trade.sell_limit_with_stop(price, size, price + stop_offset)
        elif self.form.radioButton_ltpoffset.isChecked():
            self.trade.sell_limit(ltp + offset, size)
        elif self.form.radioButton_ltpoffset_stop.isChecked():
            self.trade.sell_limit_with_stop(ltp + offset, size, ltp + offset + stop_offset)
        elif self.form.radioButton_stop.isChecked():
            self.trade.stop_order('SELL', price, size)

    def __on_clicked_order_type(self):
        if self.form.radioButton_market.isChecked():
            self.form.plainTextEdit_price.setEnabled(False)
            self.form.plainTextEdit_offset.setEnabled(False)
            self.form.plainTextEdit_stop_offset.setEnabled(False)
        elif self.form.radioButton_limit.isChecked():
            self.form.plainTextEdit_price.setEnabled(True)
            self.form.plainTextEdit_offset.setEnabled(False)
            self.form.plainTextEdit_stop_offset.setEnabled(False)
        elif self.form.radioButton_limit_stop.isChecked():
            self.form.plainTextEdit_price.setEnabled(True)
            self.form.plainTextEdit_offset.setEnabled(False)
            self.form.plainTextEdit_stop_offset.setEnabled(True)
        elif self.form.radioButton_ltpoffset.isChecked():
            self.form.plainTextEdit_price.setEnabled(False)
            self.form.plainTextEdit_offset.setEnabled(True)
            self.form.plainTextEdit_stop_offset.setEnabled(False)
        elif self.form.radioButton_ltpoffset_stop.isChecked():
            self.form.plainTextEdit_price.setEnabled(False)
            self.form.plainTextEdit_offset.setEnabled(True)
            self.form.plainTextEdit_stop_offset.setEnabled(True)
        elif self.form.radioButton_stop.isChecked():
            self.form.plainTextEdit_price.setEnabled(True)
            self.form.plainTextEdit_offset.setEnabled(False)
            self.form.plainTextEdit_stop_offset.setEnabled(False)
        return

    def __on_clicked_copy_lpt(self):
        self.__copy_clipboard_lpt_offset(0)

    def __on_clicked_copy_lpt_plus_1000(self):
        self.__copy_clipboard_lpt_offset(1000)
    
    def __on_clicked_copy_lpt_plus_2000(self):
        self.__copy_clipboard_lpt_offset(2000)

    def __on_clicked_copy_lpt_minus_1000(self):
        self.__copy_clipboard_lpt_offset(-1000)

    def __on_clicked_copy_lpt_minus_2000(self):
        self.__copy_clipboard_lpt_offset(-2000)

    def __on_clicked_copy_even(self):
        position_size = self.form.label_cur_position_size.text().replace(',', '')
        break_even_price = self.form.label_break_even_price.text().replace(',', '')
        self.form.plainTextEdit_size.setPlainText(position_size)
        self.form.plainTextEdit_price.setPlainText(break_even_price)

    def __copy_clipboard_lpt_offset(self, offset):
        ltp = float(self.form.label_ltp.text().replace(',', ''))
        copy_price = '{:.0f}'.format(ltp+offset)
        pyperclip.copy(copy_price)
        self.form.plainTextEdit_price.setPlainText(copy_price)
