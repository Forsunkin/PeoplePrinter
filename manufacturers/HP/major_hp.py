import re
import requests
from bs4 import BeautifulSoup
from InitPrinter import InitPrinter


class HPMajor(InitPrinter):
    def __init__(self, ip_address):
        super().__init__(ip_address)
        self._page_info = self.page_info()
        self._page_toner = self.page_toner()

    def page_info(self):
        url_info = f'''http://{self.ip_address}/info_configuration.html?tab=Home&menu=DevConfig'''
        page_code_info = requests.get(url_info).text
        bs_code_info = BeautifulSoup(page_code_info, "html.parser")
        return bs_code_info

    def page_toner(self):
        url_toner = f'''http://{self.ip_address}/info_suppliesStatus.html?tab=Home&menu=SupplyStatus'''  # page with toner
        page_code_toner = requests.get(url_toner).text
        bs_code_toner = BeautifulSoup(page_code_toner, "html.parser")
        return bs_code_toner

    @property
    def mac(self):
        td = self.page_info().find("td", string='Аппаратный адрес:')
        td_parent = td.find_parent('tr')
        mac_address_unsorted = td_parent.find(class_='itemFont').text
        mac_address = (re.findall(r"(\w\w.*\w\w)", mac_address_unsorted)[0]).upper()
        return mac_address

    @property
    def host_name(self):
        td = self.page_info().find("td", string='Имя хоста:')
        td_parent = td.find_parent('tr')
        host_name_unsorted = td_parent.find(class_='itemFont').text
        host_name = (re.findall(r"(\w\w.*\w\w)", host_name_unsorted)[0]).upper()
        return host_name

    @property
    def model(self):
        td = self.page_info().find("td", string='Название продукта:')
        td_parent = td.find_parent('tr')
        model = td_parent.find(class_='itemFont').text
        return model

    @property
    def toner(self):
        data_toner = self.page_toner().find(class_='SupplyName width35 alignRight')
        toner_lvl = (re.findall(r"(\d+)", data_toner.text)[0])
        return toner_lvl

    @property
    def prints_count(self):
        td = self.page_info().find("td", string='Всего оттисков:')
        td_parent = td.find_parent('tr')
        prints_count = td_parent.find(class_='itemFont').text
        return prints_count

    @property
    def info(self):
        return {'ip_address': self.ip_address, 'mac_address': self.mac, 'host_name': self.host_name, 'prod': self.prod,
                'model': self.model, 'locate': self.locate, 'toner_lvl': self.toner, 'prints_count': self.prints_count,
                'status': 'Done'}


if __name__ == "__main__":
    ip = '192.168.1.95'
    print(HPMajor(ip).info)