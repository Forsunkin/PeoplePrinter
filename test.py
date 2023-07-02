import requests
import re
from bs4 import BeautifulSoup
from kostili import kostil_base_get_list_ip as list_ip      # Временный костыль ip_list - список Ip адрессов


def get_prints_toner_kyocera(ip_address):
    url_counter = f'http://{ip_address}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
    url_toner = f'http://{ip_address}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
    url_info = f'http://{ip_address}/js/jssrc/model/dvcinfo/dvcconfig/DvcConfig_Config.model.htm'

    headers = {'Cookie': 'rtl=0; css=0',
                     'Referer': f"http://{ip_address}/startwlm/Start_Wlm.htm"}

    page_code_config = requests.get(url_counter, headers=headers)
    page_code_toner = requests.get(url_toner, headers=headers)
    page_code_info = requests.get(url_info, headers=headers)

    # Получение данных ко-ва оттисков
    try:
        printed_total = re.findall(r".*printertotal = \('(\d*)'\)", page_code_config.text)# получить отпечатанные листы
        copy_total = re.findall(r".*copytotal = \('(\d*)'\)", page_code_config.text)      # получить сканы
        prints_count = int(printed_total[0]) + int(copy_total[0])                         # получить cумму
    except (ValueError, IndexError):
        prints_count = 'Error'

    # Получение уровня тонера
    try:
        data_toner = re.findall(r".*parseInt\('(\d*)',10\)\)", page_code_toner.text)      # получить остаток тонера
        toner_lvl = int(data_toner[0])
    except (ValueError, IndexError):
        toner_lvl = 'Error'

    # Получение конфигурации
    try:
        mac_address = re.findall(r".*macAddress = '(.*)'", page_code_info.text)[0]     # получить mac адресс
        model = re.findall(r".*model = '(.*)'", page_code_info.text)[0]                # получть Модель
        # model = re.findall(r".*model = '.* (.*)'", page_code_info.text)[0]           # получть Модель без ECOSYS
        host_name = re.findall(r".*hostName = '(.*)'", page_code_info.text)[0]         # получить HostName

        f = re.findall(r"192.168.(\d*).\d*", ip_address)[0]                         # определение отеля
        if f == '1':
            locate = 'olimp'
        elif f == '2':
            locate = 'summarinn'
        elif f == '4':
            locate = 'aurum'
        else:
            locate = 'Неизвестно'


    finally:
        return {'ip_address': ip_address, 'mac_address': mac_address, 'host_name': host_name, 'prod':'KYOCERA',
                'model': model, 'locate': locate, 'toner_lvl': toner_lvl, 'prints_count': prints_count}


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

    td = bs_code_config.find("td", string='Аппаратный адрес:')
    td_parent = td.find_parent('tr')
    mac_address_unsorted = td_parent.find(class_='itemFont').text
    mac_address = (re.findall(r"(\w\w.*\w\w)", mac_address_unsorted)[0]).upper()

    td = bs_code_config.find("td", string='Имя хоста:')
    td_parent = td.find_parent('tr')
    host_name_unsorted = td_parent.find(class_='itemFont').text
    host_name = (re.findall(r"(\w\w.*\w\w)", host_name_unsorted)[0]).upper()


    td = bs_code_config.find("td", string='Название продукта:')
    td_parent = td.find_parent('tr')
    model = td_parent.find(class_='itemFont').text

    f = re.findall(r"192.168.(\d*).\d*", ip_address)[0]  # определение отеля
    if f == '1':
        locate = 'olimp'
    elif f == '2':
        locate = 'summarinn'
    elif f == '4':
        locate = 'aurum'
    else:
        locate = 'Неизвестно'


    return {'ip_address': ip_address, 'mac_address': mac_address, 'host_name': host_name, 'prod': 'KYOCERA',
            'model': model, 'locate': locate, 'toner_lvl': toner_lvl, 'prints_count': prints_count}


# логика на определение производителя принтера
def get_data_printer(ip_address):
    try:
        url = f'http://{ip_address}'
        response = requests.get(url)
        if 'KYOCERA' in response.text:
            data = get_prints_toner_kyocera(ip_address)
            return data

        elif 'HP LaserJet' in response.text:
            data = get_prints_toner_hp(ip_address)
            return data
        else:
            print(ip_address, ' - Неверный ip')
    except requests.exceptions.ConnectionError:
            print(ip_address, ' - ConnectTimeout')


def getting_info():
    for ip_address in list_ip():
            info = get_data_printer(ip_address)
            print(info)


if __name__ == "__main__":
    getting_info()

