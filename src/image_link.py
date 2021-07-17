import bs4
import requests
from bs4 import BeautifulSoup
from .network_utils import *
import lxml
import wget
import psycopg2

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()

# def stocks_image_scraper(ticker, stock):
# 	if ticker == "CVS":
# 		url = "https://www.crunchbase.com/organization/cvs-caremark"
# 	elif ticker == "LEVI":
# 		url = "https://www.crunchbase.com/organization/levi-s"
# 	else:
# 		url = "https://www.crunchbase.com/organization/" + stock.replace('&', '-').replace("'", '-').replace(" ", '-').lower()
# 	url = requests.get(url, headers=headers)
# 	soup = bs4.BeautifulSoup(url.text, features="lxml")
# 	image = soup.find_all('img')
# 	print(image.find('_ngcontent-client-app-c186'))
# 	# div = soup.find("img", attrs={'class': 'provide-styling'}).find('img')
# stocks_image_scraper("PYPL", "PAYPAL")


def testwget(image_name, url):
    wget.download(url, out='./src/static/assets/img/' + image_name)


c.execute('select * from cryptos')
for stock in c.fetchall():
    if stock[2][-1] == '0':
        image_link = stock[2][:-6]
    else:
        image_link = stock[2]
    # print(stock[0], image_link)
    testwget(stock[0] + '.png', image_link)



# testwget('NFLX.png','https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_1/v1474467529/zlaaxu2whczitkpkxxk9.jpg')




# ## Set up the image URL and filename
# image_url = "https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_1/v1474467529/zlaaxu2whczitkpkxxk9.jpg"
# filename = image_url.split("/")[-1]

# # Open the url image, set stream to True, this will return the stream content.
# r = requests.get(image_url, stream = True)

# # Check if the image was retrieved successfully
# if r.status_code == 200:
#     # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
#     r.raw.decode_content = True
    
#     # Open a local file with wb ( write binary ) permission.
#     with open(filename,'wb') as f:
#         shutil.copyfileobj(r.raw, f)
        
#     print('Image sucessfully Downloaded: ',filename)
# else:
#     print('Image Couldn\'t be retreived')
# view raw