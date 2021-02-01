import pandas
from alpha_vantage.timeseries import TimeSeries 
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from datetime import datetime
import sqlite3
import schedule
import time as clock
from stock_info import ticker_stock, ticker_crypto, ticker_price_april, ticker_price_december
import os
# import matplotlib.pyplot as plt

API_KEY = "POK3LC990DZ9598A"

# #testing output
# time = TimeSeries(key=key, output_format="pandas")
# cc = CryptoCurrencies(key=key, output_format="pandas")
# data = time.get_intraday(symbol="GOOGL", interval="1min", outputsize = "compact")
# print(data)
# data = cc.get_digital_currency_daily(symbol="XRP", market='USD')
# print(data)

time = TimeSeries(key=API_KEY)
cc = CryptoCurrencies(key=API_KEY)

# data = time.get_intraday(symbol="GOOGL", interval="1min", outputsize = "comapct")
# print(list(data[0].keys())[0])
# print(float(list(data[0].values())[0].get("1. open")))

conn = sqlite3.connect(os.path.realpath('src/stock.db'))
c = conn.cursor()

# def total_update():
# 	new_data = update_stocks()
# 	for investment in new_data:
# 		c.execute('insert into stock (ticker, stock, price, updated, first_check) values (?,?,?,?,?)', investment)
# 	conn.commit()
# 	print("done")
# def update_stocks():
# 	stock_list = []
# 	for ticker in ticker_stock.keys():
# 		data = time.get_intraday(symbol=ticker, interval="1min", outputsize = "comapct")
# 		latest_time = (list(data[0].keys())[0]).strip()
# 		price = float(list(data[0].values())[0].get("1. open"))
# 		first_check =  "{0:.2f}".format(1200/ticker_price_april.get(ticker)*price)
# 		stock_list.append([ticker, ticker_stock.get(ticker), price, latest_time, first_check])
# 		return stock_list

def total_update():
	print("starting...")
	new_data = update_stocks()+update_cryptos()
	for investment in new_data:
		c.execute('insert into stock (ticker, stock, price, updated, first_check) values (?,?,?,?,?)', investment)
	conn.commit()
	print("done")
def update_stocks():
	stock_list = []
	for ticker in ticker_stock.keys():
		data = time.get_intraday(symbol=ticker, interval="1min", outputsize = "comapct")
		latest_time = (list(data[0].keys())[0]).strip()
		price = float(list(data[0].values())[0].get("1. open"))
		first_check =  "{0:.2f}".format(1200/ticker_price_april.get(ticker)*price)
		stock_list.append([ticker, ticker_stock.get(ticker), price, latest_time, first_check])
		clock.sleep(12)
	return stock_list
def update_cryptos():
	crypto_list = []
	for ticker in ticker_crypto.keys():
		data = cc.get_digital_currency_daily(symbol=ticker, market='USD')
		latest_date = (list(data[0].keys())[0]).strip()
		price = float(list(data[0].values())[0].get("2a. high (USD)"))
		first_check =  "{0:.2f}".format(1200/ticker_price_april.get(ticker)*price)
		crypto_list.append([ticker, ticker_crypto.get(ticker), price, latest_date + " 00:00:00", first_check])
		clock.sleep(12)
	return crypto_list

schedule.every().day.at("22:19").do(total_update)

while 1:
	schedule.run_pending()

