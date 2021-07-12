from new_investment import add_investment


# when adding new investment need to add to all uncommented variables on this page and run and update_investment line in updater.py


tickers = ["TSLA", "GOOGL", "AAPL", "PTON", "FB", "AMZN", "NFLX",  "GME", "AMC", "NOK", "KOSS", "BB", "T", "MSFT", "TGT", "CVS", "BTC", "ETH", "DOGE", "XRP", "LTC", "USDT", "LINK", "ETC", "BCH", "ALGO"]

ticker_stock = {"TSLA": "TESLA", "GOOGL": "GOOGLE", "AAPL": "APPLE", "PTON": "PELOTON",
 "FB": "FACEBOOK", "AMZN": "AMAZON", "NFLX": "NETFLIX", "GME": "GAMESTOP", "AMC": "AMC THEATRES", "NOK":"NOKIA", "KOSS": "KOSS CORPORATION", "BB":"BLACKBERRY", "T":"AT&T", "MSFT": "MICROSOFT", "TGT": "TARGET", "CVS": "CVS HEALTH"}
ticker_crypto = {"BTC": "BITCOIN", "ETH": "ETHEREUM", "DOGE": "DOGECOIN", "XRP": "RIPPLE", "LTC": "LITECOIN", "USDT": "TETHER", "LINK": "CHAINLINK", "ETC": "ETHEREUM CLASSIC", "BCH": "BITCOIN CASH", "ALGO": "ALGORAND"}


ticker_investment = {**ticker_stock, **ticker_crypto}

prices_april = [142.00, 1234.00, 70.16, 31.70, 172.82, 2245.00, 412.25, 4.90, 2.02, 3.17, .92, 3.70, 29.96, 169.24, 105.25, 59.45, 6555.50, 150.36, .001886, .177, 38.60, .9811, 3.02, 4.92, 209.52, 0.1689]
ticker_price_april = dict(zip(tickers, prices_april))

"""
adjusted for stock split:

* crypto can't be split *

- TSLA: August 31, 2020 (5 for 1)
	WAS 650.95, ADJUSTED FOR 1/5 - NOW 130.19
- AAPL: August 28, 2020 (4 for 1)
	WAS 273.24, ADJUSTED FOR 1/4 - NOW 68.31
"""




#once second check prices are added
# prices_december = []
# ticker_price_december = dict(zip(tickers, prices_december))




# stocks with image links that require lowercase tickers
# lower_case_stock_links = ["GOOGL", "FB", "AAPL", "CVS", "AMZN", "NFLX", "T"]
# def get_image_link(ticker, stock):
# 	if ticker.upper() in ticker_crypto.keys():
# 		if ticker == "XRP":
# 			stock = "XRP"
# 		return "https://cryptologos.cc/logos/" + stock.replace(" ", "-").lower() + "-" + ticker.lower() + "-logo.png?v=010"
# 	elif ticker.upper() in lower_case_stock_links:
# 		return "https://eodhistoricaldata.com/img/logos/US/" + ticker.lower() + ".png"
# 	else:
# 		return "https://eodhistoricaldata.com/img/logos/US/" + ticker.upper() + ".png"




# list of image links generated with loop
ticker_stock_image_link = {'TSLA': 'https://eodhistoricaldata.com/img/logos/US/TSLA.png', 'GOOGL': 'https://eodhistoricaldata.com/img/logos/US/googl.png', 'AAPL': 'https://eodhistoricaldata.com/img/logos/US/aapl.png', 'PTON': 'https://eodhistoricaldata.com/img/logos/US/PTON.png', 'FB': 'https://eodhistoricaldata.com/img/logos/US/fb.png', 'AMZN': 'https://eodhistoricaldata.com/img/logos/US/amzn.png', 'NFLX': 'https://eodhistoricaldata.com/img/logos/US/nflx.png', 'GME': 'https://eodhistoricaldata.com/img/logos/US/GME.png', 'AMC': 'https://eodhistoricaldata.com/img/logos/US/AMC.png', 'NOK': 'https://eodhistoricaldata.com/img/logos/US/NOK.png', 'KOSS': 'https://eodhistoricaldata.com/img/logos/US/KOSS.png', 'BB': 'https://eodhistoricaldata.com/img/logos/US/BB.png', 'T': 'https://eodhistoricaldata.com/img/logos/US/t.png', 'MSFT': 'https://eodhistoricaldata.com/img/logos/US/MSFT.png', 'TGT': 'https://eodhistoricaldata.com/img/logos/US/TGT.png', 'CVS': 'https://eodhistoricaldata.com/img/logos/US/cvs.png', 'BTC': 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=010', 'ETH': 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=010', 'DOGE': 'https://cryptologos.cc/logos/dogecoin-doge-logo.png?v=010', 'XRP': 'https://cryptologos.cc/logos/xrp-xrp-logo.png?v=010', 'LTC': 'https://cryptologos.cc/logos/litecoin-ltc-logo.png?v=010', 'USDT': 'https://cryptologos.cc/logos/tether-usdt-logo.png?v=010', 'LINK': 'https://cryptologos.cc/logos/chainlink-link-logo.png?v=010', 'ETC': 'https://cryptologos.cc/logos/ethereum-classic-etc-logo.png?v=010', 'BCH': 'https://cryptologos.cc/logos/bitcoin-cash-bch-logo.png?v=010', 'ALGO': 'https://cryptologos.cc/logos/algorand-algo-logo.png?v=010'}


# iterator and print used to copy and paste into set dictionary
# ticker_stock_image_link2 = {}
# for ticker, stock in ticker_investment.items():
# 	ticker_stock_image_link2[ticker] = get_image_link(ticker, stock)
# print(ticker_stock_image_link2)


print(ticker_stock_image_link["BTC"])

# adding new investments to nav bar dropdown in base.html:
# for ticker, stock in ticker_stock.items():
# 	print("<li><a class= \"dropdown-item\" href=" + ticker + '>' + stock + "</a></li>")
# for ticker, crypto in ticker_crypto.items():
# 	print("<li><a class= \"dropdown-item\" href=" + ticker + '>' + crypto + "</a></li>")


# print(len(ticker_stock))
# for ticker, stock in ticker_stock.items():
# 	add_investment("Stock", ticker, stock, ticker_stock_image_link[ticker])

# for ticker, crypto in ticker_crypto.items():
# 	add_investment("Crypto", ticker, crypto, ticker_stock_image_link[ticker])

