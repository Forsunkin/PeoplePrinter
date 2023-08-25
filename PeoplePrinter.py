import re
import requests
from bs4 import BeautifulSoup
import time


'''Класс инициализирует новые принтеры, собирая базовую инфу
    Производитель : prod, Локацию - отель в котором находится: locate и ip_address
    PeoplePrinter(ip).init() возвращает базовую инфу для инициализации нового принтера
    ('192.168.1.36', 'KYOCERA', 'Olimp')
    '''


class PeoplePrinter:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.page = self.get_page_printer
        self.locate = self.find_locate(ip_address)
        self.prod = self.get_prod_printer

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
    def get_page_printer(self):
        r = ''
        try:
            url = f'http://{self.ip_address}'
            response = requests.get(url)
            r = r.history
        except requests.exceptions.ConnectionError:
            r = 'ConnectTimeout'
        finally:
            return r

    @property
    def get_prod_printer(self):
        prod = ''
        try:
            if 'KYOCERA' in self.page:
                prod = 'KYOCERA'
            elif 'HP LaserJet' in self.page:
                prod = 'HP'
            elif 'Pantum' in self.page:
                prod = 'PANTUM'
            else:
                prod = self.page
                return prod
        finally:
            return prod

    def init_info(self):
        return self.ip_address, self.prod, self.locate


class KyoceraMajor(PeoplePrinter):
    def __init__(self, ip_address):
        super().__init__(ip_address)
        self.headers = {'Cookie': 'rtl=0; css=0', 'Referer': f"http://{self.ip_address}/startwlm/Start_Wlm.htm"}
        self._page_info = self.page_info()
        self._page_toner = self.page_toner()
        self._page_counter = self.page_counter()

    def page_info(self):
        url_info = f'http://{self.ip_address}/js/jssrc/model/dvcinfo/dvcconfig/DvcConfig_Config.model.htm'
        page_code_info = requests.get(url_info, headers=self.headers)
        return page_code_info.text

    def page_toner(self):
        url_toner = f'http://{self.ip_address}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
        page_code_toner = requests.get(url_toner, headers=self.headers)
        return page_code_toner.text

    def page_counter(self):
        url_counter = f'http://{self.ip_address}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
        page_code_counter = requests.get(url_counter, headers=self.headers)
        return page_code_counter.text

    @property
    def mac(self):
        mac_address = re.findall(r".*macAddress = '(.*)'", self._page_info)[0]     # получить mac адресс
        return mac_address

    @property
    def host_name(self):
        host_name = re.findall(r".*hostName = '(.*)'", self._page_info)[0]
        return host_name
    @property
    def model(self):
        model = re.findall(r".*model = '(.*)'", self._page_info)[0]
        return model

    @property
    def toner(self):
        toner_lvl = 'Error'
        try:
            data_toner = re.findall(r".*parseInt\('(\d*)',10\)\)", self._page_toner)  # получить остаток тонера
            toner_lvl = int(data_toner[0])
        except (ValueError, IndexError):
            pass
        finally:
            return toner_lvl

    @property
    def prints_count(self):
        printed_total = re.findall(r".*printertotal = \('(\d*)'\)", self._page_counter)[0]  # получить отпечатанные листы
        copy_total = re.findall(r".*copytotal = \('(\d*)'\)", self._page_counter)[0]  # получить сканы
        prints_count = int(printed_total) + int(copy_total)  # получить cумму
        return prints_count

    def info(self):
        return {'ip_address': self.ip_address, 'mac_address': self.mac, 'host_name': self.host_name, 'prod': self.prod,
                'model': self.model, 'locate': self.locate, 'toner_lvl': self.toner, 'prints_count': self.prints_count,
                'status': 'Done'}


class HPMajor(PeoplePrinter):
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

    def info(self):
        return {'ip_address': self.ip_address, 'mac_address': self.mac, 'host_name': self.host_name, 'prod': self.prod,
                'model': self.model, 'locate': self.locate, 'toner_lvl': self.toner, 'prints_count': self.prints_count,
                'status': 'Done'}


class PantumMajor(PeoplePrinter):

    def page_info(self):
        url = f'http://{self.ip_address}/js/jssrc/model/dvcinfo/dvcconfig/DvcConfig_Config.model.htm?arg1=0'
        page = requests.get(url).text
        return page

    @property
    def mac(self):
        mac_address = re.findall(r".*macAddress = '(.*)'", self.page_info())
        return mac_address

    @property
    def host_name(self):
        host_name = re.findall(r".*hostName = '(.*)'", self.page_info())
        return host_name

    @property
    def model(self):
        model = re.findall(r".*model = '.* (.*)'", self.page_info())
        return model

    def info(self):
        return {'ip_address': self.ip_address, 'mac_address': self.mac, 'host_name': self.host_name, 'prod': self.prod,
                'model': self.model, 'locate': self.locate, 'toner_lvl': self.toner, 'prints_count': self.prints_count,
                'status': 'Done'}


if __name__ == "__main__":
    ip = '192.168.1.88'
    printer = PantumMajor(ip)
    print(printer.init_info())
