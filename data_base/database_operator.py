import sqlite3


class Database(object):
    DB_LOCATION = '../people_printers.db'

    def __init__(self):
        self.connection = sqlite3.connect(Database.DB_LOCATION)
        self.cur = self.connection.cursor()

    def close(self):
        self.connection.close()

    def execute(self, sqlquery):
        self.cur.execute(sqlquery)

    # def executemany(self, many_new_data):
    #     """add many new data to database in one go"""
    #     self.create_table()
    #     self.cur.executemany('REPLACE INTO jobs printers(?, ?, ?, ?)', many_new_data)

    def create_table(self):
        """create a database table if it does not exist already"""
        self.cur.execute(f'''CREATE TABLE if not exists printers (
                        ip_address TEXT PRIMARY KEY,
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
                        datetime TEXT);''')
        print("Table printers is created")

    # Возвращает ip адреса из таблицы с принтерами

    def get_ip_db(self):
        ip_addresess = self.cur.execute('SELECT ip_address FROM printers')
        ip_addresess = self.cur.fetchall()
        return ip_addresess

    # Вовращает ip адреса из файла с ip
    # (временный костыль)
    @staticmethod
    def get_ip_txt():
        ip_list = []
        with open('ip_printers.txt') as f:
            file_list = f.read().splitlines()
            for ip in file_list:
                ip_list.append(ip)
        return ip_list

    def commit(self):
        self.connection.commit()


if __name__ == "__main__":
    db = Database()
    print(db.get_ip_db())
    print(db.get_ip_txt())
