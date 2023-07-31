from database_operator import Database


class Printers():
    db = Database()

    def __init__(self):
        self.ip_txt = self.db.get_ip_txt
        self.ip_db = self.db.get_ip_db

    def sync_addresses(self):
        for ip_address in self.ip_txt():
            if ip_address in self.ip_db():
                pass
            else:
                #Класс.получить инфу и добавить
                #Класс для обработки и получения всей инфы по отсутсвующему принтеру
                pass



if __name__ == "__main__":
    p = Printers()
    p.sync_addresses()