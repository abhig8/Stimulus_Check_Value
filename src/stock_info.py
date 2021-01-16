

tickers = ["TSLA", "GOOGL", "AAPL", "PTON", "FB", "AMZN", "NFLX", "BTC", "ETH", "DOGE", "XRP", "LTC", "GME"]

ticker_stock = {"TSLA": "TESLA", "GOOGL": "GOOGLE", "AAPL": "APPLE", "PTON": "PELOTON",
 "FB": "FACEBOOK", "AMZN": "AMAZON", "NFLX": "NETFLIX", "GME": "GAMESTOP"}
ticker_crypto = {"BTC": "BITCOIN", "ETH": "ETHEREUM", "DOGE": "DOGECOIN", "XRP": "RIPPLE", "LTC": "LITECOIN"}

ticker_investment = {**ticker_stock, **ticker_crypto}

tickers_second = list(ticker_stock.keys()) + list(ticker_crypto.keys())

prices_april = [130.19, 1210.41, 68.31, 31.99, 174.79, 2168.87, 396.72, 6861.21, 156.62, .0020, .1877, 41.20, 5.27]

prices_december = []

"""
adjusted for stock split:

* crypto can't be split *

- TSLA: August 31, 2020 (5 for 1)
	WAS 650.95, ADJUSTED FOR 1/5 - NOW 130.19
- AAPL: August 28, 2020 (4 for 1)
	WAS 273.24, ADJUSTED FOR 1/4 - NOW 68.31
"""

ticker_price_april = { }

for index in range(len(tickers)):
	ticker_price_april[tickers[index]] = prices_april[index]


ticker_price_april_second = {'TSLA': 130.19, 'GOOGL': 1210.41, 'AAPL': 68.31, 'PTON': 31.99, 'FB': 174.79, 'AMZN': 2168.87, 'NFLX': 396.72, 'BTC': 6861.21, 'ETH': 156.62, 'DOGE': 0.002, 'XRP': 0.1877, 'LTC': 41.2}

ticker_price_december = { }

# for index in range(len(tickers)):
# 	ticker_price_december[tickers[index]] = prices_december[index]


