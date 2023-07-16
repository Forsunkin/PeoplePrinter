import sqlite3
import re
from kostili import kostil_base_get_list_ip as list_ip  # Временный костыль ip_list - список Ip адрессов
from PeoplePrinterSimpleInfo import PeoplePrinterSimple

sqlite_connection = sqlite3.connect('people_printers_test.db')
print("Подключен к people_printers.db SQLite")
cursor = sqlite_connection.cursor()

sqlite_create_table = f'''CREATE TABLE if not exists config_printers (
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


# синхронизация ip с базой конфигураций принеров, определение объекта locate
def sync_ip_in_base(ip_address):
    locate = PeoplePrinterSimple.find_locate(ip_address)
    cursor = sqlite_connection.cursor()
    # проверка наличия ip в базе
    checking = cursor.execute(f"SELECT * FROM config_printers WHERE ip_address ='{ip_address}'")

    if checking.fetchone() is None:
        # Ебануть класс для обработки принтера
        cursor.execute(f"INSERT INTO config_printers (ip_address, locate) VALUES ('{ip_address}', '{locate}')")
        sqlite_connection.commit()
        print(f"Добавлен новый ip: {ip_address} | {locate}")

    else:
        cursor.execute(f"UPDATE config_printers SET locate = '{locate}' WHERE ip_address = '{ip_address}'")
        sqlite_connection.commit()



def getting_info():
    print('Проверка...')
    for ip_address in list_ip():
        sync_ip_in_base(ip_address)     # логика для проверки наличия принтера в базе


if __name__ == "__main__":
    getting_info()
