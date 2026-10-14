from pathlib import Path
import requests
import sqlite3
import json

from bs4 import BeautifulSoup

data = []

connection = sqlite3.connect("ttg_housing.db")
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS 
    sold (
        houseid INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        price INTEGER,
        website TEXT,
        date TEXT,
        cars INTEGER,
        bath INTEGER,
        beds INTEGER
    )
''')

for file in Path("websites").iterdir():
    with open(file,"r",encoding = "utf-8") as html:
        soup = BeautifulSoup(html,"html.parser")

        data.append(soup)

print(data)
connection.commit()
connection.close()