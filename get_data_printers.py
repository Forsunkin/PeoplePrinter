import requests
import re
from bs4 import BeautifulSoup


class PeoplePrinter:

    # def ident_printer(ip):
    #     try:
    #         r = requests.get(ip)
    # логика на определение производителя принтера,

    def get_data_hp(self):
        url = f'''http://{self}/info_suppliesStatus.html?tab=Home&menu=SupplyStatus'''

        source_code = requests.get(url).text
        bs_code = BeautifulSoup(source_code, "html.parser")
        data_numbers = bs_code.find_all(class_='itemSpsFont')
        data_toner = bs_code.find(class_='SupplyName width35 alignRight')

        toner_lvl = re.findall(r"(\d+)", data_toner.text)
        counter = ''

        return toner_lvl, counter
        # логика на получение данных
    def get_data_kyocera(self):
        url_toner = f'http://{self}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
        url_counter = f'http://{self}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'

    # получение уровня тонера
        r_toner = requests.get(url_toner)
        data_toner = re.findall(r".*parseInt\('(\d*)',10\)\)", r_toner.text)  # получить остаток тонера
        toner_lvl = int(data_toner[0])

    # получение кол-ва листов
        r_counter = requests.get(url_counter)
        printer_total = re.findall(r".*printertotal = \('(\d*)'\)", r_counter.text)     # получить отпечатанные листы
        copy_total = re.findall(r".*copytotal = \('(\d*)'\)", r_counter.text)           # получить сканы
        counter = int(printer_total[0]) + int(copy_total[0])                            # получить тотал

        return toner_lvl, counter

    def get_counter_kyocera(self):
        url_counter = f'http://{self}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'

        r_counter = requests.get(url_counter)
        printer_total = re.findall(r".*printertotal = \('(\d*)'\)", r_counter.text)       # получить отпечатанные листы
        copy_total = re.findall(r".*copytotal = \('(\d*)'\)", r_counter.text)             # получить сканы
        counter = int(printer_total[0]) + int(copy_total[0])                         # получить тотал
        return counter


    def get_toner_kyocera(self):
        url_toner = f'http://{self}/js/jssrc/model/startwlm/Hme_Toner.model.htm'

        r_toner = requests.get(url_toner)
        data_toner = re.findall(r".*parseInt\('(\d*)',10\)\)", r_toner.text)  # получить остаток тонера
        toner_lvl = int(data_toner[0])
        return toner_lvl



