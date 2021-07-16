from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, asc, Float
from sqlalchemy.orm.attributes import InstrumentedAttribute
from .utils import get_latest_value, calculate_percentage

db = SQLAlchemy()

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
        
    @staticmethod
    def get_all_stocks(check_number):
        query = []
        for x in Stocks.query.all():
            value = get_latest_value(check_number, Investments.query.order_by(Investments.id.desc()).filter_by(ticker=x.ticker).first())
            query.append([x.stock.lower(), x.ticker, value, calculate_percentage(check_number, value), x.image_link])
        return query

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

    @staticmethod
    def get_all_cryptos(check_number):
        query = []
        for x in Cryptos.query.all():
            value = get_latest_value(check_number, Investments.query.order_by(Investments.id.desc()).filter_by(ticker=x.ticker).first())
            query.append([x.stock.lower(), x.ticker, value, calculate_percentage(check_number, value), x.image_link])
        return query
