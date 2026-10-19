from flask import Flask, render_template, redirect, url_for
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import io
import base64
import matplotlib.dates as mdates
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("ttg_housing.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
     
     return render_template('index.html')

@app.route('/raw')
def raw():
     conn = get_db_connection()
     data = conn.execute("SELECT * FROM sold").fetchall()
     conn.close()
     return render_template('raw.html',data=data)

@app.route('/graphs')
def graphs():
     conn = get_db_connection()
     data = conn.execute("SELECT * FROM sold").fetchall()
     df = pd.DataFrame(data)
     fig,ax =plt.subplots()
     ax.bar(df[2],df[3])
     ax.xaxis.set_major_locator(mdates.AutoDateLocator())
     ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
     fig.autofmt_xdate()
     fig.show()
     return render_template('graphs.html')

@app.route('/predict')
def predict():
     return render_template('predict.html')

@app.route('/trends')
def trends():
     return render_template('trends.html')
    