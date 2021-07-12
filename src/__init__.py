from flask import Flask, render_template, session, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, asc, Float
from sqlalchemy.orm.attributes import InstrumentedAttribute
import os
import flask_login
from flask_login import LoginManager, UserMixin
from .new_investment import add_investment

login_manager = LoginManager()


app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.secret_key = 'key'

# DATABASE_URL = "postgresql://aaclbzejzdxebt:eba4ca8018075b68e2c553d37745eb9b16194d663c1fd15ba85c7e3c934fae64@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d119nni8ln3u0i"
DATABASE_URL = os.environ['DATABASE_URL']


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager.init_app(app)

# if 0 --> April 15, 2020 --> check 1
# if 1 --> check 2
# if 2 --> check 3
check_number = 0

users = {'abhig.123':{'password': 'myp@33w0.rd'}}

class Investments(db.Model):
    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    ticker = db.Column(db.String())
    stock = db.Column(db.String())
    price = db.Column(db.Float)
    updated = db.Column(db.String())
    first_check = db.Column(db.String())
    second_check = db.Column(db.String())
    third_check = db.Column(db.String())

    def __init__(self, ticker, stock, price, updated, first_check):
        self.ticker = ticker
        self.stock = stock
        self.price = price
        self.updated = updated
        self.first_check = first_check
        self.second_check = second_check
        self.third_check = third_check

class Stocks(db.Model):
    ticker = db.Column(db.String(), primary_key=True)
    stock = db.Column(db.String())
    image_link = db.Column(db.String())
    first_check_val = db.Column(db.String())
    second_check_val = db.Column(db.String())
    third_check_val = db.Column(db.String())

    def __init__(self, ticker, stock, price, updated, first_check):
        self.ticker = ticker
        self.stock = stock
        self.image_link = image_link
        self.first_check_val = first_check_val
        self.second_check_val = second_check_val
        self.third_check_val = third_check_val

class Cryptos(db.Model):
    ticker = db.Column(db.String(), primary_key=True)
    stock = db.Column(db.String())
    image_link = db.Column(db.String())
    first_check_val = db.Column(db.String())
    second_check_val = db.Column(db.String())
    third_check_val = db.Column(db.String())

    def __init__(self, ticker, stock, price, updated, first_check):
        self.ticker = ticker
        self.stock = stock
        self.image_link = image_link
        self.first_check_val = first_check_val
        self.second_check_val = second_check_val
        self.third_check_val = third_check_val

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return
    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == users[username]['password']
    return user



def format_time(date_time):
    return date_time[:10] + " at" + date_time[10:] + " " + "PST"


def top(investment_type):
    if investment_type == "Both":
        query = get_stocks() + get_cryptos()
    elif investment_type == "Crypto":
        query = get_cryptos()
    elif investment_type == "Stock":
        query = get_stocks()
    query.sort(key = lambda x: x[2], reverse = True)
    for entry in query:
        entry[2] = "{:,.2f}".format(entry[2])
    return query


def get_cryptos():
    query = []
    for x in Cryptos.query.all():
        price = Investments.query.order_by(Investments.id.desc()).filter_by(ticker=x.ticker).first()
        if not check_number:
            price = float(price.first_check)
        elif check_number == 1:
            price = float(price.second_check)
        elif check_number == 2:
            price = float(price.third_check)
        query.append([x.stock.lower(), x.ticker, price, int((price-1200)/12), x.image_link])
    return query

def get_stocks():
    query = []
    for x in Stocks.query.all():
        price = Investments.query.order_by(Investments.id.desc()).filter_by(ticker=x.ticker).first()
        if not check_number:
            price = float(price.first_check)
        elif check_number == 1:
            price = float(price.second_check)
        elif check_number == 2:
            price = float(price.third_check)
        query.append([x.stock.lower(), x.ticker, price, int((price-1200)/12), x.image_link])
    return query


def get_image_links(ticker, stock):
    link_1 = "https://eodhistoricaldata.com/img/logos/US/" + ticker.upper() + ".png"
    link_2 = "https://eodhistoricaldata.com/img/logos/US/" + ticker.lower() + ".png"
    link_3 = "https://cryptologos.cc/logos/" + stock.lower().replace(" ","-") + "-" + ticker.lower() + "-logo.png"
    return [link_1, link_2, link_3]

@app.route("/")
def home():
    return render_template("overview.html", investment_list=top("Both"))

@app.route("/stocks")
def stocks():
    return render_template("overview.html", investment_list=top("Stock"))


@app.route("/cryptos")
def cryptos():
    return render_template("overview.html", investment_list=top("Crypto"))

@app.route("/<stock_ticker>")
def stock(stock_ticker):
    for investment in Stocks.query.all():
        if stock_ticker == investment.ticker or stock_ticker == investment.stock:
            stock_data = Investments.query.filter_by(ticker=investment.ticker).order_by(Investments.id.desc()).first()
            if not check_number:
                price = float(stock_data.first_check)
            if check_number == 1:
                price = float(stock_data.second_check)
            if check_number == 2:
                price = float(stock_data.third_check)
            return render_template("stock.html", stock_name=stock_data.stock, stock_ticker=stock_data.ticker, 
            stock_price = "{:,.2f}".format(price), last_updated = format_time(stock_data.updated),
            percentage = int((price-1200)/12), image_link = investment.image_link)
    for investment in Cryptos.query.all():
        if stock_ticker == investment.ticker or stock_ticker == investment.stock:
            stock_data = Investments.query.filter_by(ticker=investment.ticker).order_by(Investments.id.desc()).first()
            if not check_number:
                price = float(stock_data.first_check)
            if check_number == 1:
                price = float(stock_data.second_check)
            if check_number == 2:
                price = float(stock_data.third_check)
            return render_template("stock.html", stock_name=stock_data.stock, stock_ticker=stock_data.ticker, 
            stock_price = "{:,.2f}".format(price), last_updated = format_time(stock_data.updated),
            percentage = int((price-1200)/12), image_link = investment.image_link)
    else:
        return error(stock_ticker)

@app.route("/search")
def search():
    return stock(request.args.get("q").upper())

@app.route("/error/<stock_ticker>")
def error(stock_ticker):
    return render_template("error.html", error_stock=stock_ticker)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        if username in users.keys():
            if request.form.get('password') == users[username]['password']:
                user = User()
                user.id = username
                flask_login.login_user(user)
                return redirect(url_for('protect_1'))
        else:
            return render_template('admin.html')
    return render_template('admin.html')

@app.route('/protect_1', methods=['GET', 'POST'])
@flask_login.login_required
def protect_1():
    if request.method == 'POST':
        if 'logout' in request.form:
            return redirect(url_for('logout'))
        else:
            return redirect(url_for("protect_2", investment_type=request.form.get('investment_type'), ticker=request.form.get('ticker'), stock=request.form.get('name')))
    return render_template('protected_1.html')

@app.route('/protect_2/<investment_type>/<ticker>/<stock>', methods=['GET', 'POST'])
@flask_login.login_required
def protect_2(investment_type, ticker, stock):
    if request.method == 'POST':
        if 'logout' in request.form:
            return redirect(url_for('logout'))
        else:
            if request.form.get('image_link') == "Image_Custom":
                image_link = request.form.get('custom_image_link')
            else:
                image_link = request.form.get('image_link')            
            return redirect(url_for(add_investment(request.form.get('investment_type'), request.form.get('ticker').upper(), request.form.get('name').upper(), image_link)))
    return render_template('protected_2.html', investment_type=investment_type, ticker=ticker, stock=stock, links=get_image_links(ticker, stock))

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))


