import pprint
import hashlib
import hmac
import time
import urllib
import json
import http_requester

#https://lightning.bitflyer.com/docs

class BitflyerAPIWrapper:

    __url_base = 'https://api.bitflyer.jp'

    def __init__(self, api_key, api_secret):
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__http = http_requester.HttpRequester(self.__url_base)
        return

    #
    # Private API用のヘッダを生成
    #
    def __generate_header_for_private_api(self, method, path, params, body):
        timestamp = str(time.time())
        hash = self.__generate_hash(timestamp, method, path, params, body)
        return { 'ACCESS-KEY': self.__api_key,
                 'ACCESS-TIMESTAMP': timestamp,
                 'ACCESS-SIGN': hash,
                 'Content-Type': 'application/json' }

    #
    # Hashを計算
    #
    def __generate_hash(self, timestamp, method, path, params, body):
        if params is not None:
            path = path + '?' + urllib.parse.urlencode(params)
        json_body = ''
        if body is not None:
            json_body = json.dumps(body)
        ba_text = bytearray(timestamp + method + path + json_body, 'ASCII')
        ba_secret = bytearray(self.__api_secret, 'ASCII')
        hash = hmac.new(ba_secret, ba_text, hashlib.sha256).hexdigest()
        return hash
 
    #
    # Private APIを実行(GET)
    #
    def __submit_private_api_get(self, path, params):
        headers = self.__generate_header_for_private_api('GET', path, params, None)
        return self.__http.get(path, params, headers)

    #
    # Private APIを実行(POST)
    #
    def __submit_private_api_post(self, path, params, body):
        headers = self.__generate_header_for_private_api('POST', path, params, body)
        return self.__http.post(path, headers, body)

    #
    # 板情報を取得
    #
    def get_board(self):
        resp = self.__http.get('/v1/getboard', None, None)
        pprint.pprint(resp)

    #
    # FXのLTPを取得
    #
    def get_fx_ltp(self):
        params = {'product_code': 'FX_BTC_JPY'}
        return self.__http.get('/v1/getticker', params, None)['ltp']

    #
    # 現物のLTPを取得
    #
    def get_spot_ltp(self):
        params = {'product_code': 'BTC_JPY'}
        return self.__http.get('/v1/getticker', params, None)['ltp']

    #
    # APIの権限を取得
    #
    def get_permission(self):
        resp = self.__submit_private_api_get('/v1/me/getpermissions', None)
        pprint.pprint(resp)

    #
    # 資金残高を取得
    #
    def get_balance(self):
        resp = self.__submit_private_api_get('/v1/me/getbalance', None)
        pprint.pprint(resp)

    #
    # 証拠金の状態を取得
    #
    def get_collateral(self):
        resp = self.__submit_private_api_get('/v1/me/getcollateral', None)
        pprint.pprint(resp)

    #
    # 預入用アドレス取得
    #
    def get_addresses(self):
        resp = self.__submit_private_api_get('/v1/me/getaddresses', None)
        pprint.pprint(resp)

    #
    # 現在のポジションを取得
    #
    def get_positions(self):
        params = {'product_code': 'FX_BTC_JPY'}
        resp = self.__submit_private_api_get('/v1/me/getpositions', params)
        return resp

    #
    # 注文の一覧を取得
    #
    def get_childorders(self):
        params = {
            'product_code': 'FX_BTC_JPY',
            'count': '5',
            'child_order_state': 'ACTIVE'
        }
        resp = self.__submit_private_api_get('/v1/me/getchildorders', params)
        pprint.pprint(resp)

    #
    # 新規注文を出す
    #
    def send_childorders(self, order_type, side, price, size):
        body = {
            'product_code': 'FX_BTC_JPY',
            'child_order_type': order_type,
            'side': side,
            'price': str(price),
            'size': str(size),
        }
        resp = self.__submit_private_api_post('/v1/me/sendchildorder', None, body)
        pprint.pprint(resp)

    #
    # STOP注文を出す
    #
    def send_parentorders_simple_stop(self, side, price, size):
        param1 = {}
        param1['product_code'] = 'FX_BTC_JPY'
        param1['condition_type'] = 'STOP'
        param1['side'] = side
        param1['size'] = str(size)
        param1['trigger_price'] = str(price)
        parameters = []
        parameters.append(param1)
        body = {}
        body['order_method'] = 'SIMPLE'
        body['parameters'] = parameters

        resp = self.__submit_private_api_post('/v1/me/sendparentorder', None, body)
        pprint.pprint(resp)

    #
    # IFD注文を出す
    #
    def send_parentorders_ifd_stop(self, side, price, size, stop_price):
        param0 = {}
        param0['product_code'] = 'FX_BTC_JPY'
        param0['condition_type'] = 'LIMIT'
        param0['side'] = side
        param0['size'] = str(size)
        param0['price'] = str(price)
        param1 = {}
        param1['product_code'] = 'FX_BTC_JPY'
        param1['condition_type'] = 'STOP'
        param1['side'] = 'BUY' if side == 'SELL' else 'SELL'
        param1['size'] = str(size)
        param1['trigger_price'] = str(stop_price)
        parameters = []
        parameters.append(param0)
        parameters.append(param1)
        body = {}
        body['order_method'] = 'IFD'
        body['parameters'] = parameters

        resp = self.__submit_private_api_post('/v1/me/sendparentorder', None, body)
        pprint.pprint(resp)

    #
    # すべての注文をキャンセルする
    #
    def cancel_all_child_orders(self):
        body = {
            'product_code': 'FX_BTC_JPY',
        }
        resp = self.__submit_private_api_post('/v1/me/cancelallchildorders', None, body)
        pprint.pprint(resp)
