import pprint
import requests
import hashlib
import hmac
import time
import urllib
import json

class CryptoWatchAPIWrapper:

    __url_base = 'https://api.cryptowat.ch/markets/'

    def __init__(self, markets, pair):
        self.markets = markets
        self.pair = pair
        return

    def get_ohlc(self, periods, after, before):
        params = {
            'periods': str(periods),
            'after' : str(after),
            'before': str(before),
        }
        url = self.__url_base + self.markets + "/" + self.pair + "/ohlc"
        #resp = requests.get(url, params=params).json()['result']
        resp = requests.get(url, params=params).json()
        return resp

    def get_price(self):
        url = self.__url_base + self.markets + "/" + self.pair + "/price"
        return requests.get(url).json()
