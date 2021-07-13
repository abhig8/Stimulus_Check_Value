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


# if 1: check date 1: April 15, 2020
# if 2: check date 2: December 29th, 2020
# finding date check date 3: March 16th, 2021
check_number = 1

check_number_overview_line = {
    1: "Possible gains on a $1200 investment made on April 15, 2020",
    2: "Possible gains on a $600 investment made on December 29, 2020",
    3: "Possible gains on a $1400 investment made on March 16, 2021"
}

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

def calculate_percentage(price):
    if check_number == 1:
        return int((price-1200)/12)
    elif check_number == 2:
        return int((price-600)/6)
    elif check_number == 3:
        return int((price-1400)/14)

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

def get_latest_value(row):
    if check_number == 1:
        return float(row.first_check)
    elif check_number == 2:
        return float(row.second_check)
    elif check_number == 3:
        return float(row.third_check)

def get_cryptos():
    query = []
    for x in Cryptos.query.all():
        value = get_latest_value(Investments.query.order_by(Investments.id.desc()).filter_by(ticker=x.ticker).first())
        query.append([x.stock.lower(), x.ticker, value, calculate_percentage(value), x.image_link])
    return query

def get_stocks():
    query = []
    for x in Stocks.query.all():
        value = get_latest_value(Investments.query.order_by(Investments.id.desc()).filter_by(ticker=x.ticker).first())
        query.append([x.stock.lower(), x.ticker, value, calculate_percentage(value), x.image_link])
    return query

def get_image_links(ticker, stock):
    link_1 = "https://eodhistoricaldata.com/img/logos/US/" + ticker.upper() + ".png"
    link_2 = "https://eodhistoricaldata.com/img/logos/US/" + ticker.lower() + ".png"
    link_3 = "https://cryptologos.cc/logos/" + stock.lower().replace(" ","-") + "-" + ticker.lower() + "-logo.png"
    return [link_1, link_2, link_3]


@app.route("/")
def home():
    print(check_number)
    return render_template("overview.html", investment_list=top("Both"), overview_line = check_number_overview_line[check_number])

@app.route("/stocks")
def stocks():
    return render_template("overview.html", investment_list=top("Stock"), overview_line = check_number_overview_line[check_number])


@app.route("/cryptos")
def cryptos():
    return render_template("overview.html", investment_list=top("Crypto"), overview_line = check_number_overview_line[check_number])

@app.route("/<stock_ticker>")
def stock(stock_ticker):
    row = None
    for investment in Stocks.query.all():
        if stock_ticker == investment.ticker or stock_ticker == investment.stock:
            image_link = investment.image_link
            row = Investments.query.filter_by(ticker=investment.ticker).order_by(Investments.id.desc()).first()
            break
    if not row: 
        for investment in Cryptos.query.all():
            if stock_ticker == investment.ticker or stock_ticker == investment.stock:
                image_link = investment.image_link
                row = Investments.query.filter_by(ticker=investment.ticker).order_by(Investments.id.desc()).first()
                break
    if row: 
        value = get_latest_value(row)
        return render_template("stock.html", stock_name=row.stock, stock_ticker=row.ticker, 
        stock_price = "{:,.2f}".format(value), last_updated = format_time(row.updated),
        percentage = calculate_percentage(value), image_link = image_link, overview_line = check_number_overview_line[check_number])
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


