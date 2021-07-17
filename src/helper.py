import psycopg2
from .new_investment import add_investment
from .network_utils import *


conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

# ticker_list = ["AAPL", "GOOGL", "FB", "NKE", "BAC", "AMZN", "CVS", "NFLX", "PFE", "VZ", "T"]

# c.execute('select * from stocks')
# for record in c.fetchall():
# 	if record[0] in ticker_list:
# 		add_investment("Stock", record[0], record[1], "https://eodhistoricaldata.com/img/logos/US/" + record[0].lower() + ".png")


c.execute('select * from stocks')
for stock in c.fetchall():
	sql = 'insert into assets (ticker, stock, investment_type, image_link, first_check_val, second_check_val, third_check_val) values (%s,%s,%s,%s,%s,%s,%s)'
	c.execute(sql, [stock[0], stock[1], "Stock", stock[2], stock[3], stock[4], stock[5]])
c.execute('select * from cryptos')
for stock in c.fetchall():
	sql = 'insert into assets (ticker, stock, investment_type, image_link, first_check_val, second_check_val, third_check_val) values (%s,%s,%s,%s,%s,%s,%s)'
	c.execute(sql, [stock[0], stock[1], "Crypto", stock[2], stock[3], stock[4], stock[5]])
conn.commit()