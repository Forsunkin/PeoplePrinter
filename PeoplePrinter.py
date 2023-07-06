import requests
import re
from kostili import kostil_base_get_list_ip as list_ip
from bs4 import BeautifulSoup


class PeoplePrinter:

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.mac_address = '123'
        self.prod = self.get_prod_printer
        self.locate = self.find_locate(ip_address)
        self.config = self.collect


    def __str__(self):
        return str(self.collect)

    @staticmethod
    def find_locate(ip_address):
        f = re.findall(r"192.168.(\d*).\d*", ip_address)[0]  # определение отеля
        if f == '1':
            locate = 'olimp'
        elif f == '2':
            locate = 'summarinn'
        elif f == '4':
            locate = 'aurum'
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
                return self.prod

            elif 'HP LaserJet' in response.text:
                self.prod = 'HP'
                return self.prod
            else:
                return self, ' - Неверный ip'
        except requests.exceptions.ConnectionError:
            return self, ' - ConnectTimeout'

    @property
    def collect(self):
        info_dict = {'ip_address': self.ip_address, 'mac_address': self.mac_address, 'host_name': 123,
                     'prod': self.prod,
                     'model': 123, 'locate': self.locate, 'toner_lvl': 123, 'prints_count': 123}
        return info_dict


ip = '192.168.1.36'
printer = PeoplePrinter(ip)
print(printer.config)
