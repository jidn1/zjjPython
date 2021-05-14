#!/usr/bin/python
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext.dispatcher import run_async
import exchange.huobi as hb
import expand.doge as d
import expand.girl as g


@run_async
def help(update, context):
    try:
        msg = '欢迎加入*比特古*, 你在此可以为所欲为:' \
              '\n*/p 交易对*:查看火币当前价格 ' \
              '\n*/doge* : 查看可爱的狗狗' \
              '\n*/girl* : 查看色图'  \
              '\n*/porn* : 查看小片片';
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
        symbol = context.args[0]
        msg = hb.getTicker(symbol)
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
def porn(update, context):
    try:
        url = g.getGirl()
        context.bot.send_photo(chat_id=update.message.chat_id, photo=url, parse_mode='html')
    except Exception as e:
        print(e)


def startUp():
    updater = Updater('BOT_TOKEN', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('p', price))
    dp.add_handler(CommandHandler('doge', doge))
    dp.add_handler(CommandHandler('girl', girl))
    dp.add_handler(CommandHandler('porn', porn))
    updater.start_polling()
    updater.idle()


