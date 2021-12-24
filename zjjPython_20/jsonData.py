import os, json, time

data_path = os.getcwd()+""+"/config.json"
# data_path = "/Users/jidening/soft/ideaWorkSpace/gitProject/zjjPython/zjjPython_20/config.json"
class RunJsonData:

    def _get_json_data(self):
        '''读取json文件'''
        tmp_json = {}
        with open(data_path, 'r') as f:
            tmp_json = json.load(f)
            f.close()
        return tmp_json

    def _modify_json_data(self, data):
        '''修改json文件'''
        with open(data_path, "w") as f:
            f.write(json.dumps(data, indent=4))
        f.close()

    def get_symbol(self):
        data_json = self._get_json_data()
        return data_json["symbols"]

    def get_spot_price(self,symbol):
        '''获取上次价格'''
        data_json = self._get_json_data()
        return data_json['data'][symbol]['price']

    def get_rise_ratio(self,symbol):
        '''上涨比率'''
        data_json = self._get_json_data()
        return data_json['data'][symbol]['rise_ratio']

    def get_fall_ratio(self,symbol):
        '''下跌比率'''
        data_json = self._get_json_data()
        return data_json['data'][symbol]['fall_ratio']

    def modify_spot_price_time(self, deal_price,symbol):
        data_json = self._get_json_data()
        data_json["data"][symbol]['price'] = deal_price # 保留2位小数
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data_json["data"][symbol]["time"] = dt
        self._modify_json_data(data_json)

    def add_symbol(self,symbol,price):
        data_json = self._get_json_data()
        data_json["symbols"].append(symbol)
        newSymbol = {}
        newSymbol['price'] = price
        newSymbol['rise_ratio'] = 0.01
        newSymbol['fall_ratio'] = 0.01
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        newSymbol["time"] = dt
        data_json["data"][symbol] = newSymbol
        self._modify_json_data(data_json)


if __name__ == '__main__':
    config = RunJsonData()
    config.add_symbol("SNADUSDT",3.56)