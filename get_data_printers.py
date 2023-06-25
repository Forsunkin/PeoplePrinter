import requests
from requests.exceptions import ConnectionError

import re
from bs4 import BeautifulSoup


class PeoplePrinter:


    def get_data_hp(self):
        url = f'''http://{self}/info_suppliesStatus.html?tab=Home&menu=SupplyStatus'''

        source_code = requests.get(url).text
        bs_code = BeautifulSoup(source_code, "html.parser")
        data_numbers = bs_code.find_all(class_='itemSpsFont')
        data_toner = bs_code.find(class_='SupplyName width35 alignRight')

        toner_lvl = re.findall(r"(\d+)", data_toner.text)
        counter = ''

        return toner_lvl, counter


    def get_data_kyocera(self):
        url_toner = f'http://{self}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
        url_counter = f'http://{self}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'

        headers_toner = {'Cookie': 'rtl=0; css=0',
                        'Referer': f"http://{self}/startwlm/Hme_Toner.htm"}

        headers_counter = {'Cookie': 'rtl=0; css=0',
                        'Referer': f'http://{self}/startwlm/Hme_Paper.htm'}


    # получение уровня тонера
        r_toner = requests.get(url_toner, headers=headers_toner)
        data_toner = re.findall(r".*parseInt\('(\d*)',10\)\)", r_toner.text)            # получить остаток тонера
        toner_lvl = int(data_toner[0])


    # получение кол-ва листов
        r_counter = requests.get(url_counter, headers=headers_counter)
        printer_total = re.findall(r".*printertotal = \('(\d*)'\)", r_counter.text)     # получить отпечатанные листы
        copy_total = re.findall(r".*copytotal = \('(\d*)'\)", r_counter.text)           # получить сканы
        counter = int(printer_total[0]) + int(copy_total[0])                            # получить тотал

        return toner_lvl, counter

    def get_data_printer(self):
        url = f'http://{self}'
        try:
            response = requests.get(url)
            if 'KYOCERA' in response.text:
                pp.get_data_kyocera(self)
            elif 'HP LaserJet' in response.text:
                pp.get_data_hp(self)

            else:
                return None
                print('Неверный ip')

        except ConnectionError:  # This is the correct syntax
            err = "Connection_Error"
            print(err)
            return err

    # логика на определение производителя принтера,


ip = '192.168.1.36'
pp = PeoplePrinter
print(pp.get_data_printer(ip))