from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
     
     return render_template('index.html')

@app.route('/raw')
def raw():
     return render_template('raw.html')

@app.route('/graphs')
def graphs():
     return render_template('graphs.html')

@app.route('/predict')
def predict():
     return render_template('predict.html')

@app.route('/trends')
def trends():
     return render_template('trends.html')
    