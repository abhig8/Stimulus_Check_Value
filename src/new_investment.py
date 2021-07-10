import os
import psycopg2
import bs4
import requests
from bs4 import BeautifulSoup
import datetime

DATABASE_URL = "postgresql://aaclbzejzdxebt:eba4ca8018075b68e2c553d37745eb9b16194d663c1fd15ba85c7e3c934fae64@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d119nni8ln3u0i"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

def add_investment(investment_type, ticker, name):
	if investment_type == "Stock":
		add_stock(ticker, name)
	elif investment_type == "Crypto":
		add_crypto(ticker, name)

	return "overview.html"
	# need to return string for template to navigate to after this

def add_stock(ticker, name):
	url = requests.get('https://finance.yahoo.com/quote/' + ticker + '/history?period1=1586822400&period2=1586995200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')
	soup = bs4.BeautifulSoup(url.text, features="html.parser")
	first_date_value = float(soup.find_all("tr", {'class': 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})[0].find('span').text.replace(',',''))
	print(first_date_value)
	second_date_value = 0
	third_date_value = 0
	return

def add_crypto(ticker, name):
	url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD?p=' + ticker + '-USD')
	soup = bs4.BeautifulSoup(url.text, features="html.parser")
	first_date_value = 0
	second_date_value = 0
	third_date_value = 0
	price = float(soup.find_all("div", {'class': 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
	return


c.execute('select * from stocks')
records = c.fetchall()
# print(records)

logo_link = ""
website_link = ""
