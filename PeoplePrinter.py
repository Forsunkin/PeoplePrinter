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


    def get_prints_toner_kyocera(ip_address):
        url_counter = f'http://{ip_address}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
        url_toner = f'http://{ip_address}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
        url_info = f'http://{ip_address}/js/jssrc/model/dvcinfo/dvcconfig/DvcConfig_Config.model.htm'
        ''
        headers = {'Cookie': 'rtl=0; css=0',
                   'Referer': f"http://{ip_address}/startwlm/Start_Wlm.htm"}

        page_code_config = requests.get(url_counter, headers=headers)
        page_code_toner = requests.get(url_toner, headers=headers)
        page_code_info = requests.get(url_info, headers=headers)

        # Получение данных ко-ва оттисков
        try:
            printed_total = re.findall(r".*printertotal = \('(\d*)'\)",
                                       page_code_config.text)  # получить отпечатанные листы
            copy_total = re.findall(r".*copytotal = \('(\d*)'\)", page_code_config.text)  # получить сканы
            prints_count = int(printed_total[0]) + int(copy_total[0])  # получить cумму
        except (ValueError, IndexError):
            prints_count = 'Error'

        # Получение уровня тонера
        try:
            data_toner = re.findall(r".*parseInt\('(\d*)',10\)\)", page_code_toner.text)  # получить остаток тонера
            toner_lvl = int(data_toner[0])
        except (ValueError, IndexError):
            toner_lvl = 'Error'

        # Получение конфигурации
        try:
            mac_address = re.findall(r".*macAddress = '(.*)'", page_code_info.text)[0]  # получить mac адресс
            model = re.findall(r".*model = '(.*)'", page_code_info.text)[0]  # получть Модель
            # model = re.findall(r".*model = '.* (.*)'", page_code_info.text)[0]           # получть Модель без ECOSYS
            host_name = re.findall(r".*hostName = '(.*)'", page_code_info.text)[0]  # получить HostName

            f = re.findall(r"192.168.(\d*).\d*", ip_address)[0]  # определение отеля
            if f == '1':
                locate = 'olimp'
            elif f == '2':
                locate = 'summarinn'
            elif f == '4':
                locate = 'aurum'
            else:
                locate = 'Неизвестно'


        finally:
            return {'ip_address': ip_address, 'mac_address': mac_address, 'host_name': host_name, 'prod': 'KYOCERA',
                    'model': model, 'locate': locate, 'toner_lvl': toner_lvl, 'prints_count': prints_count}

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


class Kyocera(PeoplePrinter):
    def __init__(self, ip_address):
        super().__init__(ip_address)
        self.prod = '12333'




ip = '192.168.1.36'
printer = PeoplePrinter(ip)
print(printer.config)
