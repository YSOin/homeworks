import string
import random


from flask import Flask

import pandas as pd


app = Flask(__name__)

@app.route("/generate_password")
def hello_world():
    generate_pass = ''.join([random.choice(
                        string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation)
                        for n in range(random.randint(10, 20))])
    return f"<p>{generate_pass}</p>"




@app.route("/calculate_average")
def calculate_average():
    df = pd.read_csv('files/hw.csv')
    average_height = round(df[' Height(Inches)'].mean(axis = 0, skipna = False), 2)
    average_weight = round(df[' Weight(Pounds)'].mean(axis = 0, skipna = False), 2)
    return f"""<p>Средний рост студентов: {average_height} - Inches</p>
    <p>Средний вес студентов: {average_weight} - Pounds</p>"""
