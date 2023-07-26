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

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def commit(self):
        self.connection.commit()

if __name__ == "__main__":
    with Database() as db:
        print(db.execute(f"SELECT * FROM printers WHERE ip_address ='192.168.1.31'"))