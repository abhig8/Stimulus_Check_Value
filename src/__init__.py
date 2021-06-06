from flask import Flask, render_template, session, request, url_for, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, asc, Float
from .stock_info import ticker_investment, DATABASE_URL, ticker_stock_image_link
import os
from sqlalchemy.orm.attributes import InstrumentedAttribute

app = Flask(__name__, template_folder = "templates", static_folder = "static")

# db_name = "stock.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

check_number = 0

class Stock(db.Model):
    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    ticker = db.Column(db.String())
    stock = db.Column(db.String())
    price = db.Column(db.Float)
    updated = db.Column(db.String())
    first_check = db.Column(db.String())

    def __init__(self, ticker, stock, price, updated, first_check):
    	self.ticker = ticker
    	self.stock = stock
    	self.price = price
    	self.updated = updated
    	self.first_check = first_check

def format_time(date_time):
	return date_time[:10] + " @" + date_time[10:] + " " + "PST"

def top_stocks():
	query = []
	for ticker, stock in ticker_investment.items():
		price = Stock.query.order_by(Stock.id.desc()).filter_by(ticker=ticker).first()
		if not check_number:
			price = float(price.first_check)
		else:
			price = float(price.second_check)

		query.append([stock.lower(), ticker, price, int((price-1200)/12), ticker_stock_image_link.get(ticker)])

	query.sort(key = lambda x: x[2], reverse = True)

	for entry in query:
		entry[2] = "{:,.2f}".format(entry[2])
	return query

	# # recent_stocks = Stock.query.order_by(Stock.id.desc()).limit(len(ticker_investment)).all()
	# # recent_stocks.sort(key=lambda x: float(x.first_check), reverse=True)
	# query.sort(key=lambda x: float(x.first_check), reverse=True)
	# # card_values = []
	# for x in range(len(query)):
	# 	# print(recent_stocks[x].ticker)
	# 	if not check_number:
	# 		price = float(query[x].first_check)
	# 	else:
	# 		price = float(query[x].second_check)
	# 	# card_values.append([x.stock.lower(), x.ticker, "{:,.2f}".format(price), int((price-1200)/12)])
	# 	query[x] = [query[x].stock.lower(), query[x].ticker, "{:,.2f}".format(price), int((price-1200)/12)]
	# return query

# @app.route("/")
# def home():
# 	top = top_stocks(8)
# 	return render_template("home.html", top_4 = top[:4], last_4 = top[4:])

@app.route("/")
def home():
	return render_template("overview.html", investment_list=top_stocks())

@app.route("/<stock_ticker>")
def stock(stock_ticker):
	try:
		stock_data = Stock.query.filter_by(ticker=stock_ticker).order_by(Stock.id.desc()).first()
		if not check_number:
			price = float(stock_data.first_check)
		# else:
		# 	price = float(stock_data.second_check)
		return render_template("stock.html", stock_name=stock_data.stock, stock_ticker=stock_ticker, 
		stock_price = "{:,.2f}".format(price), last_updated = format_time(stock_data.updated),
		percentage = int((price-1200)/12), image_link = ticker_stock_image_link.get(stock_ticker))
	except:
		if(stock_ticker in ticker_investment.values()):
			return stock(list(ticker_investment.keys())[list(ticker_investment.values()).index(stock_ticker)])
		return error(stock_ticker)

@app.route("/search")
def search():
	return stock(request.args.get("q").upper())

@app.route("/error/<stock_ticker>")
def error(stock_ticker):
	return render_template("error.html", error_stock=stock_ticker)

# @app.route("/overview")
# def overview():
# 	return render_template("overview.html", investment_list=top_stocks(len(ticker_investment)))


# if __name__ == "__main__":
# 	app.run(debug=False)
# 	# app.run()





