from flask import Flask, render_template, session, request, url_for, redirect, g
import flask_login
from flask_login import LoginManager, UserMixin
from .new_investment import add_investment
from .utils import *
from .db import *
from .network_utils import *
from .user_login import *

app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.secret_key = 'key'


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app
db.init_app(app)

login_manager.init_app(app)

@app.before_request
def before_request():
    g.check_number = get_formatted_check_number(request.args.get('check_number'))
    

# if 1: check date 1: April 15, 2020
# if 2: check date 2: December 29th, 2020
# if 3: check date 3: March 16th, 2021


def top(investment_type, check_number):
    if investment_type == "Both":
        query = Assets.get_all_stocks(check_number) + Assets.get_all_cryptos(check_number)
    elif investment_type == "Crypto":
        query = Assets.get_all_cryptos(check_number)
    elif investment_type == "Stock":
        query = Assets.get_all_stocks(check_number)
    query.sort(key = lambda x: x[2], reverse = True)
    for entry in query:
        entry[2] = "{:,.2f}".format(entry[2])
    return query

@app.route("/")
def home():
    check_number = get_formatted_check_number(request.args.get('check_number'))
    return render_template("overview.html", investment_list=top("Both", check_number), overview_line = get_overview_line(check_number))

@app.route("/stocks")
def stocks():
    check_number = get_formatted_check_number(request.args.get('check_number'))
    return render_template("overview.html", investment_list=top("Stock", check_number), overview_line = get_overview_line(check_number))

@app.route("/cryptos")
def cryptos():
    check_number = get_formatted_check_number(request.args.get('check_number'))
    return render_template("overview.html", investment_list=top("Crypto", check_number), overview_line = get_overview_line(check_number))

@app.route("/<stock_ticker>")
def stock(stock_ticker):
    check_number = get_formatted_check_number(request.args.get('check_number'))
    asset_row = Assets.query.filter_by(ticker=stock_ticker).first()
    if asset_row:
        image_link = asset_row.image_link
        latest_row = Investments.query.order_by(Investments.id.desc()).filter_by(ticker=stock_ticker).first()
        value = get_latest_value(check_number, latest_row)
        return render_template("stock.html", stock_name=latest_row.stock, stock_ticker=latest_row.ticker, 
        stock_price = "{:,.2f}".format(value), last_updated = format_time(latest_row.updated),
        percentage = calculate_percentage(check_number, value), image_link = image_link, overview_line = get_overview_line(check_number))
    return error(stock_ticker)

@app.route("/search")
def search():
    check_number = get_formatted_check_number(request.args.get('check_number'))
    return redirect(url_for('stock', stock_ticker=request.args.get("q").upper(), check_number=check_number))

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


