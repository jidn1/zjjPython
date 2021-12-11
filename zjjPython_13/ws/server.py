#!/usr/bin/python
import websocket
import utils.ws_url as ws_url
import exchange.huobi as hb
import exchange.binance as ba
import exchange.okex as ok
import exchange.bitget as bg


def huobi():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url.HUOBI_WS_TICKER_URL,
                                on_open = hb.on_open,
                                on_message = hb.on_message,
                                on_error = hb.on_error,
                                on_close = hb.on_close)
    ws.run_forever()


def binance():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url.BINANCE_WS_TICKER_URL,
                                on_open = ba.on_open,
                                on_message = ba.on_message,
                                on_error = ba.on_error,
                                on_close = ba.on_close)
    ws.run_forever()


def okex():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url.OKEX_WS_TICKER_URL,
                                on_open = ok.on_open,
                                on_message = ok.on_message,
                                on_error = ok.on_error,
                                on_close = ok.on_close)
    ws.run_forever()


def bitget():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url.BITGET_WS_TICKER_URL,
                                on_open = bg.on_open,
                                on_message = bg.on_message,
                                on_error = bg.on_error,
                                on_close = bg.on_close)
    ws.run_forever()