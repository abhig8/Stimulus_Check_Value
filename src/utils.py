import datetime

def get_curr_time():
    return datetime.datetime.now().strftime('%m-%d-%Y %I:%M:%S %p')
    # return('07-12-2021 01:00:00 PM')

def format_time(date_time):
    return date_time[:10] + " at" + date_time[10:] + " " + "PST"

def calculate_percentage(check_number, price):
    if check_number == 1:
        return round((price-1200)/12)
    elif check_number == 2:
        return round((price-600)/6)
    elif check_number == 3:
        return round((price-1400)/14)

def get_all_curr_values(curr_price, first_check_val, second_check_val, third_check_val):
    first_val = "{0:.2f}".format(1200/float(first_check_val)*curr_price)
    second_val = "{0:.2f}".format(600/float(second_check_val)*curr_price)
    third_val = "{0:.2f}".format(1400/float(third_check_val)*curr_price)
    return [first_val, second_val, third_val]
    
def get_latest_value(check_number, row):
    if check_number == 1:
        return float(row.first_check)
    elif check_number == 2:
        return float(row.second_check)
    elif check_number == 3:
        return float(row.third_check)

def get_all_curr_values(curr_price, first_check_val, second_check_val, third_check_val):
    first_val = "{0:.2f}".format(1200/float(first_check_val)*curr_price)
    second_val = "{0:.2f}".format(600/float(second_check_val)*curr_price)
    third_val = "{0:.2f}".format(1400/float(third_check_val)*curr_price)
    return [first_val, second_val, third_val]

# finding date check date 1: April 15, 2020
# finding date check date 2: December 29th, 2020
# finding date check date 3: March 16th, 2021
def get_timestamp(check_number):
    if check_number == 1:
        timestamp1 = '1586908800'
        timestamp2 = '1586995200'
    elif check_number == 2:
        timestamp1 = '1609200000'
        timestamp2 = '1609286400'
    elif check_number == 3:
        timestamp1 = '1615852800'
        timestamp2 = '1615939200'
    return timestamp1, timestamp2

def get_overview_line(check_number):
    if check_number == 1:
        return "Possible gains on a $1200 investment made on April 15, 2020"
    if check_number == 2:
        return "Possible gains on a $600 investment made on December 29, 2020"
    if check_number == 3:
        return "Possible gains on a $1400 investment made on March 16, 2021"

def get_formatted_check_number(check_number):
    if check_number in ['2', '3'] or check_number in [2, 3]:
        return int(check_number)
    return 1

def get_image_links(ticker, stock):
    link_1 = "https://eodhistoricaldata.com/img/logos/US/" + ticker.upper() + ".png"
    link_2 = "https://eodhistoricaldata.com/img/logos/US/" + ticker.lower() + ".png"
    link_3 = "https://cryptologos.cc/logos/" + stock.lower().replace(" ","-") + "-" + ticker.lower() + "-logo.png"
    return [link_1, link_2, link_3]