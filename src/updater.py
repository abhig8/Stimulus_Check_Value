# import pandas
# from alpha_vantage.timeseries import TimeSeries 
# from alpha_vantage.cryptocurrencies import CryptoCurrencies
# import sqlite3
import schedule
import time as clock
from stock_info import ticker_stock, ticker_crypto, ticker_price_april, ticker_price_december, ticker_investment
import os
import psycopg2
import bs4
import requests
from bs4 import BeautifulSoup
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler



# DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = "postgresql://aaclbzejzdxebt:eba4ca8018075b68e2c553d37745eb9b16194d663c1fd15ba85c7e3c934fae64@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d119nni8ln3u0i"


# import matplotlib.pyplot as plt

# API_KEY = ""

# #testing output
# time = TimeSeries(key=key, output_format="pandas")
# cc = CryptoCurrencies(key=key, output_format="pandas")
# data = time.get_intraday(symbol="GOOGL", interval="1min", outputsize = "compact")
# print(data)
# data = cc.get_digital_currency_daily(symbol="XRP", market='USD')
# print(data)

# time = TimeSeries(key=API_KEY)
# cc = CryptoCurrencies(key=API_KEY)

# data = time.get_intraday(symbol="CSCO", interval="1min", outputsize = "comapct")
# print(data)
# print(list(data[0].keys())[0])
# print(float(list(data[0].values())[0].get("1. open")))

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#conn = sqlite3.connect(os.path.realpath('src/stock.db'))
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


# def total_update():
# 	print("starting...")
# 	new_data = update_stocks()+update_cryptos()
# 	for investment in new_data:
# 		# c.execute('insert into stock (ticker, stock, price, updated, first_check) values (?,?,?,?,?)', investment)
# 		c.execute('insert into stock (ticker, stock, price, updated, first_check) values (%s,%s,%s,%s,%s)', investment)
# 	conn.commit()
# 	print("done")
def update_stocks():
	stock_list = []
	for ticker, stock in ticker_stock.items():
		# data = time.get_intraday(symbol=ticker, interval="1min", outputsize = "comapct")
		# date_time = (list(data[0].keys())[0]).strip()
		# price = float(list(data[0].values())[0].get("1. open"))
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		date_time = datetime.datetime.now().strftime('%m-%d-%Y %I:%M:%S %p')
		first_check =  "{0:.2f}".format(1200/ticker_price_april.get(ticker)*price)
		stock_list.append([ticker, stock, price, date_time, first_check])
		# clock.sleep(12)
	# return stock_list
	for investment in stock_list:
		# c.execute('insert into stock (ticker, stock, price, updated, first_check) values (?,?,?,?,?)', investment)
		c.execute('insert into stock (ticker, stock, price, updated, first_check) values (%s,%s,%s,%s,%s)', investment)
	conn.commit()
def update_cryptos():
	crypto_list = []
	for ticker, crypto in ticker_crypto.items():
		# data = cc.get_digital_currency_daily(symbol=ticker, market='USD')
		# latest_date = (list(data[0].keys())[0]).strip()
		# price = float(list(data[0].values())[0].get("2a. high (USD)"))
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD?p=' + ticker + '-USD')
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		date_time = datetime.datetime.now().strftime('%m-%d-%Y %I:%M:%S %p')
		first_check =  "{0:.2f}".format(1200/ticker_price_april.get(ticker)*price)
		crypto_list.append([ticker, crypto, price, date_time, first_check])
		# clock.sleep(12)
		# crypto_list.append([ticker, ticker_crypto.get(ticker), price, latest_date + " " + update_time + ":00", first_check])
	# return crypto_list
	for investment in crypto_list:
		# c.execute('insert into stock (ticker, stock, price, updated, first_check) values (?,?,?,?,?)', investment)
		c.execute('insert into stock (ticker, stock, price, updated, first_check) values (%s,%s,%s,%s,%s)', investment)
	conn.commit()

def update_investment(ticker, investment_type):
	if investment_type == "stock":
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker)
		investment = ticker_investment.get(ticker)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
	else:
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD?p=' + ticker + '-USD')
		investment = ticker_investment.get(ticker)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
	date_time = datetime.datetime.now().strftime('%m-%d-%Y %I:%M:%S %p')
	first_check =  "{0:.2f}".format(1200/ticker_price_april.get(ticker)*price)
	c.execute('insert into stock (ticker, stock, price, updated, first_check) values (%s,%s,%s,%s,%s)', [ticker, investment, price, date_time, first_check])

# update_cryptos()
# update_stocks()

#update_investment("T", "stock")



scheduler = BlockingScheduler(timezone = 'America/Los_Angeles')
scheduler.add_job(update_cryptos, 'interval', hours=1, start_date = '2021-06-05 23:00:00')
scheduler.add_job(update_stocks, 'cron', day_of_week='mon-fri', hour=6, minute=31)
scheduler.add_job(update_stocks, 'cron', day_of_week='mon-fri', hour='7-13')
scheduler.start()

# update_time = "12:00"


# schedule.every().day.at(update_time).do(total_update)

# while 1:
# 	schedule.run_pending()

