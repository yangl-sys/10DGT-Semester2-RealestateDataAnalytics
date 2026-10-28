import re

from flask import Flask, render_template, redirect, url_for, request
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

@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
     conn = get_db_connection()
     data = conn.execute("SELECT * FROM sold").fetchall()
     columnnames = ["ID","Address","Date Sold","Price($)","# of Beds","Size(m²)"]
     df = pd.DataFrame(data, columns = columnnames)
     def graph(x,y):
          fig,ax =plt.subplots()
          ax.scatter(df[x],df[y])
          plt.xlabel(x)
          plt.ylabel(y)
          fig.autofmt_xdate()
          fig.savefig('static/graph.png')
          plt.close(fig)
     if request.method =="POST":
          labelx = request.form.get("x")
          labely = request.form.get("y")
          x = df[labelx]
          y = df[labely]
          cdata= [{'x':nx,'y':ny} for nx,ny in zip(x,y)]
     else:
          cdata=[]
          labelx=''
          labely=''
     return render_template('graphs.html',options = columnnames,cdata=cdata, labelx = labelx, labely=labely)

@app.route('/predict')
def predict():
     return render_template('predict.html')

@app.route('/trends')
def trends():
     return render_template('trends.html')
    