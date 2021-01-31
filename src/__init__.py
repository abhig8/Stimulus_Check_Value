from flask import Flask, render_template, session, request, url_for, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, asc, Float
from datetime import datetime
from .stock_info import ticker_investment
from sqlalchemy.orm.attributes import InstrumentedAttribute

app = Flask(__name__)

db_name = "stock.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
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

def get_standard_time(date_time):
	date = datetime.strptime(date_time[:10], '%Y-%m-%d').strftime('%m-%d-%Y')
	time = date_time[11:]
	hour = int(time[:2])
	is_am = hour < 12
	if not is_am:
		hour -=12
	if not hour:
		hour = 12
	time = str(hour) + time[2:]
	if is_am:
		 time += " AM "
	else:
		time += " PM "
	time += "EST"
	return date + " @ " + time

def top_stocks(number):
	recent_stocks = Stock.query.order_by(Stock.id.desc()).limit(len(ticker_investment)).all()
	recent_stocks.sort(key=lambda x: float(x.first_check), reverse=True)
	card_values = []
	for x in range(number):
		if not check_number:
			price = float(recent_stocks[x].first_check)
		else:
			price = float(recent_stocks[x].second_check)
		card_values.append([recent_stocks[x].stock, recent_stocks[x].ticker, "{:,.2f}".format(price), int((price-1200)/12)])
	return card_values

@app.route("/")
def home():
	top = top_stocks(8)
	return render_template("home.html", top_4 = top[:4], last_4 = top[4:])

@app.route("/<stock_ticker>")
def stock(stock_ticker):
	try:
		stock_data = Stock.query.filter_by(ticker=stock_ticker).order_by(Stock.id.desc()).first()
		if not check_number:
			price = float(stock_data.first_check)
		else:
			price = float(stock_data.second_check)
		return render_template("stock.html", stock_name=stock_data.stock, stock_ticker=stock_ticker, 
		stock_price = "{:,.2f}".format(price), last_updated = get_standard_time(stock_data.updated),
		percentage = int((price-1200)/12))
	except:
		return error(stock_ticker)


@app.route("/search")
def search():
	return stock(request.args.get("q").upper())

@app.route("/error/<stock_ticker>")
def error(stock_ticker):
	return render_template("error.html", error_stock=stock_ticker)

@app.route("/overview")
def overview():
	return render_template("overview.html", investment_list=top_stocks(len(ticker_investment)))


# if __name__ == "__main__":
# 	app.run(debug=False)
# 	# app.run()




