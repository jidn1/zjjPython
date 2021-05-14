
import json


symbol = 'cmt_ethusdt'
websocketURL = 'wss://contractsocket-ucloud.9ibp.com/websocket'
payload = json.dumps({'action': 'history', 'msgId': 'message1619590179968', 'productCode': symbol, 'size': 50})
