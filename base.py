import sqlite3, re, requests, datetime
from bs4 import BeautifulSoup





sqlite_connection = sqlite3.connect('people_printers.db')
print("Подключен к SQLite")

def create_table():
    cursor = sqlite_connection.cursor()
    sqlite_create_table = f'''CREATE TABLE if not exists data_printers (
    	ip TEXT,
    	mac TEXT,
    	hostname TEXT,
    	firma TEXT,
    	kartrige TEXT,
    	object TEXT,
    	locate TEXT,
    	PRIMARY KEY(mac)
    );'''

    cursor.execute(sqlite_create_table)
    sqlite_connection.commit()
    sqlite_connection.close()

def get