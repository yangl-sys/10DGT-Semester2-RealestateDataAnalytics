from pathlib import Path
import requests
import sqlite3
import json

from bs4 import BeautifulSoup

data = [["109 Hancock Road","29-09-2026",770000,3,1,2,452,"House"],]

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
        bath INTEGER,
        cars INTEGER,
        size INTEGER,
        type TEXT
    )
''')

for i in data:
    cursor.execute('''
        INSERT INTO sold(
            address,
            date,
            price,
            beds,
            bath,
            cars,
            size,
            type
        ) VALUES(?,?,?,?,?,?,?,?)
        ON CONFLICT(address) DO NOTHING
    ''',(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))

connection.commit()
connection.close()