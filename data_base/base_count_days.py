import sqlite3
import datetime

sqlite_connection = sqlite3.connect('sqlite_python.db')
print("Подключен к SQLite")

cursor = sqlite_connection.cursor()

dt_now = datetime.datetime.now()

slite_create_table_date = f'''CREATE TABLE if not exists date_n_time (
	id int,
	d1 text
);'''


def get_date_between(table_name, column_with_date, count_days):
    sqlite_query_between = f'''SELECT * FROM {table_name} 
    WHERE {column_with_date} BETWEEN datetime('now', '-{count_days} days') AND datetime('now', 'localtime')'''

    inf = cursor.execute(sqlite_query_between)
    inf = cursor.fetchall()
    return inf


print(get_date_between('test', 'date', 14))  # params (table_name, column_with_date, count_days)

sqlite_connection.commit()
sqlite_connection.close()
print("Connection Close")
