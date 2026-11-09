from pathlib import Path
import requests
import sqlite3
import json
import pandas as pd
from bs4 import BeautifulSoup

csv = pd.read_csv(input("csv path"))
csv=csv.to_dict(orient="records")
data = []
for i in csv:
    i["Amount"]=i["Amount"].replace(",", "").replace("$","")
    data.append(i)
connection = sqlite3.connect("ttg_housing.db")
cursor = connection.cursor()

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