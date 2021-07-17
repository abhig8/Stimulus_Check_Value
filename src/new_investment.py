import psycopg2
import bs4
import requests
from bs4 import BeautifulSoup
from .utils import get_curr_time, get_timestamp, get_all_curr_values
from .network_utils import *

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

def add_investment(investment_type, ticker, name, image_link):
	try: 
		if investment_type == "Stock":
			first_date_value, second_date_value, third_date_value = get_lowest_price(ticker, 1, "Stock"), get_lowest_price(ticker, 2, "Stock"), get_lowest_price(ticker, 3, "Stock")
			sql = ('insert into assets (ticker, stock, investment_type, image_link, first_check_val, second_check_val, third_check_val) values (%s,%s,%s,%s,%s,%s,%s) ' 
				   'on conflict(ticker) do update set stock=EXCLUDED.stock, image_link=EXCLUDED.image_link, investment_type=EXCLUDED.investment_type,'
				   'first_check_val=EXCLUDED.first_check_val, second_check_val=EXCLUDED.second_check_val, third_check_val=EXCLUDED.third_check_val')
		elif investment_type == "Crypto":
			first_date_value, second_date_value, third_date_value = get_lowest_price(ticker, 1, "Crypto"), get_lowest_price(ticker, 2, "Crypto"), get_lowest_price(ticker, 3, "Crypto")
			sql = ('insert into assets (ticker, stock, investment_type, image_link, first_check_val, second_check_val, third_check_val) values (%s,%s,%s,%s,%s,%s,%s) ' 
				   'on conflict(ticker) do update set stock=EXCLUDED.stock, image_link=EXCLUDED.image_link, investment_type=EXCLUDED.investment_type,'
				   'first_check_val=EXCLUDED.first_check_val, second_check_val=EXCLUDED.second_check_val, third_check_val=EXCLUDED.third_check_val')
		c.execute(sql, [ticker, name, investment_type, image_link , first_date_value, second_date_value, third_date_value])
		update_investment(ticker, name, investment_type, first_date_value, second_date_value, third_date_value)
		conn.commit()
	except Exception as e:
		print(e)
	return "protect_1"

def get_lowest_price(ticker, date, investment_type):
		timestamp1, timestamp2 = get_timestamp(date)
		if investment_type == "Stock":
			url = requests.get('https://finance.yahoo.com/quote/' + ticker + '/history?period1=' + str(timestamp1) + '&period2=' + str(timestamp2) + '&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true', headers=headers, timeout=10)
		elif investment_type == "Crypto":
			url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD/history?period1=' + timestamp1 + '&period2=' + timestamp2 + '&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true', headers=headers, timeout=10)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		table = soup.find("table", attrs={'class': 'W(100%) M(0)'})
		table_body = table.find('tbody')
		row_1 = table_body.find('tr').find_all('td')
		return row_1[3].find("span").text.replace(',','')

def update_investment(ticker, name, investment_type, first_check_val, second_check_val, third_check_val):
	if investment_type == "Stock":
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
	elif investment_type == "Crypto":
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD?p=' + ticker + '-USD')
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
	values = get_all_curr_values(float(price), first_check_val, second_check_val, third_check_val)
	sql = ('insert into investments (ticker, stock, price, updated, first_check, second_check, third_check) values (%s,%s,%s,%s,%s,%s,%s)')
	c.execute(sql, [ticker, name, price, get_curr_time(), values[0], values[1], values[2]])
	return
