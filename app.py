import numpy as np

from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
import sqlite3
import io
import base64
from datetime import datetime 

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("ttg_housing.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
     conn = get_db_connection()
     maxp = f"{conn.execute("SELECT MAX(price) FROM sold").fetchone()[0]:,.2f}"
     amt = f"{conn.execute("SELECT COUNT(price) FROM sold").fetchone()[0]:,}"
     avgp = f"{conn.execute("SELECT AVG(price) FROM sold").fetchone()[0]:,.2f}"
     conn.close()
     return render_template('index.html',max = maxp,avg=avgp,amt = amt)

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
     columnnamesy = [i for i in columnnames if pd.api.types.is_any_real_numeric_dtype(df[i])] #makes y axis options only int/float
     if request.method =="POST":
          labelx = request.form.get("x")
          labely = request.form.get("y")
          x = df[labelx]
          x = pd.to_datetime(x, errors='ignore') #if it isn't datetime, it will error but revert to previous state
          if x.dtype == datetime:
               pass
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
     conn.close()
     return render_template('graphs.html',optionsx = columnnamesx,optionsy=columnnamesy,cdata=cdata, labelx = labelx, labely=labely,trendlinedata = trendline)

@app.route('/predict',methods=['POST',"GET"])
def predict():
     conn = get_db_connection()
     data = conn.execute("SELECT * FROM sold").fetchall()
     df = pd.DataFrame(data)
     print(df)
     if request.method =="POST":
          try:
               bed = int(request.form.get("bedroomsInput"))
               size = int(request.form.get("sizeInput"))
               mperbed = size/bed
               def get_avg(x,y,value):
                    slope, intercept = np.polyfit(df[x], df[y], deg=1)
                    avg = intercept + slope * value
                    return avg
               valueb = get_avg(4,3,bed)
               values = get_avg(5,3,size)
               value = f"{(valueb+values)/2:,.2f}"
               minval = f"{min([valueb,values]):,.2f}"
               maxval = f"{max([valueb,values]):,.2f}"
          except ZeroDivisionError:
               bed = 0
               size = 0
               mperbed = 0
               value = 0
               minval = 0
               maxval = 0
     else:
          bed = 0
          size = 0
          mperbed = 0
          value = 0
          minval = 0
          maxval = 0
     conn.close()
     return render_template('predict.html', bed = bed, size = size, mperbed = mperbed, value = value, minval = minval, maxval = maxval)