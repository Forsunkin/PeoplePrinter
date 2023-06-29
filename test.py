import requests
import re
from bs4 import BeautifulSoup
from kostili import kostil_base_get_list_ip as list_ip      # Временный костыль ip_list - список Ip адрессов


def get_prints_toner_kyocera(ip_address):
    url_counter = f'http://{ip_address}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
    url_toner = f'http://{ip_address}/js/jssrc/model/startwlm/Hme_Toner.model.htm'

    headers = {'Cookie': 'rtl=0; css=0',
                     'Referer': f"http://{ip_address}/startwlm/Start_Wlm.htm"}

    page_code_config = requests.get(url_counter, headers=headers)
    page_code_toner = requests.get(url_toner, headers=headers)

    # Получение данных ко-ва оттисков
    try:
        printed_total = re.findall(r".*printertotal = \('(\d*)'\)", page_code_config.text)# получить отпечатанные листы
        copy_total = re.findall(r".*copytotal = \('(\d*)'\)", page_code_config.text)      # получить сканы
        prints_count = int(printed_total[0]) + int(copy_total[0])                         # получить cумму
    except (ValueError, IndexError):
        prints_count = 'Error'

    # получение уровня тонера
    try:
        data_toner = re.findall(r".*parseInt\('(\d*)',10\)\)", page_code_toner.text)      # получить остаток тонера
        toner_lvl = int(data_toner[0])
    except (ValueError, IndexError):
        toner_lvl = 'Error'

    finally:
        return toner_lvl, prints_count


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



def get_data_printer(ip_address):
    # логика на определение производителя принтера,
    url = f'http://{ip_address}'
    response = requests.get(url)
    if 'KYOCERA' in response.text:
        data = get_prints_toner_kyocera(ip_address)
        print(f'{ip_address}: Toner - {data[0]}, Prints - {data[1]}')

    elif 'HP LaserJet' in response.text:
        data = get_prints_toner_hp(ip_address)
        print(f'{ip_address}: Toner - {data[0]}, Prints - {data[1]}')
    else:
        print(ip_address, 'Неверный ip')


def getting_info():
    for ip_address in list_ip():
        try:
            info = get_data_printer(ip_address)
        except (requests.exceptions.ConnectTimeout):
            print(f'{ip_address}- ConnectTimeout')







getting_info()