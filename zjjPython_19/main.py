#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
# bitget 513   ?slug=bitget&category=spot&start=101&limit=100
# url = 'https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest'
url = 'https://api.coinmarketcap.com/data-api/v3/exchange/market-pairs/latest?slug=bitget&category=spot&start=101&limit=100'
parameters = {
    # 'slug':'bitget',
    # 'category':'spot',
    # 'start':'0',
    # 'limit':'100'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '6963e91f-72f9-4f8f-946f-8fa46000ecde',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
