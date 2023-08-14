import requests
import re

'''Метод get_init_info() возвращает базовую инфу о модели в виде словаря используется для частого сбора данных
    о работе принтеров
    {'ip_address': '192.168.1.36', 
    'prod': 'KYOCERA', 
    'locate': 'Olimp'}
    
    
    Метод get_full_info() используется для получения всех данных по принтеру, для разового занесения в базу
    возвращает словарь, со всеми данными
    '''


#   класс PeoplePrinterInit содержит базовые функции для проверки ip и принтера
class PeoplePrinterInit:

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.prod = self.get_prod_printer
        self.locate = self.find_locate(ip_address)

    def __str__(self):
        pass

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

    def get_init_info(self):
        init_info = {'ip_address': self.ip_address, 'prod': self.prod, 'locate': self.locate}
        return init_info


#   класс получает всю инфу, которая может понадобиться
class PeoplePrinter(PeoplePrinterInit):
    def __int__(self):
        if self.prod == 'KYOCERA':
            self.data = KyoceraMajor

        elif self.prod == 'HP':
            self.data = HpMajor


    def info(self):
        # возвращает словарь со всевозможными данными
        return self.prod, self.ip_address, self.locate


class KyoceraMajor(PeoplePrinter):
    '''Класс используется для больинства моделей Kyocera, получает всю инфу'''
    def __int__(self):
        url_counter = f'http://{self.ip_address}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
        url_toner = f'http://{self.ip_address}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
        url_info = f'http://{self.ip_address}/js/jssrc/model/dvcinfo/dvcconfig/DvcConfig_Config.model.htm'

        headers = {'Cookie': 'rtl=0; css=0',
                   'Referer': f"http://{self.ip_address}/startwlm/Start_Wlm.htm"}

        self.page_code_config = requests.get(url_counter, headers=headers)
        self.page_code_toner = requests.get(url_toner, headers=headers)
        self.page_code_info = requests.get(url_info, headers=headers)

    def get_toner_prints(self):
        print('test')


class HpMajor(PeoplePrinter):
    pass



if __name__ == "__main__":
    ip = '192.168.4.162'
    printer = PeoplePrinter(ip)
    print(printer.info())


