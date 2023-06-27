from bs4 import BeautifulSoup
import requests
import re


def get_data_hp(obj):
    url_toner = f'''http://{obj}/info_suppliesStatus.html?tab=Home&menu=SupplyStatus'''
    url_config = f'''http://{obj}/info_configuration.html?tab=Home&menu=DevConfig'''

    source_code_config = requests.get(url_config).text
    source_code_toner = requests.get(url_toner).text

    bs_code_toner = BeautifulSoup(source_code_toner, "html.parser")
    bs_code_config = BeautifulSoup(source_code_config, "html.parser")

    # data_numbers = bs_code.find_all(class_='itemSpsFont') прочие данные с инфо о кол-ве оттисков с картриджем

    # data_config = bs_code_config.find_all('tr')

    data_toner = bs_code_toner.find(class_='SupplyName width35 alignRight')

    toner_lvl = re.findall(r"(\d+)", data_toner.text)
    counter = ''
    data_config = bs_code_config.find_all(class_='mainContentArea').find_all(class_='pad10')
    print(data_config)
    #father.findNext('div', {'class': 'class_value'}).findNext('div', {'id': 'id_value'}).findAll('a')
    #div[class=class_value]/div[id=id_value]
    # xpath
    # /html/body/div[@class='applicationPalette']
    # /table/tbody/tr[2]
    # /td[@class='rightContentPane']
    # /div[@class='pad10'][3]
    # /table[@class='mainContentArea']
    # /tbody
    # /tr[1]
    # /td[@class='itemFont']
    return 1




print(get_data_hp('192.168.1.95'))

