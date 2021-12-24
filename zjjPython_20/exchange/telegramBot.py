
import telegram

bot_token = ''
group_id = ''



class TelegramBot:

    def send_msg(self, symbol,  price, quoteRatio):
        msg = "上涨预警：\n币种为：{cointype}\n 当前价格：{price} \n 24小时涨跌幅：{quoteRatio}%".format(cointype=symbol,price=price,quoteRatio=quoteRatio)
        bot = telegram.Bot(token=bot_token)
        bot.sendMessage(chat_id=group_id, text=msg)

    def send_rise_msg(self, symbol, lastPrice, price, quoteRatio,dayRatio):
        msg = "上涨预警：\n 币种为：{cointype}\n 上次价格：{lastPrice}\n 当前价格：{price}\n 上涨幅度：{quoteRatio}%,\n 24H涨跌幅：{dayRatio}%".format(cointype=symbol,lastPrice=lastPrice,price=price,quoteRatio=quoteRatio,dayRatio=dayRatio)
        bot = telegram.Bot(token=bot_token)
        bot.sendMessage(chat_id=group_id, text=msg)

    def send_fall_msg(self, symbol, lastPrice, price, quoteRatio,dayRatio):
        msg = "下跌报警：\n 币种为：{cointype}\n 上次价格：{lastPrice}\n 当前价格：{price}\n 下跌幅度：{quoteRatio}% \n 24H涨跌幅：{dayRatio}%".format(cointype=symbol,lastPrice=lastPrice,price=price,quoteRatio=quoteRatio,dayRatio=dayRatio)
        bot = telegram.Bot(token=bot_token)
        bot.sendMessage(chat_id=group_id, text=msg)





