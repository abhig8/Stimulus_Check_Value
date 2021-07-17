import time as clock
import psycopg2
import bs4
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from .utils import get_curr_time, get_all_curr_values
from .network_utils import *

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

def update_stocks():
	c.execute('select * from assets where investment_type=%s', ('Stock',))
	for x in c.fetchall():
		ticker = x[0]
		stock = x[1]
		print(ticker)
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker, headers = headers, timeout=10)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		c.execute('select * from stocks where ticker=' + f"'{ticker}'")
		row = c.fetchall()
		print(row)
		row = row[0]
		vals = get_all_curr_values(price, row[3], row[4], row[5])
		sql = ('insert into investments (ticker, stock, price, updated, first_check, second_check, third_check) values (%s,%s,%s,%s,%s,%s,%s)')
		c.execute(sql, [ticker, stock, price, get_curr_time(), vals[0], vals[1], vals[2]])
		clock.sleep(10)
	conn.commit()


def update_cryptos():
	c.execute('select * from assets where investment_type=%s', ('Crypto',))
	for x in c.fetchall():
		ticker = x[0]
		stock = x[1]
		print(ticker)
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD?p=' + ticker + '-USD', headers = headers, timeout=10)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		c.execute('select * from cryptos where ticker=' + f"'{ticker}'")
		row = c.fetchall()
		print(row)
		row = row[0]
		vals = get_all_curr_values(price, row[3], row[4], row[5])
		sql = ('insert into investments (ticker, stock, price, updated, first_check, second_check, third_check) values (%s,%s,%s,%s,%s,%s,%s)')
		c.execute(sql, [ticker, stock, price, get_curr_time(), vals[0], vals[1], vals[2]])
		clock.sleep(10)
	conn.commit()


# try:
# 	update_cryptos()
# 	# update_stocks()
# except Exception as e:
# 	print('here')
# 	print(e)


scheduler = BlockingScheduler(timezone = 'America/Los_Angeles', executors={'default': ProcessPoolExecutor(max_workers=1)}, job_defaults={'misfire_grace_time': 10 * 60})
scheduler.add_job(update_cryptos, 'interval', hours=1, start_date = '2021-06-05 23:00:00')
scheduler.add_job(update_stocks, 'cron', day_of_week='mon-fri', hour=6, minute=31)
scheduler.add_job(update_stocks, 'cron', day_of_week='mon-fri', hour='7-13')
scheduler.start()

