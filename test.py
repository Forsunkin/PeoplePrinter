import sqlite3
import datetime

sqlite_connection = sqlite3.connect('sqlite_python.db')
print("Подключен к SQLite")


dt_now = datetime.datetime.now()

sqlite_select_table_query = f'''SELECT * FROM test WHERE date < select max(date) from test'''
cursor = sqlite_connection.cursor()
ttt = cursor.execute(sqlite_select_table_query)
ttt = cursor.fetchall()

# select * from votes
# where creationDate > (select max(creationDate)-3 from votes)

sqlite_connection.commit()
sqlite_connection.close()

print(ttt)
