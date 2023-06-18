import sqlite3, re, requests, datetime
from bs4 import BeautifulSoup





sqlite_connection = sqlite3.connect('people_printers.db')
print("Подключен к SQLite")

