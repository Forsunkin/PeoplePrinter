import sqlite3, re, requests, datetime
from bs4 import BeautifulSoup
from kostili import kostil_base_get_list_ip as list_ip  # Временный костыль ip_list - список Ip адрессов

sqlite_connection = sqlite3.connect('people_printers.db')
print("Подключен к people_printers.db SQLite")


def getting_info():
    for ip_address in list_ip():
        print(ip_address)


def create_table():
    cursor = sqlite_connection.cursor()
    sqlite_create_table = f'''CREATE TABLE if not exists run (
                        ip_address TEXT,
                        mac_address TEXT,
                        host_name TEXT,
                        prod TEXT,
                        model TEXT,
                        locate TEXT,
                        toner_lvl INT,
                        prints_count INT,
                        cartridge TEXT,
                        zamena_toner TEXT,
                        otpechatano_cartrige INT,
                        ottisk_ostalos INT,
                        status TEXT,
                        datetime TEXT
    );'''

    cursor.execute(sqlite_create_table)
    print('created')
    sqlite_connection.commit()
    print('close')
    sqlite_connection.close()


if __name__ == "__main__":
    create_table()
