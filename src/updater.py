import time as clock
import os
import psycopg2
import bs4
import requests
from bs4 import BeautifulSoup
import datetime
from stock_info import ticker_stock, ticker_crypto, ticker_price_april, ticker_price_december, ticker_investment
from apscheduler.schedulers.blocking import BlockingScheduler



DATABASE_URL = os.environ['DATABASE_URL']
# DATABASE_URL = "postgresql://aaclbzejzdxebt:eba4ca8018075b68e2c553d37745eb9b16194d663c1fd15ba85c7e3c934fae64@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d119nni8ln3u0i"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()


def get_time():
	return datetime.datetime.now().strftime('%m-%d-%Y %I:%M:%S %p')

def get_first_check_val(ticker, curr_price):
	return "{0:.2f}".format(1200/ticker_price_april.get(ticker)*curr_price)

def update_stocks():
	for ticker, stock in ticker_stock.items():
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		c.execute('insert into stock (ticker, stock, price, updated, first_check) values (%s,%s,%s,%s,%s)', [ticker, stock, price, get_time(), get_first_check_val(ticker, price)])
		clock.sleep(10)
	conn.commit()

def update_cryptos():
	for ticker, crypto in ticker_crypto.items():
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD?p=' + ticker + '-USD')
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		c.execute('insert into stock (ticker, stock, price, updated, first_check) values (%s,%s,%s,%s,%s)', [ticker, crypto, price, get_time(), get_first_check_val(ticker, price)])
		clock.sleep(10)
	conn.commit()

def update_investment(ticker, investment_type):
	if investment_type == "stock":
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
	else:
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD?p=' + ticker + '-USD')
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
	investment = ticker_investment.get(ticker)
	c.execute('insert into stock (ticker, stock, price, updated, first_check) values (%s,%s,%s,%s,%s)', [ticker, investment, price, get_time(), get_first_check_val(ticker, price)])
	conn.commit()

# update_cryptos()
# update_stocks()

# update_investment("T", "stock")

scheduler = BlockingScheduler(timezone = 'America/Los_Angeles')
scheduler.add_job(update_cryptos, 'interval', hours=1, start_date = '2021-06-05 23:00:00')
scheduler.add_job(update_stocks, 'cron', day_of_week='mon-fri', hour=6, minute=31)
scheduler.add_job(update_stocks, 'cron', day_of_week='mon-fri', hour='7-13')
scheduler.start()

