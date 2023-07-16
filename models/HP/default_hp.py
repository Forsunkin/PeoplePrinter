import re
import requests
from bs4 import BeautifulSoup


def get_prints_toner_hp(ip_address):

    url_config = f'''http://{ip_address}/info_configuration.html?tab=Home&menu=DevConfig'''      # page with config info
    url_toner = f'''http://{ip_address}/info_suppliesStatus.html?tab=Home&menu=SupplyStatus'''   # page with toner

    page_code_config = requests.get(url_config).text
    page_code_toner = requests.get(url_toner).text

    bs_code_config = BeautifulSoup(page_code_config, "html.parser")
    bs_code_toner = BeautifulSoup(page_code_toner, "html.parser")

    # Получение данных ко-ва оттисков
    td = bs_code_config.find("td", string='Всего оттисков:')
    td_parent = td.find_parent('tr')
    prints_count = td_parent.find(class_='itemFont').text                                       # общее кол-во оттисков

    # Работа с данными по тонеру
    data_toner = bs_code_toner.find(class_='SupplyName width35 alignRight')
    toner_lvl = (re.findall(r"(\d+)", data_toner.text)[0])                                        # уровнеь тонера

    return int(toner_lvl), int(prints_count)


if __name__ == "__main__":
    pass
