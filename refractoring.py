import sqlite3
import re
from kostili import kostil_base_get_list_ip as list_ip  # Временный костыль ip_list - список Ip адрессов

sqlite_connection = sqlite3.connect('people_printers.db')
print("Подключен к people_printers.db SQLite")


def find_locate(ip_address):
    locate_param = re.findall(r"192.168.(\d*).\d*", ip_address)[0]  # определение отеля
    if locate_param == '1':
        locate = 'olimp'
    elif locate_param == '2':
        locate = 'summarinn'
    elif locate_param == '4':
        locate = 'aurum'
    else:
        locate = 'Неизвестно'
    return locate


# синхронизация ip с базой конфигураций принеров, определение объекта locate
def sync_ip_in_base(ip_address):
    cursor = sqlite_connection.cursor()
    locate = find_locate(ip_address)
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

    sqlite_connection.close()


def getting_info():
    print('Проверка...')
    for ip_address in list_ip():
        sync_ip_in_base(ip_address)     # логика для проверки наличия принтера в базе


if __name__ == "__main__":
    sync_ip_in_base('192.168.1.35')
