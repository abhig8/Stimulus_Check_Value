import os
import psycopg2
import bs4
import requests
from bs4 import BeautifulSoup
import datetime

DATABASE_URL = "postgresql://aaclbzejzdxebt:eba4ca8018075b68e2c553d37745eb9b16194d663c1fd15ba85c7e3c934fae64@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d119nni8ln3u0i"

headers = { 
    'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'DNT'             : '1', # Do Not Track Request Header 
    'Connection'      : 'close'
}
#get headers randomizer

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

def add_investment(investment_type, ticker, name, image_link):
	try: 
		if investment_type == "Stock":
			first_date_value, second_date_value, third_date_value = add_stock(ticker, name)
		elif investment_type == "Crypto":
			first_date_value, second_date_value, third_date_value = add_crypto(ticker, name)
		c.execute('insert into stocks (ticker, stock, image_link, first_check_val, second_check_val, third_check_val) values (%s,%s,%s,%s,%s,%s) on conflict(ticker) do update set stock=EXCLUDED.stock, image_link=EXCLUDED.image_link, first_check_val=EXCLUDED.first_check_val, second_check_val=EXCLUDED.second_check_val, third_check_val=EXCLUDED.third_check_val', [ticker, name, image_link , first_date_value, second_date_value, third_date_value])
		conn.commit()
		update_investment(ticker, name, investment_type)
	except:
		pass
		# need to display error that program was unable to scrape the specifi ivnestment & ticker or picture
	return "protected.html"
	# figure out way to add success image pop-up investment is added
	# figure out way to scrape Stock name once the ticker is entered and allow the user to change it if they wish
	# figure out way to quickly scrape images from all possible links and allow the user to select options or input custom link

# finding date check date 1: April 15, 2020
# finding date check date 2: December 29th, 2020
# finding date check date 3: March 16th, 2021
def add_stock(ticker, name):
	def get_lowest_price(ticker, date):
		if date == 1:
			timestamp1 = '1586908800'
			timestamp2 = '1586995200'
		elif date == 2:
			timestamp1 = '1609200000'
			timestamp2 = '1609286400'
		elif date == 3:
			timestamp1 = '1615852800'
			timestamp2 = '1615939200'
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '/history?period1=' + str(timestamp1) + '&period2=' + str(timestamp2) + '&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true', headers=headers, timeout=5)
		soup = bs4.BeautifulSoup(url.text, features="lxml")
		table = soup.find("table", attrs={'class': 'W(100%) M(0)'})
		table_body = table.find('tbody')
		row_1 = table_body.find('tr').find_all('td')
		return row_1[3].find("span").text.replace(',','')
	return get_lowest_price(ticker, 1), get_lowest_price(ticker, 2), get_lowest_price(ticker, 3)

def add_crypto(ticker, name):
	def get_lowest_price(ticker, date):
		if date == 1:
			timestamp1 = '1586908800'
			timestamp2 = '1586995200'
		elif date == 2:
			timestamp1 = '1609200000'
			timestamp2 = '1609286400'
		elif date == 3:
			timestamp1 = '1615852800'
			timestamp2 = '1615939200'
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD/history?period1=' + timestamp1 + '&period2=' + timestamp2 + '&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true', headers=headers, timeout=5)
		soup = bs4.BeautifulSoup(url.text, features="lxml")
		table = soup.find("table", attrs={'class': 'W(100%) M(0)'})
		table_body = table.find('tbody')
		row_1 = table_body.find('tr').find_all('td')
		return row_1[3].find("span").text.replace(',','')
	return get_lowest_price(ticker, 1), get_lowest_price(ticker, 2), get_lowest_price(ticker, 3)

def get_all_curr_values(ticker, tablename, curr_price):
	c.execute('select * from ' + tablename + ' where ticker=' + 'ticker')
	row = c.fetchall()[0]
	first_val = "{0:.2f}".format(1200/float(row[3])*curr_price)
	second_val = "{0:.2f}".format(1200/float(row[4])*curr_price)
	third_val = "{0:.2f}".format(1200/float(row[5])*curr_price)
	return [first_val, second_val, third_val]

def update_investment(ticker, name, investment_type):
	if investment_type == "Stock":
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker)
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		tablename = 'stocks'
	elif investment_type == "Crypto":
		url = requests.get('https://finance.yahoo.com/quote/' + ticker + '-USD?p=' + ticker + '-USD')
		soup = bs4.BeautifulSoup(url.text, features="html.parser")
		price = float(soup.find_all("div", {'class': 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)'})[0].find('span').text.replace(',',''))
		tablename = 'cryptos'
	# time = datetime.datetime.now().strftime('%m-%d-%Y %I:%M:%S %p')
	time = "07-09-2021 01:00:00 PM"
	values = get_all_curr_values(ticker, tablename, float(price))
	c.execute('insert into investments (ticker, stock, price, updated, first_check, second_check, third_check) values (%s,%s,%s,%s,%s,%s,%s)', [ticker, name, price, time, values[0], values[1], values[2]])
	conn.commit()

# add_crypto("BTC", "Bitcoin", "")
# print(first_date_value, second_date_value, third_date_value, ticker, name)

# c.execute('select * from stocks')
# records = c.fetchall()
# print(records)

# website_link = ""
