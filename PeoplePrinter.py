import re
import requests


'''Класс инициализирует новые принтеры, собирая базовую инфу
    Производитель : prod, Локацию - отель в котором находится: locate и ip_address
    PeoplePrinter(ip).init() возвращает базовую инфу для инициализации нового принтера
    ('192.168.1.36', 'KYOCERA', 'Olimp')
    '''


class PeoplePrinter:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.prod = self.get_prod_printer
        self.locate = self.find_locate(ip_address)

    @staticmethod
    def find_locate(ip_address):
        f = re.findall(r"192.168.(\d*).\d*", ip_address)[0]  # определение отеля
        if f == '1':
            locate = 'Olimp'
        elif f == '2':
            locate = 'Summarinn'
        elif f == '4':
            locate = 'Aurum'
        else:
            locate = 'Неизвестно'
        return locate

    @property
    def get_prod_printer(self):
        try:
            url = f'http://{self.ip_address}'
            response = requests.get(url)
            if 'KYOCERA' in response.text:
                self.prod = 'KYOCERA'
            elif 'HP LaserJet' in response.text:
                self.prod = 'HP'
            else:
                self.prod = 'Неверный ip'
                return self.prod
        except requests.exceptions.ConnectionError:
            self.prod = 'ConnectTimeout'
            return self.prod
        finally:
            return self.prod

    def init_info(self):
        return self.ip_address, self.prod, self.locate

    def info(self):
        if self.prod == 'KYOCERA':
            return KyoceraMajor.full_info(self)
        elif self.prod == 'HP':
            return HpMajor.full_info(self)


class KyoceraMajor(PeoplePrinter):
    def full_info(self):
        return self.prod, self.locate, self.ip_address, 'test'


class HpMajor(PeoplePrinter):
    def full_info(self):
        return self.prod, self.locate, self.ip_address, 'test'

if __name__ == "__main__":
    ip = '192.168.1.36'
    printer = PeoplePrinter(ip)
    print(printer.info())