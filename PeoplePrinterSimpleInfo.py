import requests
import re

'''Метод get_simple_info() возвращает базовую инфу о модели в виде словаря используется для частого сбора данных
    о работе принтеров
    {'ip_address': '192.168.1.36', 
    'prod': 'KYOCERA', 
    'locate': 'Olimp'}
    
    
    Метод get_full_info() используется для получения всех данных по принтеру, для разового занесения в базу
    возвращает словарь, со всеми данными
    '''


#   класс содержит базовые функции для проверки ip и принтера
class PeoplePrinterInit:

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.prod = self.get_prod_printer
        self.locate = self.find_locate(ip_address)

    def __str__(self):
        return str(self.get_simple_info())

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
                return self, ' - Неверный ip'
        except requests.exceptions.ConnectionError:
            return self, ' - ConnectTimeout'
        finally:
            return self.prod

    def get_init_info(self):
        init_info = {'ip_address': self.ip_address, 'prod': self.prod, 'locate': self.locate}
        return init_info


#   класс получает всю инфу, которая может понадобиться
class PeoplePrinter(PeoplePrinterInit):
    def __int__(self):
        if self.prod == 'KYOCERA':
            self.data = KyoceraMajor




    def get_full_info(self):
        # возвращает словарь со всевозможными данными
        return self.prod, self.ip_address, self.locate


class KyoceraMajor(PeoplePrinter):

    def __int__(self):
        url_counter = f'http://{self.ip_address}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
        url_toner = f'http://{self.ip_address}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
        url_info = f'http://{self.ip_address}/js/jssrc/model/dvcinfo/dvcconfig/DvcConfig_Config.model.htm'

        headers = {'Cookie': 'rtl=0; css=0',
                   'Referer': f"http://{self.ip_address}/startwlm/Start_Wlm.htm"}

        page_code_config = requests.get(url_counter, headers=headers)
        page_code_toner = requests.get(url_toner, headers=headers)
        page_code_info = requests.get(url_info, headers=headers)


if __name__ == "__main__":
    ip = '192.168.1.36'
    printer = PeoplePrinter(ip)
    print(printer.get_full_info())


