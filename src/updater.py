import time as clock
import os
import psycopg2
import bs4
import requests
from bs4 import BeautifulSoup
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# get headers randomizer
headers = { 
    'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'DNT'             : '1', # Do Not Track Request Header 
    'Connection'      : 'close'
}



DATABASE_URL = os.environ['DATABASE_URL']
# DATABASE_URL = "postgresql://aaclbzejzdxebt:eba4ca8018075b68e2c553d37745eb9b16194d663c1fd15ba85c7e3c934fae64@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d119nni8ln3u0i"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()


def get_curr_time():
	return datetime.datetime.now().strftime('%m-%d-%Y %I:%M:%S %p')
	# return('07-12-2021 01:00:00 PM')

def get_all_curr_values(curr_price, first_check_val, second_check_val, third_check_val):
	first_val = "{0:.2f}".format(1200/float(first_check_val)*curr_price)
	second_val = "{0:.2f}".format(600/float(second_check_val)*curr_price)
	third_val = "{0:.2f}".format(1400/float(third_check_val)*curr_price)
	return [first_val, second_val, third_val]


def update_stocks():
	c.execute('select * from stocks')
	for x in c.fetchall():
		ticker = x[0]
		stock = x[1]
		print(ticker)
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker, hedaers = headers, timeout=10)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		c.execute('select * from stocks where ticker=' + f"'{ticker}'")
		row=c.fetchall()[0]
		vals = get_all_curr_values(price, row[3], row[4], row[5])
		c.execute('insert into investments (ticker, stock, price, updated, first_check, second_check, third_check) values (%s,%s,%s,%s,%s,%s,%s)', [ticker, stock, price, get_curr_time(), vals[0], vals[1], vals[2]])
		clock.sleep(10)
	conn.commit()


def update_cryptos():
	c.execute('select * from cryptos')
	for x in c.fetchall():
		ticker = x[0]
		stock = x[1]
		print(ticker)
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD?p=' + ticker + '-USD', headers = headers, timeout=10)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		c.execute('select * from cryptos where ticker=' + f"'{ticker}'")
		row=c.fetchall()[0]
		vals = get_all_curr_values(price, row[3], row[4], row[5])
		c.execute('insert into investments (ticker, stock, price, updated, first_check, second_check, third_check) values (%s,%s,%s,%s,%s,%s,%s)', [ticker, stock, price, get_curr_time(), vals[0], vals[1], vals[2]])
		clock.sleep(10)
	conn.commit()

# try:
# 	update_cryptos()
# 	update_stocks()
# except Exception as e:
# 	print(e)


scheduler = BlockingScheduler(timezone = 'America/Los_Angeles')
scheduler.add_job(update_cryptos, 'interval', hours=1, start_date = '2021-06-05 23:00:00')
scheduler.add_job(update_stocks, 'cron', day_of_week='mon-fri', hour=6, minute=31)
scheduler.add_job(update_stocks, 'cron', day_of_week='mon-fri', hour='7-13')
scheduler.start()

