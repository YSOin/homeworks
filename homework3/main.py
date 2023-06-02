from http import HTTPStatus
from datetime import date

import requests
import pandas as pd


from webargs import validate, fields
from webargs.flaskparser import use_kwargs
from faker import Faker
from flask import Flask, render_template
from flask import request


fake = Faker(locale = "UK")
app = Flask(__name__, template_folder='templates')


def write_cdata(data):
    with pd.ExcelWriter(f'data.xlsx',
            mode = 'w') as writer:
        data.to_excel(writer, index = False)


@app.route("/generate_students")
@use_kwargs(
    {
        "count": fields.Int(
            missing=10,
            validate=[validate.Range(max=1000)]
        ),
    },
    location="query"
)
def generate_students(count):
    persons_generator_dict = {
        'First Name': [fake.first_name() for item in range(count+1)],
        'Last Name': [fake.last_name() for item in range(count+1)],
        'Birthday': [fake.date_between(start_date = date(1969,1,1),
                            end_date = date(2005,1,1))
                        for item in range(count+1)],
        'Email': [fake.email() for item in range(count+1)],
        'Password': [fake.password() for item in range(count+1)],
    }
    df = pd.DataFrame(persons_generator_dict,
        columns = ["First Name", "Last Name", "Birthday", "Email", "Password"])
    table = df.to_html(index = False)
    df.to_csv('static/data.csv', index = False)


    return render_template("at-leaderboard.html", table=table)


@app.route("/bitcoin_rate")
@use_kwargs(
    {
        "currency_code": fields.String(
            missing="USD",
        ),
        "convert": fields.Float(
            missing=1,
        )
    },
    location="query"
)
def get_bitcoin_value(currency_code, convert):
    currency_rates_data = requests.get('https://bitpay.com/api/rates', {})
    currency_data = requests.get('https://bitpay.com/currencies', {})
    if currency_rates_data.status_code not in (HTTPStatus.OK,):
        return Response(
            "ERROR: Something went wrong",
            status=result.status_code
        )
    elif currency_data.status_code not in (HTTPStatus.OK,):
        return Response(
            "ERROR: Something went wrong",
            status=result.status_code
        )
    currency_rates_list = currency_rates_data.json()
    currency_data_list = currency_data.json().get('data', {})
    currency_symbols = {item.get("code", str()):item.get("symbol", str()) for item in currency_data_list}
    currency_rates = {item.get("code", str()):item.get("rate", 0) for item in currency_rates_list}
    currency_symbol = currency_symbols.get(currency_code, None)
    currency_rate = currency_rates.get(currency_code, None)
    if currency_symbol is not None:
        return f"""
        <p style="font-size: 20px;">Курс {currency_symbols["BTC"]} - {currency_rate}{currency_symbol} за единицу</p>
        <p style="font-size: 20px;">Для покупки {convert} BTC  нужно {currency_rate*convert} {currency_code}
        """
    else:
        return f"<p>Curreny Error, {currency_code} not in database</p>"







if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
