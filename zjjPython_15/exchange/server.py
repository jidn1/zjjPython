import websocket
import exchange.binance as ba

BINANCE_WS_TICKER_URL = 'wss://stream.binance.com/stream'


def binance():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(BINANCE_WS_TICKER_URL,
                                on_open = ba.on_open,
                                on_message = ba.on_message,
                                on_error = ba.on_error,
                                on_close = ba.on_close)
    ws.run_forever()


def trigger_timer(inc):
    ba.printTime(inc)
