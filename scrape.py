from pathlib import Path
import requests
import sqlite3
import json
import pandas as pd
from bs4 import BeautifulSoup

csv = pd.read_csv('websites/ttg_house_sales_2026 - ttg_house_sales_2026.csv')
csv=csv.to_dict(orient="records")
data = []
for i in csv:
    i["Amount"]=i["Amount"].replace(",", "").replace("$","")
    data.append(i)
connection = sqlite3.connect("ttg_housing.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS sold")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS 
    sold (
        houseid INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT UNIQUE,
        date TEXT,
        price INTEGER,
        beds INTEGER,
        size INTEGER
    )
''')

for i in data:
    cursor.execute('''
        INSERT INTO sold(
            address,
            date,
            price,
            beds,
            size
        ) VALUES(?,?,?,?,?)
        ON CONFLICT(address) DO NOTHING
    ''',(i["Address"],i["Date"],int(i["Amount"]),int(i["Bedrooms"]),int(i["Land Size"])))

connection.commit()
connection.close()