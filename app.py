import numpy as np

from flask import Flask, render_template, redirect, url_for, request
import matplotlib
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

@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
     conn = get_db_connection()
     data = conn.execute("SELECT * FROM sold").fetchall()
     columnnames = ["ID","Address","Date Sold","Price($)","# of Beds","Size(m²)"]
     df = pd.DataFrame(data, columns = columnnames)
     columnnames.remove("ID")
     columnnamesx = columnnames
     columnnamesy = [i for i in columnnames if pd.api.types.is_any_real_numeric_dtype(df[i])]
     if request.method =="POST":
          labelx = request.form.get("x")
          labely = request.form.get("y")
          x = df[labelx]
          y = df[labely]
          cdata= [{'x':nx,'y':ny} for nx,ny in zip(x,y)]
          #make it so that dates work with trendline
          if pd.api.types.is_numeric_dtype(x):
               slope, intercept = np.polyfit(x, y, deg=1) #finds slope and intercept using x and y as points
               trendline = [{'x':min(x),'y':intercept + slope * min(x)},{'x':max(x),'y':intercept + slope * max(x)}]
          else:
               trendline = []
     else:
          cdata=[]
          trendline = []
          labelx=''
          labely=''
     return render_template('graphs.html',optionsx = columnnamesx,optionsy=columnnamesy,cdata=cdata, labelx = labelx, labely=labely,trendlinedata = trendline)

@app.route('/predict')
def predict():
     return render_template('predict.html')

@app.route('/trends')
def trends():
     return render_template('trends.html')
    