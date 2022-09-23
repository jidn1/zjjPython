# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *

"""
本策略采用布林线进行均值回归交易。当价格触及布林线上轨的时候进行卖出，当触及下轨的时候，进行买入。
使用600004在 2009-09-17 13:00:00 到 2020-03-21 15:00:00 进行了回测。
注意： 
1：实盘中，如果在收盘的那一根bar或tick触发交易信号，需要自行处理，实盘可能不会成交。
"""

# 策略中必须有init方法
def init(context):
    """ init函数是在策略开始运行时被调用，进行初始化工作的函数"""

    # 设置布林线的三个参数
    context.maPeriod = 10  # 计算BOLL布林线中轨的参数
    context.stdPeriod = 10 # 计算BOLL 标准差的参数
    context.stdRange = 1  # 计算BOLL 上下轨和中轨距离的参数

    # 设置要进行回测的合约 合约名称写法详见 https://www.myquant.cn/docs/python/python_concept#44e233ec21d880c2
    # 或者可以在掘金终端的仿真交易中输入这个代码看是否查询的是需要的标的

    context.symbol = "SHSE.603259"  # 订阅&交易标的, 此处订阅的是600004
    context.period = max(context.maPeriod, context.stdPeriod, context.stdRange) + 1  # 订阅数据滑窗长度
    # 滑窗指的是每次从最新的行情往回取一定周期的数据， 相当于行情软件中k线图一个屏所容纳的k线

    # 订阅行情 第一个参数是标的， 第二个是时间周期，表示日线，第三个指指定设置count参数，表示需要的滑窗大
    # 详见 https://www.myquant.cn/docs/python/python_subscribe#15ad56f8be8519c0
    subscribe(symbols= context.symbol, frequency='1d', count=context.period)
    # 默认回撤超过10%即止损
    context.stop_loss=0.1
    context.high = 0

def on_bar(context, bars):
    """
    当init中subscribe订阅过的标的的k线完成的时候，on_bar 会被调用，用来处理计算和交易下单逻辑
    详见 https://www.myquant.cn/docs/python/python_data_event#b198d6b609adb1d4
    """

    # 获取数据滑窗，只要在init里面有订阅，在这里就可以取的到， 返回值是pandas.DataFrame的数据结构
    data = context.data(symbol=context.symbol, frequency='1d', count=context.period, fields='close')

    # 计算boll的上下界
    bollUpper = data.close.rolling(context.maPeriod).mean() \
                + context.stdRange * data.close.rolling(context.stdPeriod).std()

    bollBottom = data.close.rolling(context.maPeriod).mean() \
                 - context.stdRange * data.close.rolling(context.stdPeriod).std()

    # 获取现有持仓
    pos = context.account().position(symbol=context.symbol, side=PositionSide_Long)


    # 交易逻辑与下单
    # 当有持仓，且股价穿过BOLL上界的时候卖出股票。
    if data.close.values[-1] > bollUpper.values[-1] and data.close.values[-2] < bollUpper.values[-2]:
        if pos:  # 有持仓就市价卖出股票。
            # order_volume(symbol=context.symbol, volume=100, side=OrderSide_Sell,
            #              order_type=OrderType_Market, position_effect=PositionEffect_Close)
            print(context.now, '以市价单卖出')
            # order_target_percent(symbol=context.symbol, percent=1, order_type=OrderType_Market,
            #                      position_side=PositionSide_Short)
            # order_close_all()
            order_target_percent(symbol=context.symbol, percent=0, order_type=OrderType_Market,
                                 position_side=PositionSide_Long)
            # print(str(now) + '持仓：\n' + str(target_list))
    # 当没有持仓，且股价穿过BOLL下界的时候买出股票。
    elif data.close.values[-1] < bollBottom.values[-1] and data.close.values[-2] > bollBottom.values[-2]:
        if not pos:  # 没有持仓就买入一百股。
            # order_volume(symbol=context.symbol, volume=100, side=OrderSide_Buy,
            #              order_type=OrderType_Market, position_effect=PositionEffect_Open)
            print(context.now, '以市价单买入')
            order_target_percent(symbol=context.symbol, percent=1, order_type=OrderType_Market,
                                 position_side=PositionSide_Long)
    stop_loss(context)

# 止损策略
def stop_loss(context):
    data = history_n(symbol=context.symbol, frequency='1d', end_time=context.now, fields='high,low,close', count=2, df=True)
    price = data.close.values[-1]
    # 获取现有持仓
    pos = context.account().position(symbol=context.symbol, side=PositionSide_Long)
    if price > context.high:
        context.high = price
    if (context.high - price) / context.high > context.stop_loss and pos:
        print(context.now, 'context.symbol',context.symbol,'以市价单止损:',price)
        order_target_percent(symbol=context.symbol, percent=0, order_type=OrderType_Market,
                             position_side=PositionSide_Long)
# 查看最终的回测结果
def on_backtest_finished(context, indicator):
    print(indicator)
if __name__ == '__main__':
    '''
        strategy_id策略ID,由系统生成
        filename文件名,请与本文件名保持一致
        mode实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID,可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        '''

    run(strategy_id='e8b49858-882c-11ea-b2b5-0a0027000001',
        filename='bolling.py',
        mode=MODE_BACKTEST,
        token='9b06ce1b5a39ac39d71e58836549a95259fdcb60',
        backtest_start_time='2020-01-01 13:00:00',
        backtest_end_time='2020-08-29 15:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)