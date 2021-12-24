#
# import time
# import exchange.binanceAPI as binance
# import exchange.runBetData as betData
# import exchange.calcIndex as calc
# import exchange.telegramBot as tel
#
# binan = binance.BinanceAPI('pWkjFBUETB8S1QwpJcxzr8YGmFYwxDwC91eIKwZZEE8RJIPiNK9cW0pCMXTs3APx','YI3nYZ6YcbW6YxWpb0pJoSIokM8ngsKkVMxajVyHiBzjRrE8CZ5LHHr5bzwGP0rj')
# runbet = betData.RunBetData()
# index = calc.CalcIndex()
# bot = tel.TelegramBot();
#
# class Run_Main():
#
#     def __init__(self):
#         self.coinType = runbet.get_cointype()  # 交易币种
#         self.profitRatio = runbet.get_profit_ratio() # 止盈比率
#         self.doubleThrowRatio = runbet.get_double_throw_ratio() # 补仓比率
#         pass
#
#     def loop_run(self):
#         while True:
#
#             rise_ratio = runbet.get_rise_ratio() # 现货价格 上涨幅度
#             fall_ratio = runbet.get_fall_ratio() # 现货价格 下跌幅度
#
#             spot_buy_price = runbet.get_spot_buy_price()  # 现货买入价格
#             spot_sell_price = runbet.get_spot_sell_price() # 现货卖出价格
#             spot_quantity = runbet.get_spot_quantity()  # 现货买入量
#             spot_step = runbet.get_spot_step()  # 当前现货步数(手数)
#
#             future_buy_price = runbet.get_future_buy_price()  # 现货买入价格
#             future_sell_price = runbet.get_future_sell_price() # 现货卖出价格
#             future_quantity = runbet.get_future_quantity()   # 期货买入量
#             future_step = runbet.get_future_step() # 当前期货步数(手数)
#
#             cur_market_price = binan.get_ticker_price(runbet.get_cointype())  # 当前交易对市价
#             cur_price_change_percent = binan.get_ticker_24hour(runbet.get_cointype())  # 当前交易对价格涨幅
#             right_size = len(str(cur_market_price).split(".")[1])
#             #trend_status = index.set_trendStatus(self.coinType, "1d", right_size) # 趋势状态值
#
#
#             # 超出范围不允许网格策略
#             if cur_market_price < runbet.get_floor_price() or cur_market_price > runbet.get_ceil_price():
#                 time.sleep(60 * 10)
#                 continue
#
#             # 开多
#             elif spot_buy_price >= cur_market_price and index.calcAngle(self.coinType,"5m",False,right_size):   # 做多买入,趋势正在拉升，不买入
#
#                 bot.send_msg(self.coinType,cur_market_price,cur_price_change_percent)
#                 runbet.set_spot_step(spot_step+1)
#                 runbet.set_ratio(self.coinType)
#                 runbet.modify_spot_price(cur_market_price) #修改data.json中价格、当前步数
#                 time.sleep(60*0.5) # 挂单后，停止运行1分钟
#                 # res = msg.open_buy_market_msg(self.coinType, spot_quantity) # 现货买入
#                 #
#                 # if res['orderId']: # 挂单成功
#                 #     time.sleep(1)
#                 #     runbet.set_spot_step(spot_step+1)
#                 #     runbet.set_ratio(self.coinType)
#                 #     runbet.modify_spot_price(cur_market_price) #修改data.json中价格、当前步数
#                 #     time.sleep(60*0.5) # 挂单后，停止运行1分钟
#                 # else:
#                 #     break
#             # 开空
#             elif future_buy_price <= cur_market_price and index.calcAngle(self.coinType, "5m",True,right_size):  # 是否满足卖出价
#                 print("future_buy_price")
#                 runbet.set_ratio(self.coinType)
#                 runbet.modify_future_price(cur_market_price)  # 修改data.json中价格
#                 runbet.set_future_step(future_step + 1)
#                 # future_res = msg.open_sell_market_msg(self.coinType, future_quantity)  # 期货买入开空
#                 # if future_res['orderId']:
#                 #     time.sleep(1)
#                 #     runbet.set_ratio(self.coinType)
#                 #     runbet.modify_future_price(cur_market_price)  # 修改data.json中价格
#                 #     runbet.set_future_step(future_step + 1)
#                 #     time.sleep(60 * 1)  # 挂单后，停止运行1分钟
#                 # else:
#                 #     break
#             # 平多
#             elif spot_sell_price <= cur_market_price and index.calcAngle(self.coinType,"5m",True,right_size):  # 是否满足卖出价
#                 if spot_step > 0 :
#                     # spot_res = msg.do_buy_market_msg(self.coinType,runbet.get_spot_quantity(False)) # 期货卖出开多
#
#                     # if spot_res['orderId']:
#                         runbet.set_ratio(self.coinType)
#                         last_price = runbet.get_record_spot_price()
#                         runbet.modify_spot_price(last_price) #修改data.json中价格
#                         runbet.set_spot_step(spot_step - 1)  # 挂卖单,仓位 -1
#                         runbet.remove_record_spot_price()
#                         time.sleep(60*0.5)  # 挂单后，停止运行1分钟
#                     # else:
#                     #     break
#                 else:
#                     runbet.modify_spot_price(cur_market_price)
#             # 平空
#             elif future_sell_price >= cur_market_price and index.calcAngle(self.coinType, "5m", False,right_size):  # 是否满足卖出价
#                 print("future_sell_price")
#                 if future_step > 0:
#                     # future_res = msg.do_sell_market_msg(self.coinType, runbet.get_future_quantity(False))  # 期货卖出开多
#                     # if future_res['orderId']:
#                         runbet.set_ratio(self.coinType)
#                         last_price = runbet.get_record_future_price()
#                         runbet.modify_future_price(last_price)  # 修改data.json中价格
#                         runbet.set_future_step(future_step - 1)  # 挂卖单,仓位 -1
#                         runbet.remove_record_future_price()
#                         time.sleep(60 * 0.5)  # 挂单后，停止运行1分钟
#                     # else:
#                     #     break
#                 else:
#                     runbet.modify_future_price(cur_market_price)
#
#             time.sleep(2) # 为了不被币安api请求次数限制
#
#
# if __name__ == "__main__":
#     instance = Run_Main()
#     instance.loop_run()
#
