#!/usr/bin/python

import requests, time, hmac, hashlib
from urllib.parse import urlencode


class BinanceAPI(object):
    BASE_URL = "https://www.binance.com/api/v1"
    FUTURE_URL = "https://fapi.binance.com"
    BASE_URL_V3 = "https://api.binance.com/api/v3"
    PUBLIC_URL = "https://www.binance.com/exchange/public/product"

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def get_ticker_price(self,market):
        time.sleep(2)
        path = "%s/ticker/price" % self.BASE_URL_V3
        params = {"symbol":market}
        res =  self._get_no_sign(path,params)
        return float(res['price'])

    def get_ticker_24hour(self,market):
        path = "%s/ticker/24hr" % self.BASE_URL_V3
        params = {"symbol":market}
        res =  self._get_no_sign(path,params)
        return round(float(res['priceChangePercent']),2)

    def get_ticker_exchange(self,market):
        time.sleep(2)
        path = "%s/fapi/v1/ticker/price" % self.FUTURE_URL
        params = {"symbol":market}
        res =  self._get_no_sign(path,params)
        return float(res['price'])

    def buy_market(self, market, quantity):
        '''
            现货市价买入
        :param market:
        :param quantity:
        :return:
        '''
        path = "%s/order" % self.BASE_URL_V3
        params = self._spot_order(market, quantity, "BUY")
        return self._post(path, params)

    def sell_market(self, market, quantity):
        '''现货市价卖出'''
        path = "%s/order" % self.BASE_URL_V3
        params = self._spot_order(market, quantity, "SELL")
        return self._post(path, params)

    def market_future_order(self, side, symbol, quantity,positionSide):

        ''' 合约市价单
            :param side: 做多or做空 BUY SELL
            :param symbol:币种类型。如：BTCUSDT、ETHUSDT
            :param quantity: 购买量
            :param positionSide: 双向持仓 BUY-LONG 开多 SELL-SHORT 开空
            :param price: 开仓价格
        '''
        path = "%s/fapi/v1/order" % self.FUTURE_URL
        params = self._order(symbol, quantity, side, positionSide)
        return self._post(path, params)


    def get_klines(self, market, interval, limit,startTime=None, endTime=None):
        path = "%s/klines" % self.BASE_URL_V3
        params = None
        if startTime is None:
            params = {"symbol": market, "interval":interval, "limit":limit}
        else:
            params = {"symbol": market,"limit":limit, "interval":interval, "startTime":startTime, "endTime":endTime}
        return self._get_no_sign(path, params)

    def get_spot_trades(self, symbol):
        '''获取账户成交历史'''
        path = "%s/myTrades" % self.BASE_URL_V3
        params = {"symbol":symbol}
        time.sleep(1)
        return self._get(path, params).json()

    ### --- 合约 --- ###
    def set_leverage(self,symbol, leverage):

        ''' 调整开仓杠杆
            :param symbol 交易对
            :param leverage 杠杆倍数
        '''
        path = "%s/fapi/v1/leverage" % self.BASE_URL
        params = {'symbol':symbol, 'leverage': leverage}
        return self._post(path, params)

    def get_positionInfo(self, symbol):
        '''当前持仓交易对信息'''
        path = "%s/fapi/v2/positionRisk" % self.FUTURE_URL
        params = {"symbol":symbol}
        time.sleep(1)
        return self._get(path, params)


    def limit_future_order(self, side, market, quantity,positionSide, price):

        ''' 合约限价单
            :param side: 做多or做空 BUY SELL
            :param market:币种类型。如：BTCUSDT、ETHUSDT
            :param quantity: 购买量
            :param positionSide: 双向持仓 BUY-LONG 开多 SELL-SHORT 开空
            :param price: 开仓价格
        '''
        path = "%s/fapi/v1/order" % self.FUTURE_URL
        params = self._order(market, quantity, side, positionSide, price)
        return self._post(path, params)

    ### ----私有函数---- ###

    def _order(self, market, quantity, side, positionSide,price=None):
        '''
        :param market:币种类型。如：BTCUSDT、ETHUSDT
        :param quantity: 购买量
        :param side: 订单方向，买还是卖
        :param positionSide 双向持仓
        :param price: 价格
        :return:
        '''
        params = {}

        if price is not None:
            params["type"] = "LIMIT"
            params["price"] = self._format(price)
            params["timeInForce"] = "GTC"
        else:
            params["type"] = "MARKET"

        params["symbol"] = market
        params["side"] = side
        params["quantity"] = '%.8f' % quantity
        params['positionSide'] = positionSide
        return params

    def _spot_order(self, market, quantity, side, price=None):
        '''
        :param market:币种类型。如：BTCUSDT、ETHUSDT
        :param quantity: 购买量
        :param side: 订单方向，买还是卖
        :param price: 价格
        :return:
        '''
        params = {}

        if price is not None:
            params["type"] = "LIMIT"
            params["price"] = self._format(price)
            params["timeInForce"] = "GTC"
        else:
            params["type"] = "MARKET"

        params["symbol"] = market
        params["side"] = side
        params["quantity"] = '%.8f' % quantity

        return params

    def _get(self, path, params={}):
        params.update({"recvWindow": 5000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.get(url, headers=header,timeout=30, verify=True).json()

    def _get_no_sign(self, path, params={}):
        query = urlencode(params)
        url = "%s?%s" % (path, query)
        return requests.get(url, timeout=180, verify=True).json()

    def _sign(self, params={}):
        data = params.copy()

        ts = int(1000 * time.time())
        data.update({"timestamp": ts})
        h = urlencode(data)
        b = bytearray()
        b.extend(self.secret.encode())
        signature = hmac.new(b, msg=h.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        data.update({"signature": signature})
        return data

    def _post(self, path, params={}):
        params.update({"recvWindow": 5000})
        query = self._sign(params)
        url = "%s" % (path)
        header = {"X-MBX-APIKEY": self.key}
        return requests.post(url, headers=header, data=query,timeout=180, verify=True).json()

    def _format(self, price):
        return "{:.8f}".format(price)



if __name__ == "__main__":
    instance = BinanceAPI('pWkjFBUETB8S1QwpJcxzr8YGmFYwxDwC91eIKwZZEE8RJIPiNK9cW0pCMXTs3APx','YI3nYZ6YcbW6YxWpb0pJoSIokM8ngsKkVMxajVyHiBzjRrE8CZ5LHHr5bzwGP0rj')
    print(instance.get_ticker_price("RNDRUSDT"))