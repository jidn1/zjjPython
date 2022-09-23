
import time
import exchange.binanceAPI as binance
import tools.calcIndex as calc
from tools import telegramBot as tb, jsonData as configData

binan = binance.BinanceAPI('','')
index = calc.CalcIndex()
bot = tb.TelegramBot();
config = configData.RunJsonData()


class Run_Main():

    def loop_run(self):
        while True:

            symbols = config.get_symbol()
            for symbol in symbols:

                spot_price = config.get_spot_price(symbol)  # 现货价格
                cur_market_price = binan.get_ticker_price(symbol)  # 当前交易对市价
                cur_price_change_percent = binan.get_ticker_24hour(symbol)  # 当前交易对价格涨幅
                rise_ratio = config.get_rise_ratio(symbol)  # 涨幅比例
                fall_ratio = config.get_fall_ratio(symbol)  # 跌幅比例
                right_size = len(str(cur_market_price).split(".")[1])

                if spot_price >= cur_market_price and index.calcAngle(symbol,"5m",False,right_size):

                    last_price_change = round((spot_price - cur_market_price) / spot_price,4)
                    if last_price_change > rise_ratio :
                        raise_price = round(last_price_change * 100,2)
                        bot.send_fall_msg(symbol,spot_price,cur_market_price,raise_price,cur_price_change_percent)
                        config.modify_spot_price_time(cur_market_price,symbol)

                    time.sleep(10)

                elif spot_price < cur_market_price and index.calcAngle(symbol,"5m",False,right_size):

                    last_price_change = round((cur_market_price - spot_price) / spot_price,4)
                    if last_price_change > fall_ratio :
                        raise_price = round(last_price_change * 100,2)
                        bot.send_rise_msg(symbol,spot_price,cur_market_price,raise_price,cur_price_change_percent)
                        config.modify_spot_price_time(cur_market_price,symbol)
                    time.sleep(10)

            time.sleep(60)


if __name__ == "__main__":
    instance = Run_Main()
    instance.loop_run()


