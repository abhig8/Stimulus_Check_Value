import psycopg2


DATABASE_URL = "postgresql://aaclbzejzdxebt:eba4ca8018075b68e2c553d37745eb9b16194d663c1fd15ba85c7e3c934fae64@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d119nni8ln3u0i"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

# c.execute('insert into stocks (ticker, stock, image_link, first_check_val, second_check_val, third_check_val) values (%s,%s,%s,%s,%s,%s)', ["AMC", "AMC THEATRES", "https", "0", "0", "0"])
# conn.commit()


c.execute('select * from ' + "stocks" + " where ticker=" + "'AMC'")
row = c.fetchall()
print(row)

# c.execute('select * from stocks')
# records = c.fetchall()
# print(records)

# import bs4
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime

# headers = { 
#     'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
#     'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
#     'Accept-Language' : 'en-US,en;q=0.5',
#     'DNT'             : '1', # Do Not Track Request Header 
#     'Connection'      : 'close'
# }

# print(datetime.fromtimestamp(1586822400))

# date1 = str(datetime.strptime("04.14.2020", '%m.%d.%Y').timestamp())
# print(date1)
# print(1586822400)
# date2 =  str(datetime.strptime("04.16.2020", '%m.%d.%Y').timestamp())
# print(date2)
# print(1586995200)

# url = requests.get('https://finance.yahoo.com/quote/' + 'AMC' + '/history?period1=' + date1 + '&period2=' + date2 + '&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true', headers=headers, timeout=5)
# # url = requests.get("https://finance.yahoo.com/quote/AMC?p=AMC")
# soup = bs4.BeautifulSoup(url.text, features="lxml")
# # print(soup.prettify())

# table = soup.find("table", attrs={'class': 'W(100%) M(0)'})
# table_body = table.find('tbody')
# row_1 = table_body.find('tr').find_all('td')
# lowest_price = row_1[3]
# print(lowest_price.find("span").text.replace(',',''))


# # url = requests.get('https://finance.yahoo.com/quote/' + 'AMC' + '/history?period1=1586822400&period2=1586995200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true', headers=headers, timeout=5)
# # soup = bs4.BeautifulSoup(url.text, features="lxml")
# # table = soup.find("table", attrs={'class': 'W(100%) M(0)'})
# # table_body = table.find('tbody')
# # row_1 = table_body.find('tr').find_all('td')
# # lowest_price = row_1[3].find("span").text.replace(',','')

# print(datetime.strptime("04.15.2020", '%m.%d.%Y').timestamp())