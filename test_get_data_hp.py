import re, requests
from bs4 import BeautifulSoup


urlspa = "http://192.168.1.99/info_suppliesStatus.html?tab=Home&menu=SupplyStatus" # SPA

class HPData:
    def __init__(self, ip):
        self.get_da1ta = '123'

    def get_data(ip):
        url = f"http://{ip}/info_suppliesStatus.html?tab=Home&menu=SupplyStatus"
        source_code = requests.get(url).text
        bs_code = BeautifulSoup(source_code, "html.parser")
        data_numbers = bs_code.find_all(class_='itemSpsFont')
        data_toner = bs_code.find(class_='SupplyName width35 alignRight')


        toner_lvl = re.findall(r"(\d+)", data_toner.text)           #уровень тонера
        return data_numbers

    def get_config_hp(ip):
        url = f"http://{ip}/info_configuration.html?tab=Home&menu=DevConfig"
        source_code = requests.get(url).text
        bs_code = BeautifulSoup(source_code, "html.parser")
        print(bs_code)


ip = '192.168.1.99'

r = HPData(ip)
r.get_data()