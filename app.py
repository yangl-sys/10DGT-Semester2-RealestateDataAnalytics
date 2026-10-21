from flask import Flask, render_template, redirect, url_for
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import io
import base64
import matplotlib.dates as mdates
from datetime import datetime

# this makes the matplot stuff run on another thread to prevent "UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail."
matplotlib.use('Agg') 

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
     def graph(x,y,name):
          fig,ax =plt.subplots()
          ax.bar(df[x],df[y])
          if pd.api.types.is_datetime64_any_dtype(df[x]):
               print("Yes")
               ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %y'))
               fig.autofmt_xdate()
          else:
               print("No")
          fig.savefig(f'static/{name}.png')
          plt.close(fig)
     graph(2,3,"dateprice")
     graph(4,3,"sizeprice")
     return render_template('graphs.html')

@app.route('/predict')
def predict():
     return render_template('predict.html')

@app.route('/trends')
def trends():
     return render_template('trends.html')
    