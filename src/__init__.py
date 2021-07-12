from flask import Flask, render_template, session, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, asc, Float
from sqlalchemy.orm.attributes import InstrumentedAttribute
from .stock_info import *
import os
import flask_login
from flask_login import LoginManager, UserMixin
from .new_investment import add_investment

login_manager = LoginManager()


app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.secret_key = 'key'

DATABASE_URL = "postgresql://aaclbzejzdxebt:eba4ca8018075b68e2c553d37745eb9b16194d663c1fd15ba85c7e3c934fae64@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d119nni8ln3u0i"
# DATABASE_URL = os.environ['DATABASE_URL']


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager.init_app(app)

# if 0 --> April 15, 2020 --> check 1
# if 1 --> check 2
# if 2 --> check 3
check_number = 0

users = {'abhig':{'password': 'hello123'}}

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

def top(investment):
    query = []
    for ticker, stock in investment.items():
        price = Investments.query.order_by(Investments.id.desc()).filter_by(ticker=ticker).first()
        if not check_number:
            price = float(price.first_check)
        elif check_number == 1:
            price = float(price.second_check)
        elif check_number == 2:
            price = float(price.third_check)
        query.append([stock.lower(), ticker, price, int((price-1200)/12), ticker_stock_image_link.get(ticker)])

    query.sort(key = lambda x: x[2], reverse = True)

    for entry in query:
        entry[2] = "{:,.2f}".format(entry[2])
    return query


@app.route("/")
def home():
    return render_template("overview.html", investment_list=top(ticker_investment))

@app.route("/stocks")
def stocks():
    return render_template("overview.html", investment_list=top(ticker_stock))


@app.route("/cryptos")
def cryptos():
    return render_template("overview.html", investment_list=top(ticker_crypto))

@app.route("/<stock_ticker>")
def stock(stock_ticker):
    try:
        stock_data = Investments.query.filter_by(ticker=stock_ticker).order_by(Investments.id.desc()).first()
        if not check_number:
            price = float(stock_data.first_check)
        else:
            price = float(stock_data.second_check)
        return render_template("stock.html", stock_name=stock_data.stock, stock_ticker=stock_ticker, 
        stock_price = "{:,.2f}".format(price), last_updated = format_time(stock_data.updated),
        percentage = int((price-1200)/12), image_link = ticker_stock_image_link.get(stock_ticker))
    except Exception as e:
        if(stock_ticker in ticker_investment.values()):
            return stock(list(ticker_investment.keys())[list(ticker_investment.values()).index(stock_ticker)])
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
                return redirect(url_for('protect'))
        else:
            return render_template('admin.html')
    return render_template('admin.html')

@app.route('/protect', methods=['GET', 'POST'])
@flask_login.login_required
def protect():
    if request.method == 'POST':
        if 'logout' in request.form:
            return redirect(url_for('logout'))
        else:
            return render_template(add_investment(request.form.get('investment_type'), request.form.get('ticker'), request.form.get('name'), request.form.get('image_link')))
    return render_template('protected.html')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))


