import sqlite3
import json

from bs4 import BeautifulSoup

connection = sqlite3.connect("ttg_housing.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS bookings")



cursor.execute('''
    CREATE TABLE sold (
        houseid INTEGER PRIMARYKEY AUTOINCREMENT
        address TEXT,
        price INTEGER,
        website TEXT,
        date TEXT,
        cars INTEGER,
        bath INTEGER,
        beds INTEGER,

    )
''')

cursor.execute('''
    CREATE TABLE selling (
        houseid INTEGER PRIMARYKEY AUTOINCREMENT
        address TEXT,
        price INTEGER,
        website TEXT,
        cars INTEGER,
        bath INTEGER,
        beds INTEGER,
    )
''')

connection.commit()
connection.close()