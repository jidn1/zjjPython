# import os,json,time
# import exchange.binanceAPI as binance
#
# # 本地调试
# data_path = os.getcwd()+""+"/data.json"
# binan = binance.BinanceAPI('','')
#
#
# class RunBetData:
#
#     def _get_json_data(self):
#         '''读取json文件'''
#         tmp_json = {}
#         with open(data_path, 'r') as f:
#             tmp_json = json.load(f)
#             f.close()
#         return tmp_json
#
#
#     def _modify_json_data(self,data):
#         '''修改json文件'''
#         with open(data_path, "w") as f:
#             f.write(json.dumps(data, indent=4))
#         f.close()
#
#
#     ####------下面为输出函数--------####
#     def get_hedgingStatus(self):
#         '''
#             趋势行情是否开启对冲
#         :return: boolean
#         '''
#         data_json = self._get_json_data()
#         return data_json["config"]['hedging']
#
#     # def get_MApoint(self):
#     #     '''返回均线需要的小数点位数'''
#     #     data_json = self._get_json_data()
#     #     return data_json["config"]['MApoint']
#
#     def get_record_future_price(self):
#         '''卖出后，step减一后，再读取上次买入的价格'''
#         data_json = self._get_json_data()
#         cur_step = self.get_future_step() - 1
#         return data_json['runBet']['record_future_price'][cur_step]
#
#     def get_record_spot_price(self):
#         '''卖出后，step减一后，再读取上次买入的价格'''
#         data_json = self._get_json_data()
#         cur_step = self.get_spot_step() - 1
#         return data_json['runBet']['record_spot_price'][cur_step]
#
#     def get_spot_buy_price(self):
#         data_json = self._get_json_data()
#         return data_json["runBet"]["spot_buy_price"]
#
#     def get_floor_price(self):
#         data_json = self._get_json_data()
#         return data_json["config"]["floor_price"]
#
#     def get_ceil_price(self):
#         data_json = self._get_json_data()
#         return data_json["config"]["ceil_price"]
#
#     def get_spot_sell_price(self):
#         data_json = self._get_json_data()
#         return data_json["runBet"]["spot_sell_price"]
#
#     def get_future_buy_price(self):
#         data_json = self._get_json_data()
#         return data_json["runBet"]["future_buy_price"]
#
#
#     def get_future_sell_price(self):
#         data_json = self._get_json_data()
#         return data_json["runBet"]["future_sell_price"]
#
#     def get_cointype(self):
#         data_json = self._get_json_data()
#         return data_json["config"]["cointype"]
#
#     def get_spot_quantity(self,exchange_method=True):
#         '''
#         :param exchange: True 代表买入，取买入的仓位 False：代表卖出，取卖出应该的仓位
#         :return:
#         '''
#
#         data_json = self._get_json_data()
#         cur_step = data_json["runBet"]["spot_step"] if exchange_method else data_json["runBet"]["spot_step"] - 1 # 买入与卖出操作对应的仓位不同
#         quantity_arr = data_json["config"]["spot_quantity"]
#
#         quantity = None
#         if cur_step < len(quantity_arr): # 当前仓位 > 设置的仓位 取最后一位
#             quantity = quantity_arr[0] if cur_step == 0 else quantity_arr[cur_step]
#         else:
#             quantity = quantity_arr[-1]
#         return quantity
#
#     def get_spot_list(self):
#         '''获取仓位数组'''
#         data_json = self._get_json_data()
#         return data_json["config"]["spot_quantity"]
#
#     def get_future_list(self):
#         '''获取仓位数组'''
#         data_json = self._get_json_data()
#         return data_json["config"]["future_quantity"]
#
#     def get_future_quantity(self,exchange_method=True):
#         '''
#         :param exchange: True 代表买入，取买入的仓位 False：代表卖出，取卖出应该的仓位
#         :return:
#         '''
#
#         data_json = self._get_json_data()
#         cur_step = data_json["runBet"]["future_step"] if exchange_method else data_json["runBet"]["future_step"] - 1 # 买入与卖出操作对应的仓位不同
#         quantity_arr = data_json["config"]["future_quantity"]
#
#         quantity = None
#         if cur_step < len(quantity_arr): # 当前仓位 > 设置的仓位 取最后一位
#             quantity = quantity_arr[0] if cur_step == 0 else quantity_arr[cur_step]
#         else:
#             quantity = quantity_arr[-1]
#         return quantity
#
#     def get_position_price(self):
#         '''获取现货持仓均价'''
#         data_json = self._get_json_data()
#         return data_json['runBet']['position_spot_price']
#
#     def get_position(self):
#         '''获取是否持仓均价平仓开关'''
#         data_json = self._get_json_data()
#         return data_json['config']['position']
#
#     def get_position_size(self):
#         '''获取否持仓均价仓位数,满足则直接均价平'''
#         data_json = self._get_json_data()
#         return data_json['config']['position_size']
#
#     def get_spot_step(self):
#         '''获取现货仓位数'''
#         data_json = self._get_json_data()
#         return data_json['runBet']['spot_step']
#
#     def get_future_step(self):
#         '''获取期货仓位数'''
#         data_json = self._get_json_data()
#         return data_json['runBet']['future_step']
#
#     def get_profit_ratio(self):
#         '''获取补仓比率'''
#         data_json = self._get_json_data()
#         return data_json['config']['profit_ratio']
#
#     def get_double_throw_ratio(self):
#         '''获取止盈比率'''
#         data_json = self._get_json_data()
#         return data_json['config']['double_throw_ratio']
#
#     def get_ratio_coefficient(self):
#         '''获取倍率系数'''
#         data_json = self._get_json_data()
#         return data_json['config']['RatioCoefficient']
#
#     def add_record_spot_price(self,value):
#         '''记录交易价格'''
#         data_json = self._get_json_data()
#         data_json['runBet']['record_spot_price'].append(value)
#         self._modify_json_data(data_json)
#
#
#     def remove_record_spot_price(self):
#         '''记录交易价格'''
#         data_json = self._get_json_data()
#         del data_json['runBet']['record_spot_price'][-1]
#         self._modify_json_data(data_json)
#
#     def add_record_future_price(self,value):
#         '''记录交易价格'''
#         data_json = self._get_json_data()
#         data_json['runBet']['record_future_price'].append(value)
#         self._modify_json_data(data_json)
#
#
#     def remove_record_future_price(self):
#         '''记录交易价格'''
#         data_json = self._get_json_data()
#         del data_json['runBet']['record_future_price'][-1]
#         self._modify_json_data(data_json)
#
#     # 买入后，修改 补仓价格 和 网格平仓价格以及步数
#     def modify_spot_price(self, deal_price):
#         data_json = self._get_json_data()
#         right_size = len(str(deal_price).split(".")[1]) + 2
#         data_json["runBet"]["spot_buy_price"] = round(deal_price * (1 - data_json["config"]["double_throw_ratio"] / 100),right_size) # 保留2位小数
#         data_json["runBet"]["spot_sell_price"] = round(deal_price * (1 + data_json["config"]["profit_ratio"] / 100), right_size)
#
#         self._modify_json_data(data_json)
#
#     def modify_future_price(self, deal_price):
#         data_json = self._get_json_data()
#         right_size = len(str(deal_price).split(".")[1]) + 2
#         data_json["runBet"]["future_buy_price"] = round(deal_price * (1 + data_json["config"]["profit_ratio"] / 100), right_size) # 保留2位小数
#         data_json["runBet"]["future_sell_price"] = round(deal_price * (1 - data_json["config"]["double_throw_ratio"] / 100), right_size)
#
#         self._modify_json_data(data_json)
#
#     def set_future_step(self,future_step,index=None):
#         '''修改期货仓位数'''
#         data_json = self._get_json_data()
#         data_json['runBet']['future_step'] = future_step
#         if index != None:
#             data_json['config']['profit_ratio'] = index
#             data_json['config']['double_throw_ratio'] = index
#
#         self._modify_json_data(data_json)
#
#     def set_hedgingStatus(self,num):
#         data_json = self._get_json_data()
#         data_json['config']['hedging'] = num
#         self._modify_json_data(data_json)
#
#     def set_spot_step(self,spot_step, index=None):
#         '''修改期货仓位数,以及比率'''
#         data_json = self._get_json_data()
#         data_json['runBet']['spot_step'] = spot_step
#         if index != None:
#             data_json['config']['profit_ratio'] = index
#             data_json['config']['double_throw_ratio'] = index
#         self._modify_json_data(data_json)
#
#     def set_ratio(self,symbol):
#         '''修改补仓止盈比率'''
#         data_json = self._get_json_data()
#         ratio_24hr = binan.get_ticker_24hour(symbol) #
#         index = abs(ratio_24hr)
#
#         if abs(ratio_24hr) >  8 : # 这是单边走势情况 只改变一方的比率
#             if ratio_24hr > 0 : # 单边上涨，补仓比率不变
#                 data_json['config']['profit_ratio'] = 5 + self.get_spot_step()/2 #
#                 data_json['config']['double_throw_ratio'] = 5 + self.get_future_step()/4 #
#             else: # 单边下跌
#                 data_json['config']['double_throw_ratio'] =  5 + self.get_future_step()/2
#                 data_json['config']['profit_ratio'] =  5 + self.get_spot_step()/4
#
#         else: # 系数内震荡行情
#
#             data_json['config']['double_throw_ratio'] = 2 +self.get_future_step()/4
#             data_json['config']['profit_ratio'] = 2 + self.get_future_step()/4
#         self._modify_json_data(data_json)
#
#     def delete_extra_zero(self, n):
#         '''删除小数点后多余的0'''
#         if isinstance(n, int):
#             return n
#         if isinstance(n, float):
#             n = str(n).rstrip('0')  # 删除小数点后多余的0
#             n = int(n.rstrip('.')) if n.endswith('.') else float(n)  # 只剩小数点直接转int，否则转回float
#             return n
#
#
# if __name__ == "__main__":
#     instance = RunBetData()
#     # print(instance.modify_price(8.87,instance.get_step()-1))
#     print(instance.get_future_quantity())