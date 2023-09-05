import requests
import re
from src.manufacturers.KYOCERA.major_kyocera import KyoceraMajor

""" Класс инициализирует новые принтеры, собирая базовую инфу
    Производитель : prod, Локацию: locate - сеть в котором находится принтер: locate
    InitPrinter(ip).init_info возвращает базовую инфу для инициализации нового принтера
    ('192.168.1.36', 'KYOCERA', 'Olimp')
"""


class InitPrinter:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.main_page = self.__get_main_page_printer()
        self.locate = self.find_locate(ip_address)
        self.prod = self.get_prod_printer()

    @staticmethod
    def find_locate(ip_address):
        f = re.findall(r"192.168.(\d*).\d*", ip_address)[0]
        if f == '1':
            locate = 'Olimp'
        elif f == '2':
            locate = 'Summarinn'
        elif f == '4':
            locate = 'Aurum'
        else:
            locate = 'Неизвестно'
        return locate

    def __get_main_page_printer(self):
        r = None
        detect_refresh = r'(http-equiv="refresh")'   # regular ex for find refresh redirect
        redirect_url = r'url=(.*)"'                  # read new url
        url = f'http://{self.ip_address}/'
        try:
            r = requests.get(url).text
            if re.findall(detect_refresh, r):
                re_url = re.findall(redirect_url, r)[0]
                new_url = url+re_url
                r = requests.get(new_url).text      # getting redirect page
                return r
        except requests.exceptions.ConnectionError:
            r = 'ConnectTimeout'
        finally:
            return r

    def get_prod_printer(self):
        prod = 'Неопределен'
        factory = ['KYOCERA', 'HP', 'PANTUM']
        for x in factory:
            if x in self.main_page:
                prod = x
            else:
                pass
        return prod

    def init_info(self):
        return self.ip_address, self.prod, self.locate

    # def full_info(self, printer):
    #     return {
    #             'ip_address': self.ip_address,
    #             'mac_address': printer.mac,
    #             'host_name': printer.host_name,
    #             'prod': self.prod,
    #             'model': printer.model,
    #             'locate': self.locate,
    #             'toner_lvl': printer.toner,
    #             'prints_count': printer.prints_count,
    #             'status': 'Done'
    #             }


if __name__ == "__main__":
    ip = '192.168.1.33'
    printer = InitPrinter(ip)
    print(printer.init_info())
