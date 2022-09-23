from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async
import expand.girl as g
import expand.doge as d
import exchange.binanceAPI as binance
from tools import jsonData as configData
from tools.contants import *

config = configData.RunJsonData()
binan = binance.BinanceAPI('','')




@run_async
def help(update, context):
    try:
        msg = '欢迎加入*比特古*, 你在此可以为所欲为:' \
              '\n*/p 交易对* : 查看币安当前价格 ' \
              '\n*/a 交易对* : 新增监控 ' \
              '\n*/list* : 查看监控的列表 ' \
              '\n*/doge* : 查看可爱的狗狗' \
            # '\n*/girl* : 查看美女' \

        context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='markdown')
    except Exception as e:
        print(e)


@run_async
def doge(update, context):
    try:
        url = d.get_image_url()
        context.bot.send_photo(chat_id=update.message.chat_id, photo=url, parse_mode='html')
    except Exception as e:
        print(e)


@run_async
def price(update, context):
    try:
        symbol = context.args[0].upper()
        msg = binan.get_ticker_price(symbol)
        context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='markdown')
    except Exception as e:
        print(e)


@run_async
def girl(update, context):
    try:
        url = g.getGirl()
        context.bot.send_photo(chat_id=update.message.chat_id, photo=url, parse_mode='html')
    except Exception as e:
        print(e)


@run_async
def add(update, context):
    try:
        symbol = context.args[0].upper()
        price = binan.get_ticker_price(symbol)
        config.add_symbol(symbol,price)
        msg = "{symbol} 开始监控 \n 当前价格：{price} ".format(symbol=symbol,price=price)
        context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='markdown')
    except Exception as e:
        print(e)

@run_async
def list(update, context):
    try:
        symbols = config.get_symbol()
        msg = "当前监控的交易对如下：\n {symbols} ".format(symbols=symbols)
        context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='markdown')
    except Exception as e:
        print(e)


def startUp():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('p', price))
    dp.add_handler(CommandHandler('doge', doge))
    dp.add_handler(CommandHandler('girl', girl))
    dp.add_handler(CommandHandler('a', add))
    dp.add_handler(CommandHandler('list', list))
    updater.start_polling()
    updater.idle()

