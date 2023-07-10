import requests
import re

'''Метод get_simple_info() возвращает базовую инфу о модели в виде словаря 
    {'ip_address': '192.168.1.36', 
    'prod': 'KYOCERA', 
    'locate': 'Olimp'}'''


class PeoplePrinterSimpleInfo:

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.prod = self.get_prod_printer
        self.locate = self.find_locate()

    def __str__(self):
        return str(self.get_simple_info())

    def find_locate(self):
        f = re.findall(r"192.168.(\d*).\d*", self.ip_address)[0]  # определение отеля
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
                return self, ' - Неверный ip'
        except requests.exceptions.ConnectionError:
            return self, ' - ConnectTimeout'
        finally:
            return self.prod

    def get_simple_info(self):
        d = {'ip_address': self.ip_address, 'prod': self.prod, 'locate':self.locate}

        return d


if __name__ == "__main__":
    ip = '192.168.1.36'
    printer = PeoplePrinterSimpleInfo(ip)
    print(printer.get_simple_info())


