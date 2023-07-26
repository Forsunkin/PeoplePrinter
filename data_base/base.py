import sqlite3, re, requests, datetime
from bs4 import BeautifulSoup
from kostili import kostil_base_get_list_ip as list_ip  # Временный костыль ip_list - список Ip адрессов
from database_operator import Database as db



if __name__ == "__main__":
    print(db.DB_LOCATION)
