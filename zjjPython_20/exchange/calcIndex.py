#!/usr/bin/python

import exchange.binanceAPI as binance

binan = binance.BinanceAPI('','')

class CalcIndex:



    def calcMA(self,symbol,interval,point):
        '''
        :param symbol: 交易对
        :param interval: 间隔时间 1h 4h 1d
        :return: 当前时间ma20 40 60 120 的值
        '''
        sum_ma10=0
        sum_ma20=0
        sum_ma40=0
        sum_ma60 = 0
        sum_ma120 = 0

        num = 0
        data = binan.get_klines(symbol, interval, 120)
        for i in range(len(data)):
            if i>=110 and i <=120:
                sum_ma10 += float(data[i][4])
            if i>=100 and i <=120:
                sum_ma20 += float(data[i][4])
            if i>=80 and i <=120:
                sum_ma40 += float(data[i][4])
            if i >= 60 and i <= 120:
                sum_ma60 += float(data[i][4])

            sum_ma120 +=float(data[i][4])
        return [round(sum_ma10/10,point),round(sum_ma20/20,point),round(sum_ma40/40,point),round(sum_ma60/60,point), round(sum_ma120/120,point)]



    # def set_trendStatus(self,symbol,interval,point):
    #     '''
    #
    #     :param symbol:
    #     :param interval:
    #     :param point:
    #     :return: 1:多头趋势 -1 空头趋势 0 震荡
    #     '''
    #     ma_list = self.calcMA(symbol,interval, point)
    #     max_value = max(ma_list)
    #     min_value = min(ma_list)
    #     future_total = self.calcTotal(runbet.get_future_list(),runbet.get_future_step())
    #     spot_total = self.calcTotal(runbet.get_spot_list(),runbet.get_spot_step())
    #     positive_two_value = ma_list[1] if ma_list[1] > ma_list[2] and ma_list[1] > ma_list[3] else 0  # ma20 大于 ma40 60
    #     lose_two_value = ma_list[1] if ma_list[1] < ma_list[2] and ma_list[1] < ma_list[3] else 0  # ma20 小于ma40 60
    #     if ma_list[0] == max_value and ma_list[4] == min_value and positive_two_value != 0: # 多头排列，直到形态走坏
    #         if runbet.get_hedgingStatus() != 11 and future_total is not 0: #多头趋势未开启对冲
    #
    #             res = msg.buy_market_msg(self.coinType,future_total)
    #             if res['orderId']:
    #                 runbet.set_hedgingStatus(11)
    #         return 1
    #     elif ma_list[0] == min_value and ma_list[4] == max_value and lose_two_value is not 0: # 空头
    #         if runbet.get_hedgingStatus() != -11 and spot_total is not 0: #空头趋势未开启对冲
    #                 res = msg.open_sell_market_msg(self.coinType, spot_total)
    #                 if res['orderId']:
    #                     runbet.set_hedgingStatus(-11)
    #         return -1
    #     else:
    #         if runbet.get_hedgingStatus() == 11 and future_total is not 0 : #已经开启多头对冲，关闭掉
    #             res = msg.sell_market_msg(self.coinType,future_total)
    #             if res['orderId']:
    #                 runbet.set_hedgingStatus(0)
    #
    #         elif runbet.get_hedgingStatus() == -11 and future_total is not 0: # 已经开启空头对冲，关闭掉
    #             res = msg.do_sell_market_msg(self.coinType,spot_total)
    #             if res['orderId']:
    #                 runbet.set_hedgingStatus(0)
    #         return 0

    def calcTotal(self,arr,step):
        total = 0
        for i in range(step):
            if len(arr) <= i:
                total += arr[-1]
            else:
                total += arr[i]
        return total

    def calcSlopeMA10(self,symbol,interval,point):
        '''

        :param symbol:
        :param interval:
        :return: 上一时刻的m20值
        '''
        last_ma10 = 0
        next_ma10 = 0
        num = 0
        data = binan.get_klines(symbol, interval, 11)
        for i in range(len(data)):
            if i==0:
                last_ma10+=float(data[i][4])
            elif i==10:
                next_ma10+=float(data[i][4])
            else:
                last_ma10+=float(data[i][4])
                next_ma10+=float(data[i][4])

        return [round(last_ma10/10,point),round(next_ma10/10,point)]

    def calcSlopeMA5(self,symbol,interval,point):
        '''

        :param symbol:
        :param interval:
        :return: 上一时刻的m20值
        '''
        last_ma5 = 0
        next_ma5 = 0
        data = binan.get_klines(symbol, interval, 6)
        for i in range(len(data)):
            if i==0:
                last_ma5+=float(data[i][4])
            elif i==5:
                next_ma5+=float(data[i][4])
            else:
                last_ma5+=float(data[i][4])
                next_ma5+=float(data[i][4])

        return [round(last_ma5/5,point), round(next_ma5/5,point)]


    # def calcSlope(self,symbol,interval,direction):
    #     '''
    #
    #     :param symbol:
    #     :param interval:
    #     :param direction: 多头还是空头 多:true 空为:false
    #     :return: 斜率是否满足开仓
    #     '''
    #     lastMA10,tmpMA10 = self.calcSlopeMA10(symbol,interval)
    #     if direction:
    #         return tmpMA10 > lastMA10
    #     else:
    #         return lastMA10 > tmpMA10


    def calcAngle(self,symbol,interval,direction,point):
        '''

        :param symbol:
        :param interval:
        :param direction:
        :return: 趋势来了 正在拉伸 不买
        '''
        lastMA5,tmpMA5 = self.calcSlopeMA5(symbol, interval,point)
        if direction:
            return tmpMA5 <= lastMA5
        else:
            return tmpMA5 >= lastMA5

    def calcMA10(self,symbol,interval,point):
        sum_ma10 = 0
        data = binan.get_klines(symbol, interval, 10)
        for i in range(len(data)):
            sum_ma10+=float(data[i][4])

        return round(sum_ma10 / 10,point)

    def get_position_price(self,symbol,direction=True):
        tmp = binan.get_positionInfo(symbol)
        for item in tmp:  # 遍历是有仓位
            if direction: # 多头持仓均价
                if item['positionSide'] == "LONG" and float(item['positionAmt']) != 0.0:
                    return float(item['entryPrice'])
            else:        # 空头持仓均价
                if item['positionSide'] == "SHORT" and float(item['positionAmt']) != 0.0:
                    return float(item['entryPrice'])

        return False