import sqlite3
import click
# допилить интерфейс для общения с базой через модуль click

sqlite_connection = sqlite3.connect('printers_base.db')
cursor = sqlite_connection.cursor()

print("Подключен к SQLite")

def create_table():
    sql_query_create = f'''CREATE TABLE if not exists simple_data (
    ip TEXT, 
    name TEXT
    
    );'''
    cursor.execute(sql_query_create)

create_table()
def run():
    print('Запуск успешен')
    while True:

        ip_input = input('Введити ip принтера: ')
        name_input = input('Введите имя: ')
        # проверка на корректностьь ip

        insert_simple_data(ip_input, name_input)


def insert_simple_data(ip, name):
    sql_query_insert_ip_name = f'''INSERT INTO simple_data VALUES ('{ip}','{name}')'''
    cursor.execute(sql_query_insert_ip_name)
    sqlite_connection.commit()
    sqlite_connection.close()
    print('успех')


# Дописать логику с проверкой ip и получения всех данных
# запись в полную таблицу всех данных





run()